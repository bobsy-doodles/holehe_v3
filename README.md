```
◈  HOLEHE  V2  —  EMAIL  INTELLIGENCE
```

Check if an email is registered across platforms. Fast. Async. Modular.



![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)




![Linux](https://img.shields.io/badge/Linux-Compatible-yellow?style=for-the-badge&logo=linux&logoColor=black)




![License](https://img.shields.io/badge/Open%20Source-MIT-green?style=for-the-badge&logo=open-source-initiative&logoColor=white)




![OSINT](https://img.shields.io/badge/OSINT-Tool-red?style=for-the-badge&logo=searchengin&logoColor=white)




![PyPI](https://img.shields.io/pypi/v/holehe-v2?style=for-the-badge&logo=pypi&logoColor=white)



---

## Installation 🛠️

**Via PyPI (recommended)**
```bash
pip install holehe-v2
```

**On Termux**
```bash
pip install holehe-v2 --break-system-packages
```

**From source**
```bash
git clone https://github.com/anubhavanonymous/holehe_v2
cd holehe_v2
pip install -r requirements.txt
```

---

## Running 🚀

```bash
python -m holehe_v2 target@email.com
```

---

## 💠 Features

### 📡 Email Existence Check

Submit any email. holehe_v2 fires async requests across all registered modules simultaneously and returns:

- **[+]** — account found on the platform
- **[-]** — no account registered
- **[!]** — error — rate limited, WAF blocked, or unexpected response

### ⚡ Async Architecture

All checkers run concurrently via `httpx.AsyncClient`. No waiting on one platform while another finishes. Full coverage in a single pass. Default concurrency is 50 — tunable via `-c`.

### 🧩 Modular Design

Each platform is a self-contained module. Drop a new `.py` file into `holehe_v2/modules/` — it registers automatically. No config edits, no runner changes.

### 🌐 Platform Coverage

| Module | Method | Signal |
|---|---|---|
| `office365` | GET — Autodiscover API | HTTP 200 / 404 |
| `gaana` | POST — JSSO IndiaTimes | `VERIFIED_EMAIL` / `UNREGISTERED_EMAIL` |
| `indiatimes` | POST — JSSO IndiaTimes | `VERIFIED_EMAIL` / `UNREGISTERED_EMAIL` |
| `naukri` | HEAD — CloudGateway API | HTTP 200 / 404 |
| `jeevansathi` | GET — Profile Exists API | `isUserExists` bool |
| `gravatar` | GET — Avatar hash lookup | HTTP 200 / 404 + profile scrape |
| `stackb` | POST — Livewire login check | Error string diff |

### 🪪 Rich Profile Extraction (Gravatar)

When a Gravatar account is found, holehe_v2 goes deeper:

- Display name, username, bio, location, job title, company
- Verified linked accounts (GitHub, Twitter, etc.)
- Public emails, phone numbers, crypto addresses
- Profile photos, background image
- Interests, timezone, account creation date

---

## Flags & Usage 🚩

### Basic scan

```bash
python -m holehe_v2 target@email.com
```

Runs all modules against the target. Shows found, not found, and errors.

---

### `--only-used` — found accounts only

```bash
python -m holehe_v2 target@email.com --only-used
```

Suppresses `[-]` not-found lines. Clean output — only platforms where the email is registered.

---

### `--show-errors` — expose error detail

```bash
python -m holehe_v2 target@email.com --show-errors
```

By default `[!]` entries are silent. This flag prints the reason next to each — WAF block, timeout, unexpected response body, etc. Useful when a module isn't behaving as expected.

---

### `--json FILE` — export to JSON

```bash
python -m holehe_v2 target@email.com --json results.json
```

Exports full results to a JSON file. Includes status, platform, URL, and any enriched profile data (Gravatar, etc.).

---

### `--csv FILE` — export to CSV

```bash
python -m holehe_v2 target@email.com --csv results.csv
```

Exports results as a flat CSV. One row per module — platform, status, URL.

---

### `--json` + `--csv` together

```bash
python -m holehe_v2 target@email.com --json results.json --csv results.csv
```

Both exports run simultaneously. Same scan, two output formats.

---

### `-m / --module NAME` — single module scan

```bash
python -m holehe_v2 target@email.com -m gravatar
python -m holehe_v2 target@email.com -m naukri
python -m holehe_v2 target@email.com -m office365
```

Runs one module only. Use for quick checks or when debugging a specific platform. Module name matches the filename without `.py`.

---

### `--proxy URL` — route through a proxy

```bash
python -m holehe_v2 target@email.com --proxy http://127.0.0.1:8080
python -m holehe_v2 target@email.com --proxy socks5://127.0.0.1:9050
```

Routes all requests through the specified proxy. Supports HTTP and SOCKS5. Useful for anonymity or bypassing regional blocks.

---

### `-c / --concurrency N` — control request concurrency

```bash
python -m holehe_v2 target@email.com -c 10
python -m holehe_v2 target@email.com -c 100
```

Sets the maximum number of simultaneous requests. Default is `50`. Lower it on slow connections or if platforms are rate limiting you. Raise it for speed on fast networks.

---

### `--no-colour` — disable coloured output

```bash
python -m holehe_v2 target@email.com --no-colour
```

Strips ANSI colour codes from output. Use when piping results to a file or running in a terminal that doesn't support colour.

---

### Combined example

```bash
python -m holehe_v2 target@email.com --only-used --json out.json --proxy socks5://127.0.0.1:9050 -c 20
```

Only-found results, exported to JSON, routed through Tor, 20 concurrent requests.

---

## Adding a Module 🔧

```python
# holehe_v2/modules/yourplatform.py
import httpx
from holehe_v2.core.result import Result

async def _check(email: str) -> Result:
    # your logic here
    ...

async def validate_yourplatform(email: str) -> Result:
    return await _check(email)
```

The runner picks up any file with a `validate_*` function automatically. No registration required.

---

## Project Structure 📁

```
holehe_v2/
├── pyproject.toml
├── README.md
├── LICENSE
├── requirements.txt
└── holehe_v2/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── result.py
    │   └── helpers.py
    └── modules/
        ├── __init__.py
        ├── office365.py
        ├── gaana.py
        ├── indiatimes.py
        ├── naukri.py
        ├── jeevansathi.py
        ├── gravatar.py
        └── stackb.py
```

---

## Troubleshooting 💡

| Problem | Fix |
|---|---|
| All results show `[!]` | Try `--show-errors` to see the actual reason per module |
| Rate limited immediately | Lower concurrency with `-c 10` or route through `--proxy` |
| Module not picked up | Confirm the file has a `validate_*` function and is inside `modules/` |
| Colour codes in piped output | Add `--no-colour` |
| Termux install fails | Use `pip install holehe-v2 --break-system-packages` |

---

## Disclaimer ⚠️

This tool is for **authorized security research and OSINT investigations only**.

- Only queries public-facing registration APIs
- Does not bypass authentication or access private data
- Users are responsible for compliance with applicable laws
- Author assumes no liability for misuse

---

## Author 👤

**Anubhav Kashyap**

Telegram / GitHub: [@anubhavanonymous](https://t.me/anubhavanonymous)
