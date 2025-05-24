#!/usr/bin/env python3
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import logging

# Optional: For Selenium fallback (dynamic JS sites)
USE_SELENIUM = False
if USE_SELENIUM:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

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
    "https://spys.one/en/socks-proxy-list/",
    "https://www.freeproxy.world/?type=socks5",
    "https://proxy-tools.com/proxy/socks",
    "https://proxy5.net/free-proxy",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://oxylabs.io/products/free-proxies",
    "https://www.webshare.io/features/free-proxy",
    "https://github.com/proxifly/free-proxy-list",
    "https://proxylib.com/proxies-by-types/socks5/",
    "https://www.proxysharp.com/proxies/socks5",
    "https://dicloak.com/",
]

# Logging setup
logging.basicConfig(
    filename="proxy_scraper.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def extract_proxies(text):
    # Fixed regex for matching IP:Port combos
    return re.findall(r'(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}', text)

def parse_spys_one(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        proxies = set()
        tables = soup.find_all('table')
        if len(tables) < 2:
            logging.warning("spys.one: No proxy table found.")
            return proxies
        rows = tables[1].find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if not cols:
                continue
            cell = cols[0]
            for tag in cell(['script', 'style']):
                tag.decompose()
            text = cell.get_text(strip=True)
            matches = extract_proxies(text)
            proxies.update(matches)
        return proxies
    except Exception as e:
        logging.error(f"spys.one failed: {e}")
        return set()

def parse_free_proxy_cz(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        proxies = set()
        table = soup.find('table', attrs={'id': 'proxy_list'})
        if not table:
            logging.warning("free-proxy.cz: No table found.")
            return proxies
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].get_text(strip=True)
                port = cols[1].get_text(strip=True)
                if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip) and port.isdigit():
                    proxies.add(f"{ip}:{port}")
        return proxies
    except Exception as e:
        logging.error(f"free-proxy.cz failed: {e}")
        return set()

def scrape_with_selenium(url):
    try:
        options = Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        sleep(5)
        text = driver.page_source
        driver.quit()
        return extract_proxies(text)
    except Exception as e:
        logging.error(f"Selenium failed for {url}: {e}")
        return set()

def scrape_all_proxies(sources):
    all_proxies = set()
    for url in sources:
        print(f"[~] Scraping: {url}")
        try:
            if "spys.one" in url:
                found = parse_spys_one(url)
            elif "free-proxy.cz" in url:
                found = parse_free_proxy_cz(url)
            else:
                r = requests.get(url, headers=headers, timeout=10)
                r.raise_for_status()
                content_type = r.headers.get("Content-Type", "")
                if "text/plain" in content_type:
                    text = r.text
                else:
                    soup = BeautifulSoup(r.content, "html.parser")
                    text = soup.get_text()
                found = extract_proxies(text)
                if not found and USE_SELENIUM:
                    found = scrape_with_selenium(url)
            if found:
                print(f"    [+] Found {len(found)} proxies")
                logging.info(f"{url} -> {len(found)} proxies found")
                all_proxies.update(found)
            else:
                print(f"    [-] No proxies found.")
                logging.warning(f"{url} returned 0 proxies")
        except requests.exceptions.HTTPError as e:
            print(f"[✗] HTTP error for {url}: {e}")
            logging.error(f"HTTPError for {url}: {e}")
        except Exception as e:
            print(f"[✗] Failed to scrape {url}: {e}")
            logging.error(f"General error for {url}: {e}")
    return sorted(all_proxies)

def main():
    proxies = scrape_all_proxies(proxy_sources)
    print(f"[✓] Total unique proxies found: {len(proxies)}")
    if proxies:
        filepath = input("Where should I save these proxies? Drop the full path (e.g., /home/user/proxies.txt): ").strip()
        try:
            with open(filepath, 'w') as f:
                for proxy in proxies:
                    f.write(proxy + '\n')
            print(f"[✓] Proxies saved to {filepath}")
        except Exception as e:
            print(f"[✗] Failed to save file: {e}")
            logging.error(f"File save error: {e}")
    else:
        print("[!] No proxies found to save.")

if __name__ == '__main__':
    main()
