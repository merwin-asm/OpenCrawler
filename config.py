"""
Configures the Open Crawler v 0.0.1
"""


from rich import print
import getpass
import json
import os


print("[blue][bold]Configuring Open Crawler v 0.0.1[/bold]  - File : config.json[/blue]")

if os.path.exists("config.json"):
    print("[yellow] config.json already found , do you want to rewrite it ? [y/n][/yellow]", end="")
    res = input(" ").lower()
    
    if res == "y":
        os.remove("config.json")
    else:
        exit()


configs = {}



print("\n[green]-----------------------------Writing to config.json-----------------------------[/green]\n")


print("[dark_orange]  [?] MongoDB's Password ?[/dark_orange]", end="")
configs.setdefault("MONGODB_PWD", getpass.getpass(prompt=" "))

print("[dark_orange]  [?] URI Provided By MongoDB ?[/dark_orange]", end="")
configs.setdefault("MONGODB_URI", input(" "))

print("[dark_orange]  [?] Timeout For Requests ?[/dark_orange]", end="")
configs.setdefault("TIMEOUT", int(input(" ")))

print("[dark_orange]  [?] Maximum Threads To Be Used ?[/dark_orange]", end="")
configs.setdefault("MAX_THREADS", int(input(" ")))

print("[dark_orange]  [?] Flaged/Bad words list (enter for default) ?[/dark_orange]", end="")
res = input(" ")

if res == "":
    res = "bad_words.txt"

configs.setdefault("bad_words", res)

print("[dark_orange]  [?] Use Proxies (y/n) ?[/dark_orange]", end="")
res = input(" ").lower()

if res == "y":
    res = True
else:
    res = False

configs.setdefault("USE_PROXIES", res)

print("[dark_orange]  [?] Scan Bad Words (y/n) ?[/dark_orange]", end="")
res = input(" ").lower()

if res == "y":
    res = True
else:
    res = False

configs.setdefault("Scan_Bad_Words", res)

print("[dark_orange]  [?] Scan Top Keywords (y/n) ?[/dark_orange]", end="")
res = input(" ").lower()

if res == "y":
    res = True
else:
    res = False

configs.setdefault("Scan_Top_Keywords", res)

print("[dark_orange]  [?] Scan URL For Malicious Stuff (y/n) ?[/dark_orange]", end="")
res = input(" ").lower()

if res == "y":
    res = True
else:
    res = False

configs.setdefault("URL_SCAN", res)

print("[dark_orange]  [?] UrlScan API Key (If not scanning just enter) ?[/dark_orange]", end="")
configs.setdefault("urlscan_key", input(" "))

print("\n[green]Saving--------------------------------------------------------------------------[/green]\n")


f = open("config.json", "w")
f.write(json.dumps(configs))
f.close()
