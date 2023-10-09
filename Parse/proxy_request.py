from uuid import uuid4
import requests
import random


def proxy_request(url, antiblock=False, **kwargs):
    ip = ["8.219.97.248:80"]
    ip_addresses = ["159.197.250.171:3128", "193.104.189.68:3128", "157.100.12.138:999", "8.219.97.248:80"]
    AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
        'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
        'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Mozilla/3.0',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3',
        'Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) Safari/419.3',
        'Opera/9.00 (Windows NT 5.1; U; en)'
    ]
    random_cookie = str(uuid4())
    if antiblock:
        agent = random.randint(0, len(AGENTS) - 1)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "de-DE,de;q=0.9",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "User-Agent": f"{AGENTS[agent]}",
            "localstorageAvailable:": "true",
            "X-Amzn-Trace-Id": "Root=1-6509d845-3fb55f98604690e258ea6c6c",
            "Cookie": "reese84={}".format(random_cookie)
        }
        response = requests.get(url, headers=headers)
        return response

    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Cookie": "reese84={}".format(random_cookie)
        }

    try:
        # raise Exception
        response = requests.get(url, headers=headers)
    except Exception as e:
        while True:
            try:
                proxy = random.randint(0, len(ip_addresses) - 1)
                proxies = {"http": ip_addresses[proxy], "https": ip_addresses[proxy]}
                response = requests.get(url, proxies=proxies, timeout=5,
                                        headers=headers,
                                        **kwargs)
                print(f"Proxy currently being used: {proxy}")
                break
            except:
                print("Error, looking for another proxy: ", proxy)
    return response
