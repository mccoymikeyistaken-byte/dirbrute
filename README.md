# 🔍 DirBrute

> A fast, smart, and actually-pretty web directory brute-forcer built in Python.  
> Because sometimes you just need to know what's hiding behind `/admin`.



```
  ██████╗ ██╗██████╗ ██████╗ ██╗   ██╗███████╗████████╗███████╗██████╗ 
  ██╔══██╗██║██╔══██╗██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
  ██║  ██║██║██████╔╝██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝
  ██║  ██║██║██╔══██╗██╔══██╗██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
  ██████╔╝██║██║  ██║██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║
  ╚═════╝ ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
```

---

## What is this?

DirBrute is a web directory brute-forcing tool — it takes a target URL and a wordlist, then hammers the server with requests to find hidden paths, files, and endpoints that aren't linked anywhere publicly.

Think of it as knocking on every door in a building to see which ones actually open.

It's smarter than just checking for `200 OK` though. It fingerprints the server's "not found" response first (status code, body length, word count, line count), then flags anything that *deviates* from that baseline — which means it catches soft 404s, redirect traps, and custom error pages that other tools miss.

---

## Features

- 🧠 **Baseline fingerprinting** — profiles the server's 404 behavior before scanning, not just status codes
- ⚡ **Multithreaded** — configurable thread count for fast scanning
- 🎨 **Clean terminal UI** — built with Rich, looks good in your screenshots
- ✅ **Input validation** — won't let you fat-finger a bad URL and waste 10 minutes
- 🔌 **Smart extension handling** — won't append `.php` to `backup.bak` (you'd be surprised how many tools do this)
- 💾 **Results saved to file** — with timestamps, so you can diff runs
- 🎛️ **Interactive wizard** — just run it, no flags to memorize

---

## Installation

**Clone the repo:**
```bash
git clone https://github.com/yourusername/dirbrute.git
cd dirbrute
```

**Install dependencies**:
```bash
pip install requests
```

That's it. No virtual environments, no Docker, no ritual sacrifice.

---

## Usage

```bash
python dirbrute.py
```

It'll walk you through everything:

```
  [?] Target URL : https://example.com
  [?] Threads [10] :
  [?] Wordlist [wordLists.txt] :
  [?] Output file [results.txt] :
  [?] Extensions [php,html,txt...] :
  [?] Verbose [y/N] : n
```

Hit Enter to accept defaults. The only required field is the target URL.

---

## Options


| Field | Description | Default |

| `Target URL` | Full URL with scheme. Required. | - |

| `Threads` | Concurrent requests. Higher = faster, don't overdo it. | `10` |

| `Wordlist` | Path to wordlist file. Must exist on disk. | `wordLists.txt` |

| `Output` | File to save results. Wiped clean each run. | `results.txt` |

| `Extensions` | Comma-separated, no dots. Smart extension handling. | `php,html,txt...` |

| `Verbose` | Print every attempt. Noisy but useful for debugging. | `n` |

---

## How it works

Most tools just check if the response is `200 OK`. That's naive — plenty of servers return `200` for pages that don't exist (looking at you, SPAs), and plenty of real pages return `301` or `500`.

DirBrute does this instead:

1. **Baseline request** — hits a guaranteed-junk URL (`/randomjunk-xyz`) and records the response signature: status code, body length, word count, line count.
2. **Scan** — for each path in the wordlist, it fires a request and compares the response against the baseline.
3. **Flag deviations** — if *any* of those four metrics differs meaningfully from baseline, it's reported as a potential find.

This catches things like:
- Custom 404 pages that return `200` (soft 404s)
- Login redirects (`302` to `/login`)
- Endpoints that exist but throw errors (`500`)
- Directories that redirect to themselves with a trailing slash (`301`)

---

## Example output

```
  [*] Baseline fingerprint:
      Status : 404  │  Length : 152  │  Words : 12  │  Lines : 8

  [FOUND]  /admin         [301 │ 0B    │ 0w   │ 0L  → /admin/]
  [FOUND]  /login.php     [200 │ 4312B │ 312w │ 91L → —]
  [FOUND]  /config.json   [200 │ 843B  │ 42w  │ 31L → —]
  [FOUND]  /backup.zip    [200 │ 98432B│ 0w   │ 0L  → —]
```

---

## Wordlist

A default wordlist (`wordLists.txt`) is included with common paths. It already includes extensions on some entries (like `/backup.bak`, `/config.json`) — DirBrute is smart enough not to double-append extensions to those.

For bigger wordlists, [SecLists](https://github.com/danielmiessler/SecLists) is the go-to. The `Discovery/Web-Content/` directory has everything from small focused lists to the nuclear option.

---

## ⚠️ Legal stuff (read this, seriously)

This tool is for **authorized security testing only**.

Only use it on:
- Systems you own
- Systems you have **explicit written permission** to test
- Intentionally vulnerable practice targets (OWASP Juice Shop, DVWA, HackTheBox, TryHackMe, etc.)

Scanning systems without permission is illegal in most countries. Don't be that person. The tool works great on Juice Shop — go use that.

---

## Tested on

- OWASP Juice Shop ✅
- Kali Linux (Python 3.11) ✅

---

## Contributing

Found a bug? Have a feature idea? Open an issue or send a PR. Clean code, clear commit messages, and you're in.

---

## Author

Built by **mike**

---

*Happy hunting. Stay legal.* 🎯