"""
Open Crawler 0.0.1

License - MIT ,
An open source crawler/spider

Features :
    - Easy install
    - Related-CLI Tools (includes ,CLI access to tool, not that good search-tool xD, etc)
    - Memory efficient [ig]
    - Pool Crawling - Use multiple crawlers at same time
    - Supports Robot.txt
    - MongoDB [DB]
    - Language Detection
    - 18 + Checks / Offensive Content Check
    - Proxies
    - Multi Threading
    - Url Scanning
    - Keyword, Desc And recurring words Logging

    
Author - Merwin M
"""





from memory_profiler import profile
from collections import Counter
from functools import lru_cache
from bs4 import BeautifulSoup
from langdetect import detect
from mongo_db import *
from rich import print
import urllib.robotparser
import threading
import requests
import signal
import atexit
import random
import json
import time
import sys
import re
import os





"""
######### Crawled Info are stored in Mongo DB as #####
Crawled sites = [ 

                {
                    "website" : "<website>"
                    
                    "time" : "<last_crawled_in_epoch_time>",

                    "mal" : Val/None, # malicious or not
                    "offn" : Val/None, # 18 +/ Offensive language

                    "ln" : "<language>",
                    
                    "keys" : [<meta-keywords>],
                    "desc" : "<meta-desc>",
                    
                    "recc" : [<recurring words>]/None,
                }
]
"""




## Regex patterns
html_pattern = re.compile(r'<[^>]+>')
url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
url_pattern_0 = "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
url_extract_pattern_0 = "[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"



# Config File
config_file = "config.json"



# Load configs from config_file - > json
try:
    config_file = open(config_file, "r")
    configs = json.loads(config_file.read())
    config_file.close()

except:
    os.system("python3 config.py") # Re-configures

    config_file = open(config_file, "r")
    configs = json.loads(config_file.read())
    config_file.close()





## Setting Up Configs
MONGODB_PWD =  configs["MONGODB_PWD"]
MONGODB_URI = configs["MONGODB_URI"]
TIMEOUT = configs["TIMEOUT"] # Timeout for reqs
MAX_THREADS = configs["MAX_THREADS"] 
bad_words = configs["bad_words"]
USE_PROXIES = configs["USE_PROXIES"]
Scan_Bad_Words = configs["Scan_Bad_Words"]
Scan_Top_Keywords = configs["Scan_Top_Keywords"]
URL_SCAN = configs["URL_SCAN"]
urlscan_key = configs["urlscan_key"]


del configs



## Main Vars
EXIT_FLAG = False
DB = None
ROBOT_SCANS = [] # On Going robot scans
WEBSITE_SCANS = [] # On Going website scans



# Loads bad words / flaged words
file = open(bad_words, "r")
bad_words = file.read()
file.close()
bad_words = tuple(bad_words.split("\n"))





# @lru_cache(maxsize=100)
# def get_robot(domain):
#     """
#     reads robots.txt
#     """

#     print(f"[green]  [+] Scans - {domain} for restrictions")
    
#     rp = urllib.robotparser.RobotFileParser()
#     rp.set_url("http://" + domain + "/robots.txt")

#     return rp.can_fetch


    

def get_top_reccuring(txt):
    """
    Gets most reccuring 8 terms from the website html
    txt : str
    returns : list
    """

    split_it = txt.split()
    counter = Counter(split_it)
    try:
        most_occur = counter.most_common(8)
        return most_occur
    except:
        return []



def lang_d(txt):
    """
    Scans for bad words/ flaged words. 
    txt : str
    return : int - > score 
    """

    if not Scan_Bad_Words:
        return None
    score = 0

    for e in bad_words:
        try:
            x = txt.split(e)
        except:
            continue
        score += len(x)-1
    
    try:
        score = round(score/len(txt))
    except:
        pass
     
    return score


def get_proxy():
    """
    Gets a free proxy from 'proxyscrape'
    returns :  dict - > {"http": "<proxy ip:port>"}
    """

    res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    return {"http" : random.choice(res.text.split("\r\n"))}



def scan_url(url):
    """
    Scans url for malicious stuff , Uses the Urlscan API 
    url : str
    return : int - > score
    """

    headers = {'API-Key':urlscan_key,'Content-Type':'application/json'}
    data = {"url": url, "visibility": "public"}
    r = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data)) 
    print(r.json()) 
    r = "https://urlscan.io/api/v1/result/" + r.json()["uuid"]
    
    for e in range(0,100):
        time.sleep(2)
        res = requests.get(r, headers) 
        res = res.json()
        try:
            if res["status"] == 404:
                pass
        except:
            print(res["verdicts"])
            return res["verdicts"]["urlscan"]["score"]
    
    return None



def remove_html(string):
    """
    removes html tags 
    string : str
    return : str
    """

    return html_pattern.sub('', string)



def handler(SignalNumber, Frame): # for handling SIGINT
    safe_exit()

signal.signal(signal.SIGINT, handler) # register handler



def safe_exit(): # safely exits the program
    global EXIT_FLAG

    print(f"\n\n[blue]  [\] Exit Triggered At : {time.time()} [/blue]")
    
    EXIT_FLAG = True
    
    print("[red] EXITED [/red]")
    


atexit.register(safe_exit) # registers at exit handler



def forced_crawl(website):
    """
    Crawl a website forcefully - ignorring the crawl wait list
    website : string
    """

    # Checks if crawled already , y__ = crawled or not , True/False
    z__ = if_crawled(website) 
    y__ = z__[0]

    mal = None
    lang_18 = None

    lang = None
    
    # Current thread no. as there is no separate threads for crawling, set as 0
    th = 0 

    print(f"[green]  [+] Started Crawling : {website} | Thread : {th}[/green]")


    proxies = {}

    if USE_PROXIES:
        proxies = get_proxy()

    try:
        website_req = requests.get(website, headers = {"user-agent":"open crawler v 0.0.1"}, proxies =  proxies, timeout = TIMEOUT)
        
        # checks if content is html or skips
        try:
            if not "html" in website_req.headers["Content-Type"]:
                print(f"[green]  [+] Skiped : {website} Because Content type not 'html' | Thread : {th}[/green]")
                return 0
        except:
            return 0           
        

        website_txt = website_req.text

        if not y__:
            save_crawl(website, time.time(), 0,0,0,0,0,0,)
        else:
            update_crawl(website, time.time(), 0,0,0,0,0,0)

    except: 
        # could be because website is down or the timeout 
        print(f"[red]  [-] Coundn't Crwal : {website} | Thread : {th}[/red]")
        if not y__:
            save_crawl(website, time.time(), "ERROR OCCURED", 0, 0, 0, 0, 0)
        else:
            update_crawl(website, time.time(), "ERROR OCCURED", 0, 0, 0, 0, 0)
        return 0

    try:
        lang = detect(website_txt)
    except:
        lang = "un-dic"

    if URL_SCAN:
        mal = scan_url(website)
    
    website_txt_ = remove_html(website_txt)
    
    if Scan_Bad_Words:
        lang_18 = lang_d(website_txt_)

    keywords = []
    desc = ""
    
    soup = BeautifulSoup(website_txt, 'html.parser')
    
    for meta in soup.findAll("meta"):
        try:
            if meta["name"] == "keywords":
                keywords = meta["content"]
        except:
            pass
        
        try:
            if meta["name"] == "description":
                desc = meta["content"]
        except:
            pass


    del soup
    
    top_r = None

    if  Scan_Top_Keywords:
        top_r = get_top_reccuring(website_txt_)

    update_crawl(website, time.time(), mal, lang_18, lang, keywords, desc, top_r)

    del mal, lang_18, lang, keywords, desc, top_r

    sub_urls = []
    
    for x in re.findall(url_extract_pattern, website_txt):
        if re.match(url_pattern, x):
            if ".onion" in x: 
                # skips onion sites
                continue

            if x[-1] == "/"  or x.endswith(".html") or x.split("/")[-1].isalnum(): 
                # tries to filture out not crawlable urls
                sub_urls.append(x)

    # removes all duplicates
    sub_urls = set(sub_urls) 
    sub_urls = list(sub_urls)
            

    # check for restrictions in robots.txt and filture out the urls found
    for sub_url in sub_urls:

        if if_waiting(sub_url):
            sub_urls.remove(sub_url)

            continue

        # restricted = robots_txt.disallowed(sub_url, proxies)


        # t = sub_url.split("://")[1].split("/")
        # t.remove(t[0])

        # t_ = ""
        # for u in t:
        #     t_ += "/" +  u

        # t = t_

        # restricted = tuple(restricted)

        # for resk in restricted:
        #     if t.startswith(resk):
        #         sub_urls.remove(sub_url)
        #         break
                

        site = sub_url.replace("https://", "")
        site = site.replace("http://", "")
        domain =  site.split("/")[0] 
        
        # print(f"[green]  [+] Scans - {domain} for restrictions")

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url("http://" + domain + "/robots.txt")

        # a = get_robot(domain)


        if not rp.can_fetch("*", sub_url):
            sub_urls.remove(sub_url)


        # try:
        #     restricted = get_robots(domain)
        # except:
        #     print(f"[green]  [+] Scans - {domain} for restrictions")
            # restricted = robots_txt.disallowed(sub_url, proxies)

        #     save_robots(domain, restricted)
            

        # restricted = tuple(restricted)

        # t = sub_url.split("://")[1].split("/")
        # t.remove(t[0])
        
        # t_ = ""
        # for u in t:
        #     t_ += "/" +  u

        # t = t_
    
        # for resk in restricted:
        #     if t.startswith(resk):
        #         sub_urls.remove(sub_url)
        #         break
            


    # check if there is a need of crawling
    for e in sub_urls:

        z__ = if_crawled(e)

        y__ = z__[0]
        t__ = z__[1]


        if y__:
            if t__ < time.time() - 604800 : # Re-Crawls Only After 7
                sub_urls.remove(e)
                continue

        try:
            website_req = requests.get(e, headers = {"user-agent":"open crawler v 0.0.1"}, proxies =  proxies, timeout = TIMEOUT)
        
        except:
            sub_urls.remove(e)
            continue

        try:
            if not "html" in website_req.headers["Content-Type"]:
                print(f"[green]  [+] Skiped : {e} Because Content type not 'html' | Thread : {th}[/green]")
                sub_urls.remove(e)
                continue
        except:
            sub_urls.remove(e)
            continue
                   
        
    write_to_wait_list(sub_urls)
    
    del sub_urls
    
    print(f"[green]  [+] Crawled : {website} | Thread : {th}[/green]")    



## for checking the memory usage uncomment @profile , also uncoment for main()
# @profile 
def crawl(th):

    global ROBOT_SCANS, WEBSITE_SCANS    

    time.sleep(th)

    if EXIT_FLAG:
        return 1


    while not EXIT_FLAG:
        
        # gets 10 urls from waitlist
        sub_urls = get_wait_list(10) 

        for website in sub_urls:
            if website in WEBSITE_SCANS:
                continue
            else:
                WEBSITE_SCANS.append(website)

            website_url = website

            website = website["website"]

            update = False
            
            # Checks if crawled already , y__ = crawled or not , True/False

            z__ = if_crawled(website)

            y__ = z__[0]
            t__ = z__[1]


            if y__:
                update = True

                if int(t__) < int(time.time()) - 604800 : # Re-Crawls Only After 7
                    print(f"[green]  [+] Already Crawled : {website} | Thread : {th}[/green]")
                    continue
                
                print(f"[green]  [+]  ReCrawling  : {website} | Thread : {th} [/green]")

            mal = None
            lang_18 = None

            lang = None
            
            print(f"[green]  [+] Started Crawling : {website} | Thread : {th}[/green]")


            proxies = {}

            if USE_PROXIES:
                proxies = get_proxy()

            try:
                website_req = requests.get(website, headers = {"user-agent":"open crawler v 0.0.1"}, proxies =  proxies, timeout = TIMEOUT)
                
                try:
                    if not "html" in website_req.headers["Content-Type"]:
                        # checks if the site responds with html content or skips
                        print(f"[green]  [+] Skiped : {website} Because Content type not 'html' | Thread : {th}[/green]")
                        continue
                except:
                    continue

                website_txt = website_req.text

                if not update:
                    save_crawl(website, time.time(), 0,0,0,0,0,0,)
                else:
                    update_crawl(website, time.time(), 0,0,0,0,0,0)

            except:
                # could be because website is down or the timeout 
                print(f"[red]  [-] Coundn't Crwal : {website} | Thread : {th}[/red]")
                save_crawl(website, time.time(), "ERROR OCCURED", 0, 0, 0, 0, 0)
                continue

            try:
                lang = detect(website_txt)
            except:
                lang = "un-dic"

            if URL_SCAN:
                mal = scan_url(website)
            
            website_txt_ = remove_html(website_txt)
            
            if Scan_Bad_Words:
                lang_18 = lang_d(website_txt_)

            keywords = []
            desc = ""
            
            soup = BeautifulSoup(website_txt, 'html.parser')
            
            for meta in soup.findAll("meta"):
                try:
                    if meta["name"] == "keywords":
                        keywords = meta["content"]
                except:
                    pass
                
                try:
                    if meta["name"] == "description":
                        desc = meta["content"]
                except:
                    pass
            
            del soup

            top_r = None

            if  Scan_Top_Keywords:
                top_r = get_top_reccuring(website_txt_)

            update_crawl(website, time.time(), mal, lang_18, lang, keywords, desc, top_r)

            del mal, lang_18, lang, keywords, desc, top_r

            sub_urls = []
            
            for x in re.findall(url_extract_pattern, website_txt):
                if re.match(url_pattern, x):
                    if ".onion" in x: 
                        # skips onion sites
                        continue

                    if x[-1] == "/"  or x.endswith(".html") or x.split("/")[-1].isalnum():
                        # tries to filture out not crawlable urls
                        sub_urls.append(x)


            # removes all duplicates
            sub_urls = set(sub_urls)
            sub_urls = list(sub_urls)
                

            # check for restrictions in robots.txt and filture out the urls found
            for sub_url in sub_urls: 
                
                if if_waiting(sub_url):
                    sub_urls.remove(sub_url)
                    continue
                

                site = sub_url.replace("https://", "")
                site = site.replace("http://", "")
                domain =  site.split("/")[0] 
                
                # print(f"[green]  [+] Scans - {domain} for restrictions")
                
                rp = urllib.robotparser.RobotFileParser()
                rp.set_url("http://" + domain + "/robots.txt")

                # a = get_robot(domain)

                if not rp.can_fetch("*", sub_url):
                    sub_urls.remove(sub_url)

                

                # restricted = robots_txt.disallowed(sub_url, proxies)
                    

                # t = sub_url.split("://")[1].split("/")
                # t.remove(t[0])
                
                # t_ = ""
                # for u in t:
                #     t_ += "/" +  u

                # t = t_

                # restricted = tuple(restricted)

                # for resk in restricted:
                #     if t.startswith(resk):
                #         sub_urls.remove(sub_url)
                #         break
                
                        
            # check if there is a need of crawling
            for e in sub_urls:

                z__ = if_crawled(e)

                y__ = z__[0]
                t__ = z__[1]


                if y__:
                    if int(t__) < int(time.time()) - 604800: # Re-Crawls Only After 7
                        sub_urls.remove(e)
                        continue
                
                try:
                    website_req = requests.get(e, headers = {"user-agent":"open crawler v 0.0.1"}, proxies =  proxies, timeout = TIMEOUT)
                
                except:
                    sub_urls.remove(e)
                    continue
                
                try:
                    if not "html" in website_req.headers["Content-Type"]:
                        print(f"[green]  [+] Skiped : {e} Because Content type not 'html' | Thread : {th}[/green]")
                        sub_urls.remove(e)
                        continue
                
                except:
                    sub_urls.remove(e)
                    continue
                               

            
            del proxies

            write_to_wait_list(sub_urls)
            
            del sub_urls
            
            WEBSITE_SCANS.remove(website_url)

            print(f"[green]  [+] Crawled : {website} | Thread : {th}[/green]")





ascii_art = """
[medium_spring_green]
  ______                                        ______                                    __       
 /      \                                      /      \                                  |  \      
|  $$$$$$\  ______    ______   _______        |  $$$$$$\  ______   ______   __   __   __ | $$      
| $$  | $$ /      \  /      \ |       \       | $$   \$$ /      \ |      \ |  \ |  \ |  \| $$      
| $$  | $$|  $$$$$$\|  $$$$$$\| $$$$$$$\      | $$      |  $$$$$$\ \$$$$$$\| $$ | $$ | $$| $$      
| $$  | $$| $$  | $$| $$    $$| $$  | $$      | $$   __ | $$   \$$/      $$| $$ | $$ | $$| $$      
| $$__/ $$| $$__/ $$| $$$$$$$$| $$  | $$      | $$__/  \| $$     |  $$$$$$$| $$_/ $$_/ $$| $$      
 \$$    $$| $$    $$ \$$     \| $$  | $$       \$$    $$| $$      \$$    $$ \$$   $$   $$| $$      
  \$$$$$$ | $$$$$$$   \$$$$$$$ \$$   \$$        \$$$$$$  \$$       \$$$$$$$  \$$$$$\$$$$  \$$      
          | $$                                                                                     
          | $$                                                                                     
           \$$                                                               [bold]v 0.0.1[/bold]  [/medium_spring_green]                            
"""


# for checking the memory usage uncomment @profile
# @profile
def main():
    global DB

    print(ascii_art)

    # Initializes MongoDB
    DB = connect_db(MONGODB_URI, MONGODB_PWD) 
    
    try:
        primary_url = sys.argv[1]
    except:
        print("\n[blue]  [?] Primary Url [You can skip this part but entering] :[/blue]", end="")
        primary_url = input(" ")

    print("")

    if primary_url != "":
        forced_crawl(primary_url)
        print("")


    # Starts threading
    for th in range(0, MAX_THREADS):
        t_d = threading.Thread(target=crawl, args=(th+1,))
        t_d.daemon = True
        t_d.start()
        
        print(f"[spring_green1]  [+] Started Thread : {th + 1}[/spring_green1]")

    print("\n")


    # while loop waiting for exit flag
    while not EXIT_FLAG:
        time.sleep(0.5)


if __name__ == "__main__":
    main()

