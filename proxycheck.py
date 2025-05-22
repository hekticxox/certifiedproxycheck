import requests
from requests.exceptions import SSLError, ProxyError, ConnectTimeout

def check_proxy_cert(proxy, protocol='socks5'):
    proxies = {
        'http': f'{protocol}://{proxy}',
        'https': f'{protocol}://{proxy}',
    }
    try:
        # Hit a known HTTPS site with verify=True to force cert check
        r = requests.get('https://www.google.com', proxies=proxies, timeout=7, verify=True)
        if r.status_code == 200:
            return True
        else:
            return False
    except SSLError:
        print(f'[✗] {proxy} cert error')
        return False
    except (ProxyError, ConnectTimeout):
        print(f'[✗] {proxy} connection error')
        return False
    except Exception as e:
        print(f'[✗] {proxy} unknown error: {e}')
        return False

def main():
    # Ask the boss where the proxy list is
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
        if check_proxy_cert(proxy):
            print(f'[✓] {proxy} passed cert check')
            good_proxies.append(proxy)
        else:
            pass  # error already printed
    
    print(f'Done. {len(good_proxies)} proxies passed cert check.')
    save = input('Wanna save these clean proxies? (y/n): ').lower()
    if save == 'y':
        with open('clean_proxies.txt', 'w') as f:
            for p in good_proxies:
                f.write(p + '\n')
        print('Clean proxy list saved to clean_proxies.txt')

if __name__ == '__main__':
    main()

#ok at the end of this script i want it to list the state/city of the proxy and response rate
