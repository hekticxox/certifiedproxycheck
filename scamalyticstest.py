import requests
import random
import re
import json
import sys

def check_ip(ip, user_agents_list):
    user_agent = random.choice(user_agents_list)
    url = f"https://scamalytics.com/ip/{ip}"

    headers = {
        "User-Agent": user_agent,
        "Host": "scamalytics.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"Failed to get response from the server: {e}")
        return None

    if response.status_code != 200:
        print(f"Can't check IP {ip} - Response code: {response.status_code}")
        return None

    print(f"Checking IP {ip}")

    pattern = re.compile(r"(?s)<pre[^>]*>(.*?)<\/pre>")
    matches = pattern.search(response.text)
    if not matches:
        print("Failed to find pattern in the response body")
        return None

    raw_data = matches.group(1)

    raw_data = raw_data.replace("...", "")
    raw_data = raw_data.replace("false,", "false")
    raw_data = raw_data.replace("true,", "true")

    raw_data = "{" + raw_data + "}"

    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        return None

    return data

def main():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        # add more user agents if you want
    ]

    file_path = input("Yo Chapta, drop the path to your IP:PORT text file: ").strip()

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Can't open file: {e}")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Split IP and port, ignore port
        if ":" in line:
            ip = line.split(":")[0]
        else:
            ip = line

        result = check_ip(ip, user_agents)
        if result:
            print(json.dumps(result, indent=4))
        else:
            print(f"Failed to get data for IP {ip}")

if __name__ == "__main__":
    main()
