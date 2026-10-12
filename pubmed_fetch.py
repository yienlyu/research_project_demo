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
EMAIL = "yienlyu@gmail.com"               # NCBI needs to know who you are
API_KEY = ""                              # optional, key speed: 3 req/s to 10
VERSION = "v2.0"                          # match the version search-strategy.md
MAX_RECORDS = 200                         # max record counts, not the total results number

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
    Return (fetched amount, actual queries in PubMed). 

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
    print("Fetched amount: ")
    counts = {}
    for qid, term in QUERIES.items():
        n, _ = count_hits(term)
        counts[qid] = n
        print(f"  {qid}: {n:,}")

    total, translation = count_hits(FINAL_QUERY)
    counts[FINAL_ID] = total
    print(f"  {FINAL_ID}: {total:,}\n")

    print("PubMed actual quries: ")
    print(f"  {translation}\n")
    print("Check this number with the PubMed site. Note it down if it's different. \n")

    if total == 0:
        print("Fetched 0, check the correctness of your quries.")
        return

    # Fetch data
    if total > MAX_RECORDS:
        print(f"Fetched {total:,}, keep the first {MAX_RECORDS} according to the publish date. This is a subset. \n")
    pmids = get_pmids(FINAL_QUERY, MAX_RECORDS)
    rows = get_metadata(pmids)
    abstracts = get_abstracts(pmids)

    # write files
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
            f.write("| date | version | number | actual quries | fetched amount | keeped amount | result file | comments |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
        q = FINAL_QUERY.replace("|", "\\|").replace("\n", " ")
        f.write(f"| {today} | {VERSION} | {FINAL_ID} | `{q}` | "
                f"{total} | {len(rows)} | {csv_path} | |\n")

    print(f"\n {csv_path} ({len(rows)}) records")
    print(f" {txt_path} ({len(abstracts):,} characters) <- upload this to Gemini Notebook")
    print(f" {log_path} added")


if __name__ == "__main__":
    main()