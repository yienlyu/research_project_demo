# Literature Search Log

紀錄每次執行 `literature/search_strategy.md` 中檢索式的結果。檢索式原文照抄，不做任何修改。

「PubMed 回傳筆數」為 NCBI E-utilities（esearch, db=pubmed）回傳之真實總命中筆數（`<Count>`），非單次分頁筆數。

| 執行日期 | 策略版本號 | 檢索式編號 | 實際送出的檢索式 | PubMed 回傳筆數 |
| -------- | ---------- | ---------- | ---------------- | --------------- |
| 2026-09-29 | v1.0 | S1 | `("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab])` | 504,627 |
| 2026-09-29 | v1.0 | S2 | `("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab])` | 300,400 |
| 2026-09-29 | v1.0 | S3 | `("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab])` | 1,076,619 |
| 2026-09-29 | v1.0 | S4 | `("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab]) AND ("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab]) AND ("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab])` | 1,140 |
| 2026-10-02 | v2.0 | S4 | `(("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab])) AND (("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab])) AND (("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab]))` | 1141 | 200 | literature/results/2026-10-02_S4.csv | |
| 2026-10-02 | v2.0 | S4 | `(("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab])) AND (("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab])) AND (("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab]))` | 1141 | 200 | literature/results/2026-10-02_S4.csv | |
| 2026-10-02 | v1.0 | S1 | `("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab])` | 504,750 |
| 2026-10-02 | v1.0 | S2 | `("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab])` | 300,490 |
| 2026-10-02 | v1.0 | S3 | `("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab])` | 1,077,178 |
| 2026-10-02 | v1.0 | S4 | `("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab]) AND ("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab]) AND ("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab])` | 1,141 |
| 2026-10-03 | v2.0 | S4 | `(("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab])) AND (("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab])) AND (("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab]))` | 1141 | 200 | literature/results/2026-10-03_S4.csv | |
| 2026-10-03 | v1.0 | S1 | `("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab])` | 504,775 |
| 2026-10-03 | v1.0 | S2 | `("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab])` | 300,516 |
| 2026-10-03 | v1.0 | S3 | `("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab])` | 1,077,266 |
| 2026-10-03 | v1.0 | S4 | `("Cat Diseases"[MeSH] OR "Dog Diseases"[MeSH] OR cat[tiab] OR cats[tiab] OR feline*[tiab] OR dog[tiab] OR dogs[tiab] OR canine*[tiab]) AND ("Lymphoma"[MeSH] OR lymphoma*[tiab] OR lymphosarcoma*[tiab]) AND ("Antineoplastic Combined Chemotherapy Protocols"[MeSH] OR "Antineoplastic Agents"[MeSH] OR chemotherap*[tiab] OR "CHOP protocol"[tiab])` | 1,141 |
