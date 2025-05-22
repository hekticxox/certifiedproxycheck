import requests
import time
from requests.exceptions import SSLError, ProxyError, ConnectTimeout
from urllib.parse import urlparse

def get_geo_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if res.status_code == 200:
            data = res.json()
            return f"{data.get('city', 'Unknown')}, {data.get('regionName', 'Unknown')}"
        else:
            return "Unknown, Unknown"
    except Exception:
        return "Unknown, Unknown"

def check_proxy_cert(proxy, protocol='socks5'):
    proxies = {
        'http': f'{protocol}://{proxy}',
        'https': f'{protocol}://{proxy}',
    }
    try:
        start = time.time()
        r = requests.get('https://www.google.com', proxies=proxies, timeout=7, verify=True)
        end = time.time()
        if r.status_code == 200:
            response_time = round((end - start) * 1000)  # ms
            ip = proxy.split(":")[0]
            location = get_geo_info(ip)
            return True, response_time, location
        else:
            return False, None, None
    except SSLError:
        print(f'[✗] {proxy} cert error')
    except (ProxyError, ConnectTimeout):
        print(f'[✗] {proxy} connection error')
    except Exception as e:
        print(f'[✗] {proxy} unknown error: {e}')
    return False, None, None

def main():
    proxy_file = input('Yo Chapta, drop the path to your proxy list file (.txt): ').strip()
    try:
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f'Nah Chapta, can’t find that file: {proxy_file}')
        return
    except Exception as e:
        print(f'Something went wrong opening that file: {e}')
        return
    
    good_proxies = []
    print(f'Checking {len(proxies)} proxies for cert errors...')
    for proxy in proxies:
        is_good, ping, location = check_proxy_cert(proxy)
        if is_good:
            print(f'[✓] {proxy} passed cert check | {ping} ms | {location}')
            good_proxies.append(f'{proxy} | {ping} ms | {location}')
    
    print(f'Done. {len(good_proxies)} proxies passed cert check.')
    save = input('Wanna save these clean proxies? (y/n): ').lower()
    if save == 'y':
        with open('clean_proxies.txt', 'w') as f:
            for p in good_proxies:
                f.write(p + '\n')
        print('Clean proxy list saved to clean_proxies.txt')

if __name__ == '__main__':
    main()
