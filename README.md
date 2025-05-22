# 🔐 certifiedproxycheck

Check a list of SOCKS5/HTTP proxies from a `.txt` file and verify which ones pass SSL certificate validation. It also pulls the city, state, and response time of every working proxy. Includes a scraper tool to auto-grab free SOCKS5 proxies from multiple public sources.

Perfect for filtering out garbage and rollin’ only with clean, certified proxies that don’t throw errors.

---

## 🚀 Features

- ✅ SSL cert check via HTTPS request
- 🏙️ City + state/region lookup of working proxies
- ⚡ Response time logging in milliseconds
- 📄 Saves results in `clean_proxies_detailed.txt`
- 🌐 `proxyscrape.py` scrapes SOCKS5 proxy IPs automatically
- ☑️ Supports both `http` and `socks5` proxies

---

## 📦 Requirements

- Python 3.x
- Modules:
  - `requests`
  - `beautifulsoup4`
  - `lxml`

Install with:

```bash
pip install requests beautifulsoup4 lxml
```

If you're using Parrot OS or any restricted Debian system, create a venv like this:

```bash
sudo apt install python3-venv
python3 -m venv proxyvenv
source proxyvenv/bin/activate
pip install requests beautifulsoup4 lxml
```

---

## 📂 Usage

### ➤ 1. `proxycheck.py`

Make a `.txt` file with proxies (one per line):

```
111.222.333.444:1080
55.66.77.88:8080
```

Run the script:

```bash
python3 proxycheck.py
```

When prompted, drop in the path to your proxy list file. Working proxies will get geo info + ping logged.

✅ Sample Output:

```
[✓] 45.133.1.90:1080 | Atlanta, Georgia | 212.34 ms
[✓] 103.204.100.25:8080 | Berlin, Berlin | 324.12 ms

Done. 2 proxies passed cert check.
Clean proxy list saved to clean_proxies_detailed.txt
```

---

### ➤ 2. `proxyscrape.py`

This script scrapes public SOCKS5 proxies from:

- proxyscrape.com
- sockslist.us
- jsdelivr GH dumps
- free-proxy.cz
- proxycompass.com
- fineproxy.org
- proxysharp.com
- proxyfreeonly.com
- proxylib.com

Run it like this:

```bash
python3 proxyscrape.py
```

You'll be asked where you wanna save the scraped proxy list. It'll auto-dump IP:PORT format ready to use in `proxycheck.py`.

---

## 🔧 Future Enhancements

- [ ] Proxy auth (`user:pass@ip:port`)
- [ ] Auto protocol detection
- [ ] CSV / JSON export
- [ ] Threading for speed

---

## 👑 Author

**Chapta** aka [@hekticxox](https://github.com/hekticxox)  
Pentest sharp. Proxy clean. Calgary cold. ❄️

> “Only the clean proxies get through. Rest get tossed.” – *Chapta 🧊*
