# Useful Commands

## Clone the Repo to Your Computer

```
git clone https://github.com/yienlyu/research_project_demo.git
cd research_project_demo
```

and it would look like:

```
├── abstract-CatDogDisease-set-1012.txt   <- saved from PubMed site, can send it to Gemini Notebook
├── add_search_strategy
├── csv-CatDogDisease-set-1012.csv        <- saved from PubMed site, same list
├── demo.py                               <- only fetch amount/numbers
├── global_setup_claude_json
├── literature/
│   ├── results/
│   │   ├── 2026-10-13_S4_abstract.txt    <- saved from pubmed_fetch.py
│   │   └── 2026-10-13_S4.csv             <- saved from pubmed_fetch.py
│   ├── search_log.md
│   └── search_strategy.md
├── pubmed_fetch.py                       <- return: csv, txt, log
└── README.md
```

## Update to Latest Version

```
git pull
```

## Terminal Basics

| Action                 | MacOS / Linux       | Windows (Powershell) |
| ---------------------- | ------------------- | -------------------- |
| Where am I? (The Path) | `pwd`               | `pwd`                |
| What's in here?        | `ls`                | `ls`                 |
| Create a folder        | `mkdir folder_name` | `mkdir folder_name`  |
| Go into a folder       | `cd folder_name`    | `cd folder_name`     |
| Go up one level        | `cd ..`             | `cd ..`              |
| Create a file          | `touch file_name`   | `New-Item file_name` |

## Open Your Terminal

- macOS: Spotlight(⌘ + 空白)打 Terminal
- Windows: 開始列打 PowerShell

## Check Python (has to be 3.12)

```
python3 --version     # macOS / Linux
python --version      # Windows
```

If you do not have Python installed: python.org/downloads
(Reminder: Windows users must check "Add Python to PATH")

## Run the Scripts

### demo.py

```
python demo.py
```

Only returns:

```
total fetch:  1387
actual queries:  "cat diseases"[MeSH Terms] OR ...
```

Will not produce any files or log!

### pubmed_fetch.py

```
python pubmed_fetch.py
```

Then produce 3 things:

```
literature/search_log.md                        # add a row of content
literature/results/2026-10-13_S4.csv            # literature list (for management)
literature/results/2026-10-13_S4_abstracts.txt  # full abstract (for reading)
```

#### !!MUST CHANGE!!

```
EMAIL = "your_email@example.com"   # NCBI needs to know who you are
API_KEY = ""                       # can keep it empty
VERSION = "v2.0"                   # for the version of your search_strategy.md
MAX_RECORDS = 200                  # the record cap, not the total fetch
```

## Install Node.js

```
# macOS
brew install node

# Windows
winget install OpenJS.NodeJS.LTS

# Linux (Debian / Ubuntu)
sudo apt install nodejs npm
```

### Check the Version (v20.x or v22.x)

```
node -v
npx -v
```

## Test the PubMed MCP Server

```
npx -y @ncukondo/mcp-server-pubmed --email your_email@example.com
```

no ERROR, and stay at pending stage means SUCCESS!
Press `Ctrl + C` to exit the test

## Write the Global Config by Yourself

Remember to change the email address!

There is already a file `global_setup_claude_json` in repo, but if you want to do it all by yourself:

```
python3 -c '
import json, os

path = os.path.expanduser("~/.claude.json")
try:
    with open(path, "r") as f:
        data = json.load(f)
except Exception:
    data = {}

if "mcpServers" not in data:
    data["mcpServers"] = {}

data["mcpServers"]["pubmed"] = {
    "command": "npx",
    "args": [
        "-y",
        "@ncukondo/mcp-server-pubmed",
        "--email",
        "your_email@example.com"
    ]
}

with open(path, "w") as f:
    json.dump(data, f, indent=2)
'
```

> Windows users please change python3 to python

## Verify the Connection

```
cd ~/your_workspace/your_project/
claude
> /mcp
```

## Gemini Notebook MCP

### Install and Login

```
uv tool install --python 3.12 notebooklm-mcp-cli
nlm login --storage protected
nlm doctor
```

No `uv`? Install first: docs.astral.sh/uv

### Onto Claude Code

```
nlm setup add claude-code
claude mcp list
```

### Do What Your Want!

```
cd ~/your_workspace/your_project/

nlm notebook create "Cat & Dog Lymphoma"
nlm alias set lymphoma <notebook-id>
nlm source add lymphoma --file abstract-CatDogDisease-set-1012.txt --wait
nlm notebook query lymphoma "Which of these sources are studies about cats?"
```

### Ways to Call Gemini Notebook (After Entering `claude`)

```
! nlm notebook query lymphoma "..."
執行 nlm notebook query ...
用 Gemini Notebook 問 notebook <name/notebook-id>: ...
```

### Claude Code SKILL

save to: `~/.claude/skills/search-log/SKILL.md`

```
---
name: search-log
description: 讀取 literature/search_strategy.md,並使用 PubMed MCP 依序執行 S1 到 S4 的檢索式。使用者說「search pubmed」「search and log」「queries」時使用。
---

嚴格遵守以下規則:

1.【禁止改動】請原封不動送出策略檔中的檢索式,不要擅自優化、增加同義詞或增刪括號。

2.【紀錄 Log】每一條檢索式執行完畢後,將「執行日期」、「策略版本號」、「檢索式編號」、
   「實際送出的檢索式」與「PubMed 回傳筆數」追加記錄至 literature/search_log.md。
   並與 PubMed 網頁的數字核對,不一致請在備註欄註明。

3.【匯出結果檔】請將最終組合檢索式(S4)的所有搜尋結果(包含 PMID、Title、Journal、
   PubYear、Authors、Abstract)儲存為 CSV 檔,
   路徑為:literature/results/<今天日期年月日>_S4.csv
```
