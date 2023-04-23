"""
Set of Tools to fix your DB | OpenCrawler v 0.0.1
"""



from mongo_db import connect_db, _DB
from rich import print
import json
import os




def mongodb():
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

    # Initializes MongoDB
    connect_db(MONGODB_URI, MONGODB_PWD) 




mongodb() # Connects to DB



print("\n[blue]---------------------------------------DB-FIXER---------------------------------------[/blue]\n")

print("""[dark_orange]\t[1] Remove Duplicates[/dark_orange]""")


print("\n[blue]Option :[/blue]", end="")
op = input(" ")

if op == "1":

    print("[blue] Scan Crawledsites (y/enter to skip) >[/blue]", end="")
    if input(" ").lower() == "y":
        print("\n[green]  [+] Scanning Duplicates In Crawledsites [/green]")

        e = _DB().Crawledsites.find({})
        for x in e:

            ww = list(_DB().Crawledsites.find({"website":x["website"]}))
            len_ = len(ww)
            
            ww = ww[0]


            if len_ != 1:
                
                _DB().Crawledsites.delete_many({"website":x["website"]})
                
                _DB().Crawledsites.insert_one(ww)

                print(f"[green]  [+] Removed : {x['website']} [/green]")



    print("[blue] Scan waitlist (y/enter to skip) >[/blue]", end="")
    if input(" ").lower() == "y":
    
        print("[green]  [+] Scanning Duplicates In waitlist [/green]")

        e = _DB().waitlist.find({})
        for x in e:

            ww = list(_DB().waitlist.find({"website":x["website"]}))
            len_ = len(ww)

            ww = ww[0]
            
            if len_ != 1:
            
                _DB().waitlist.delete_many({"website":x["website"]})
                
                _DB().waitlist.insert_one(ww)

                print(f"[green]  [+] Removed : {x['website']} [/green]")



    # print("[blue] Scan Robots (y/enter to skip) >[/blue]", end="")
    # if input(" ").lower() == "y":
    
    #     print("[green]  [+] Scanning Duplicates In Robots [/green]")

    #     e = _DB().Robots.find({})
    #     for x in e:

    #         ww = list(_DB().Robots.find({"website":x["website"]}))
    #         len_ = len(ww)

    #         ww = ww[0]
            
    #         if len_ != 1:
            
    #             _DB().Robots.delete_many({"website":x["website"]})
                
    #             _DB().Robots.insert_one(ww)

    #             print(f"[green]  [+] Removed : {x['website']} [/green]")


else:
    print(f"[red]  [-] Option '{op}' Not Found[/red]")


print("\n[blue]--------------------------------------------------------------------------------------[/blue]\n")


