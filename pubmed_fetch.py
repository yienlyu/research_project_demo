#!/usr/bin/env python3
"""
pubmed_fetch.py -> no need to install any packages

usage:
    python pubmed_fetch.py

output:
    literature/search_log.md
    literature/results/[date]_S4.csv           -> lists
    literature/results/[date]_S4_abstracts.txt -> abstracts (for Gemini Notebook)
"""

import csv, json, os, time, urllib.parse, urllib.request
from datetime import date

# -----
# your turn!
# -----
EMAIL = "example@gmail.com"               # NCBI needs to know who you are
API_KEY = ""                              # optional, key speed: 3 req/s to 10
VERSION = "v2.0"                          # match the version search-strategy.md

MAX_RECORDS = 0                           # 0 = fetch ALL hits, any number = cap
ESEARCH_CAP = 10000                       # PubMed esearch hard limit (NCBI)
NOTEBOOK_WORD_LIMIT = 500_000             # Gemini Notebook, per source

# put your queries here!
QUERIES = {
    "S1": '("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab])',
    "S2": '("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab])',
    "S3": '("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab])',
}
FINAL_ID = "S4"
FINAL_QUERY = f'({QUERIES["S1"]}) AND ({QUERIES["S2"]}) AND ({QUERIES["S3"]})'
# -----

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
_last = [0.0]
_gap = 0.11 if API_KEY else 0.36          # safety margin


def _get(endpoint, params, retries=3):
    p = {**params, "tool": "gdgoc-pubmed-workshop", "email": EMAIL}
    if API_KEY:
        p["api_key"] = API_KEY
    url = BASE + endpoint + "?" + urllib.parse.urlencode(p)
    err = None
    for attempt in range(retries):
        wait = _gap - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:
            err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"NCBI connection failed, retried {retries} times: {err}")


def count_hits(term):
    """
    Return (total hits in PubMed, the query PubMed actually ran).

    key: esearchresult.count - total amount in PubMed,
    not how much returned. Easily mistaken!
    """
    r = json.loads(_get("esearch.fcgi", {
        "db": "pubmed", "term": term, "retmode": "json", "retmax": 0
    })).get("esearchresult", {})
    if "ERROR" in r:
        raise ValueError(f"!! ERROR IN YOUR QUERIES !!: {r['ERROR']}")
    return int(r.get("count", 0)), r.get("querytranslation", "")


def get_pmids(term, retmax):
    r = json.loads(_get("esearch.fcgi", {
        "db": "pubmed", "term": term, "retmode": "json",
        "retmax": retmax, "sort": "pub_date"
    })).get("esearchresult", {})
    if "ERROR" in r:
        raise ValueError(f"!! ERROR IN YOUR QUERIES !!: {r['ERROR']}")
    return r.get("idlist", [])


def get_metadata(pmids, chunk=100):
    rows = []
    for i in range(0, len(pmids), chunk):
        batch = pmids[i:i + chunk]
        result = json.loads(_get("esummary.fcgi", {
            "db": "pubmed", "id": ",".join(batch), "retmode": "json"
        })).get("result", {})
        for uid in result.get("uids", []):
            it = result.get(uid, {})
            doi = next((a.get("value", "") for a in it.get("articleids", [])
                        if a.get("idtype") == "doi"), "")
            authors = [a.get("name", "") for a in (it.get("authors") or [])]
            rows.append({
                "pmid": uid,
                "title": it.get("title", ""),
                "journal": it.get("source", ""),
                "pubdate": it.get("pubdate", ""),
                "authors": "; ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
                "pubtype": "; ".join(it.get("pubtype") or []),
                "doi": doi,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
            })
        print(f"  list {min(i + chunk, len(pmids))}/{len(pmids)}")
    return rows


def get_abstracts(pmids, chunk=100):
    parts = []
    for i in range(0, len(pmids), chunk):
        parts.append(_get("efetch.fcgi", {
            "db": "pubmed", "id": ",".join(pmids[i:i + chunk]),
            "rettype": "abstract", "retmode": "text"
        }))
        print(f"  abstract {min(i + chunk, len(pmids))}/{len(pmids)}")
    return "\n\n".join(parts)


def main():
    today = date.today().isoformat()
    os.makedirs("literature/results", exist_ok=True)

    # 1. count the amount first
    print("Hits per block:")
    counts = {}
    for qid, term in QUERIES.items():
        n, _ = count_hits(term)
        counts[qid] = n
        print(f"  {qid}: {n:,}")

    total, translation = count_hits(FINAL_QUERY)
    counts[FINAL_ID] = total
    print(f"  {FINAL_ID}: {total:,}\n")

    print("PubMed actual queries:")
    print(f"  {translation}\n")
    print("Check this number with the PubMed site. Note it down if it's different.\n")

    if total == 0:
        print("Fetched 0, check the correctness of your queries.")
        print("(Full-width quotes? Unmatched brackets?)")
        return

    # 2. decide how many to fetch
    #    MAX_RECORDS = 0 means "all of them"
    want = total if not MAX_RECORDS else min(MAX_RECORDS, total)

    if want > ESEARCH_CAP:
        print(f"Hit {total:,}, but PubMed esearch only returns the first {ESEARCH_CAP:,}.")
        print("To get them all, split the query by date range (year by year),")
        print("or use EDirect. Capping at the limit for now.\n")
        want = ESEARCH_CAP
    elif want < total:
        print(f"Hit {total:,}, keeping the first {want:,} by publish date.")
        print("This is a SUBSET, not everything.\n")
    else:
        print(f"Hit {total:,}, fetching ALL of them.\n")

    # 3. fetch
    pmids = get_pmids(FINAL_QUERY, want)
    if not pmids:
        print("esearch returned no PMIDs. Nothing to write.")
        return
    rows = get_metadata(pmids)
    abstracts = get_abstracts(pmids)

    if not rows:
        print("esummary returned no records. Nothing to write.")
        return

    # 4. write files
    stem = f"literature/results/{today}_{FINAL_ID}"

    csv_path = f"{stem}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    txt_path = f"{stem}_abstracts.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(abstracts)

    log_path = "literature/search_log.md"
    new_log = not os.path.exists(log_path) or os.path.getsize(log_path) == 0
    with open(log_path, "a", encoding="utf-8") as f:
        if new_log:
            f.write("| date | version | number | actual queries | total hits | fetched | result file | comments |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
        q = FINAL_QUERY.replace("|", "\\|").replace("\n", " ")
        f.write(f"| {today} | {VERSION} | {FINAL_ID} | `{q}` | "
                f"{total} | {len(rows)} | {csv_path} | |\n")

    # 5. report
    words = len(abstracts.split())
    print(f"\n {csv_path} ({len(rows):,} records)")
    print(f" {txt_path} ({len(abstracts):,} characters / {words:,} words)"
          f" <- upload this to Gemini Notebook")
    if words > NOTEBOOK_WORD_LIMIT:
        over = words - NOTEBOOK_WORD_LIMIT
        print(f"   !! {words:,} words is {over:,} over Gemini Notebook's"
              f" {NOTEBOOK_WORD_LIMIT:,}-word per-source limit.")
        print(f"      Split the file, or lower MAX_RECORDS to about"
              f" {int(len(rows) * NOTEBOOK_WORD_LIMIT / words):,}.")
    print(f" {log_path} (one row added)")


if __name__ == "__main__":
    main()