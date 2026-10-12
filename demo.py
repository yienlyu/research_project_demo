import json, urllib.parse, urllib.request

EMAIL = "your_email@example.com"
TERM = '("Cat Diseases"[MeSH Terms] OR "Dog Diseases"[MeSH Terms] OR "cat"[Title/Abstract] OR "cats"[Title/Abstract] OR "feline*"[Title/Abstract] OR "dog"[Title/Abstract] OR "dogs"[Title/Abstract] OR "canine*"[Title/Abstract]) AND ("Lymphoma"[MeSH Terms] OR "lymphoma*"[Title/Abstract] OR "lymphosarcoma*"[Title/Abstract]) AND ("Antineoplastic Combined Chemotherapy Protocols"[MeSH Terms] OR "Antineoplastic Agents"[MeSH Terms] OR "chemotherap*"[Title/Abstract] OR "CHOP protocol"[Title/Abstract])'

p = urllib.parse.urlencode({"db": "pubmed", "term": TERM, "retmode": "json",
                            "retmax": 0, "tool": "demo", "email": EMAIL})
url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + p

with urllib.request.urlopen(url) as r:
    d = json.load(r)["esearchresult"]

print("total fetch: ", d["count"])
print("actual quries: ", d["querytranslation"])