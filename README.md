# 🔐 certifiedproxycheck

Check a list of SOCKS5/HTTP proxies from a `.txt` file and verify which ones pass SSL certificate validation. It also pulls the **city**, **state**, and **response time** of every working proxy.

Perfect for filtering out garbage and rollin’ only with clean, certified proxies that don’t throw errors.

## 🚀 Features

- ✅ SSL cert check via HTTPS request  
- 🏙️ City + state/region lookup of working proxies  
- ⚡ Response time logging in milliseconds  
- 📄 Saves results in `clean_proxies_detailed.txt`  
- Supports `http` and `socks5` proxies

## 📦 Requirements

- Python 3.x  
- `requests` module

```bash
pip install requests
```

## 📂 Usage

1. Create a `.txt` file with proxies, one per line:
   ```
   111.222.333.444:1080
   55.66.77.88:8080
   ```

2. Run the script:

```bash
python3 proxycheck.py
```

3. When prompted, enter the path to your proxy list file.

4. If any pass, you’ll be asked if you wanna save the good ones with their cert status, geo info, and ping time.

### ✅ Sample Output

```
[✓] 45.133.1.90:1080 | Atlanta, Georgia | 212.34 ms
[✓] 103.204.100.25:8080 | Berlin, Berlin | 324.12 ms

Done. 2 proxies passed cert check.
Clean proxy list saved to clean_proxies_detailed.txt
```

## 🔧 Future Enhancements

- Proxy auth (user:pass@ip:port)  
- Auto protocol detection  
- CSV / JSON export  
- Threading for speed

## 👑 Author

**Chapta aka @hekticxox**  
Pentest sharp. Proxy clean. Calgary cold.  
GitHub: [hekticxox](https://github.com/hekticxox)

---

> “Only the clean proxies get through. Rest get tossed.” – Chapta 🧊
