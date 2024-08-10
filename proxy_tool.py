import requests
from rich import print
import threading
import time


working_proxies = []


def check(url, protocol, proxy):
    global working_proxies

    try:
        response = requests.get(url, proxies={protocol:proxy}, timeout=2)
        if response.status_code == 200:
            print(f"Proxy {proxy} works!  [{len(working_proxies)+1}]")
            working_proxies.append(proxy)
        else:
            print(f"Proxy {proxy} failed")
    except requests.RequestException as e:
        pass


def proxy_checker(proxies, url="https://www.wired.com/review/klipsch-flexus-core-200/"):
    proxies = proxies.text.split("\r\n")
    
    if url.startswith("https"):
        protocol = "https"
    else:
        protocol = "http"
    
    proxies.pop()
    
    i = 0
    for proxy in proxies:
        threading.Thread(target=check, args=(url, protocol,  proxy)).start()
        i += 1
        if i == 20:
            time.sleep(1.5)
            i = 0

    return working_proxies

def proxy_checker_(proxies, url="https://www.wired.com/review/klipsch-flexus-core-200/"):
    proxies = proxies.split("\r\n")

    if url.startswith("https"):
        protocol = "https"
    else:
        protocol = "http"

    proxies.pop()


    i = 0
    for proxy in proxies:
        threading.Thread(target=check, args=(url, protocol,  proxy)).start()
        i += 1
        if i == 20:
            time.sleep(1.5)
            i = 0

    return working_proxies

def get_proxy():
    global working_proxies

    try:
        f = open("found_proxies_http")
        f2 = open("found_proxies_https")
        res = f.read()
        res2 = f2.read()

        HTTP = proxy_checker_(res, "https://www.wired.com/review/klipsch-flexus-core-200/")
        working_proxies = []
        HTTPS = proxy_checker(res2)

        print(f"[green]Total Number Of HTTP PROXIES FOUND : {len(HTTP)} [/green]")
        print(f"[green]Total Number Of HTTPS PROXIES FOUND : {len(HTTPS)} [/green]")

        f2.close()
        f.close()

        f = open("found_proxies_http", "w")
        f2 = open("found_proxies_https", "w")
        f.write("\n".join(HTTP))
        f2.write("\n".join(HTTPS))
        f.close()
        f2.close()


    except:
        print("[red]  [-] Failed, Maybe Because Already Didn't Have A proxyList To Refresh[/red]")

def gen_new():
    global working_proxies
    print("We are generating a new proxy list so it would take time... \[this happens when you are using old proxylist/have none]")
    res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    res2= requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    HTTP = proxy_checker(res, "http://www.wired.com/review/klipsch-flexus-core-200/")
    working_proxies = []
    HTTPS = proxy_checker(res2)
        
    print(f"[green]Total Number Of HTTP PROXIES FOUND : {len(HTTP)} [/green]")        
    print(f"[green]Total Number Of HTTPS PROXIES FOUND : {len(HTTPS)} [/green]")
    
    f = open("found_proxies_http", "w")
    f2 = open("found_proxies_https", "w")
    f.write("\n".join(HTTP))
    f2.write("\n".join(HTTPS))
    f.close()
    f2.close()

print("[blue] This Tool Belonging To OpenCrawler Project Can \nHelp With Generating And Checking HTTP And HTTPS Proxy List![/blue]")
print("")
print("""[blue]
\t [1] - Refresh The ProxyList, Remove Proxies Which Doesn't Work.
\t [2] - Renew The ProxyList, Autogenerate A New ProxyList.
\t [3] - Show Count of the Proxies HTTP And HTTPS.
        [/blue]""")

t = input("[1,2,3] > ")
if t == "1":
    get_proxy()
elif t == "2":
    gen_new()
elif t == "3":
    try:
        f = open("found_proxies_http")
        f2 = open("found_proxies_https")
        res = f.read()
        res2 = f2.read()
        a = len(res.split('\r\n'))
        b = len(res2.split('\r\n'))
        print(f"[green]Total Number Of HTTP PROXIES FOUND : {a} [/green]")
        print(f"[green]Total Number Of HTTPS PROXIES FOUND : {b} [/green]")

        f2.close()
        f.close()
    except:
        print("[red]  [-] Failed, Maybe Because Already Didn't Have A proxyList[/red]")

else:
    print("[red]  [-] Unknown Command[/red]")


