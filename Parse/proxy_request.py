import requests
import random


def proxy_request(url, **kwargs):
    ip = ["8.219.97.248:80"]
    ip_addresses = ["159.197.250.171:3128", "193.104.189.68:3128", "157.100.12.138:999", "8.219.97.248:80"]

    try:
        # raise Exception
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        # self.logger.info("Request was made without proxies")
    except:
        # self.logger.info("Error. Looking for proxy....")
        while True:
            try:
                proxy = random.randint(0, len(ip_addresses) - 1)
                proxies = {"http": ip_addresses[proxy], "https": ip_addresses[proxy]}
                response = requests.get(url, proxies=proxies, timeout=5,
                                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                                        **kwargs)
                print(f"Proxy currently being used: {proxy}")
                break
            except:
                print("Error, looking for another proxy: ", proxy)
    return response