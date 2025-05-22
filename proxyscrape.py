import re
import requests
from bs4 import BeautifulSoup

proxy_sources = [
    "https://proxyscrape.com/free-proxy-list/united-states",
    "https://sockslist.us/",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt",
    "http://free-proxy.cz/en/proxylist/country/US/socks5/ping/all",
    "https://proxycompass.com/free-proxies/north-america/united-states/",
    "https://fineproxy.org/free-proxies/north-america/united-states/",
    "https://www.proxysharp.com/proxies/socks5/us",
    "https://proxyfreeonly.com/free-proxy-list/united-states",
    "https://proxylib.com/free-proxy-list/us/",
]

def extract_proxies(text):
    # Match IP:PORT pattern
    return re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b', text)

def scrape_all_proxies(sources):
    proxies = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    for url in sources:
        try:
            print(f"[~] Scraping: {url}")
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()

            if "text/plain" in r.headers.get("Content-Type", ""):
                text = r.text
            else:
                soup = BeautifulSoup(r.content, "lxml")
                text = soup.get_text()
            
            found = extract_proxies(text)
            print(f"    [+] Found {len(found)} proxies")
            proxies.update(found)
        except Exception as e:
            print(f"[✗] Failed to scrape {url}: {e}")
    return sorted(proxies)

def main():
    all_proxies = scrape_all_proxies(proxy_sources)
    print(f"\n[✓] Total unique proxies found: {len(all_proxies)}")

    if all_proxies:
        filepath = input("\nWhere should I save these proxies? Drop the full path (e.g., /home/user/proxies.txt): ").strip()
        try:
            with open(filepath, 'w') as f:
                for proxy in all_proxies:
                    f.write(proxy + '\n')
            print(f"[✓] Proxies saved to {filepath}")
        except Exception as e:
            print(f"[✗] Failed to save file: {e}")
    else:
        print("[!] No proxies found to save.")

if __name__ == '__main__':
    main()
