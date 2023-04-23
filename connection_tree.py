"""
Part of Open Crawler v 0.0.1
"""


from rich import print
import requests
import random
import sys
import re



# regex patterns
url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
url_pattern_0 = "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
url_extract_pattern_0 = "[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"


# Main Variables
website = sys.argv[1] # website to be scanned
num = int(sys.argv[2]) # number of layers to scan




def get_proxy():
    """
    Gets a free proxy from 'proxyscrape'
    returns :  dict - > {"http": "<proxy ip:port>"}
    """

    res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    return {"http" : random.choice(res.text.split("\r\n"))}





def scan(website, max_, it):
    """
    Scans for sub urls and prints them.
    website : Str
    max_ : int
    it : int
    """

    global TOTAL
    
    if max_ != it:
        print("   "*it + "[green]----" + website + ":[/green]")
    else:
        print("   "*it + "[green]----" + website + "[/green]")
        return None    
    
    # Gets a proxy 
    try:
        proxies = get_proxy()
    except:
        proxies = {}

    try:
        website_txt = requests.get(website, headers = {"user-agent":"open crawler Mapper v 0.0.1"}, proxies = proxies).text
    except:
        print(f"[red]  [-]  '{website}' Website Couldn't Be Loaded")

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
    
    for e in sub_urls:
        scan(e, max_ , it + 1)


print(f"[dark_orange]Scanning :{website} | No. of Layers : {num} [/dark_orange]\n")
scan(website, num, 1)


