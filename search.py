"""
Open Crawler v 0.0.1 | search.py

-- Note the official search functions doesnt count the clicks or learn from search patterns etc :]
"""



from mongo_db import connect_db, _DB
from rich import print
import time
import json
import sys
import os
import re




def mongodb():
    # Config File
    config_file = "config.json"


    # Load configs from config_file - > json
    try:
        config_file = open(config_file, "r")
        configs = json.loads(config_file.read())
        config_file.close()

    except:
        try:
            os.system("python3 config.py") # Re-configures
        except:
            os.system("python config.py") # Re-configures


        config_file = open(config_file, "r")
        configs = json.loads(config_file.read())
        config_file.close()


    ## Setting Up Configs
    MONGODB_PWD =  configs["MONGODB_PWD"]
    MONGODB_URI = configs["MONGODB_URI"]

    # Initializes MongoDB
    connect_db(MONGODB_URI, MONGODB_PWD) 




mongodb() # Connects to DB


# Get the search
search = sys.argv[1:]


RESULTS = {} # Collects the results


if len(search) > 1:
    
    t_1 = time.time()

    for e in search:
        url = list(_DB().Crawledsites.find({"$or" : [
            {"recc": {"$regex": re.compile(e, re.IGNORECASE)}},
            {"keys": {"$regex":  re.compile(e, re.IGNORECASE)}},
            {"desc": {"$regex": re.compile(e, re.IGNORECASE)}},
            {"website" : {"$regex": re.compile(e, re.IGNORECASE)}}
        ]}))
        
        res = []
        [res.append(x["website"]) for x in url if x["website"] not in res]
        
        del url

        for url in res:
            if url in RESULTS.keys():
                RESULTS[url] += 1
            else:
                RESULTS.setdefault(url, 1)


    t_2 = time.time()


    RESULTS_ = RESULTS

    RESULTS = sorted(RESULTS.items(), key=lambda x:x[1], reverse=True)

    c = 0
    for result in RESULTS:
        if RESULTS_[result[0]] > 1:
            print(f"[green]Link: {result[0]} | Common words: {result[1]} [/green]")
            c += 1

    print(f"[dark_orange]Query : {search} | Total Results : {c} | Time Taken : {t_2 - t_1}s[/dark_orange]")

else:
    t_1 = time.time()
    e = search[0]
    url = list(_DB().Crawledsites.find({"$or" : [
    {"recc": {"$regex": re.compile(e, re.IGNORECASE)}},
    {"keys": {"$regex":  re.compile(e, re.IGNORECASE)}},
    {"desc": {"$regex": re.compile(e, re.IGNORECASE)}},
    {"website" : {"$regex": re.compile(e, re.IGNORECASE)}}
]}))
    t_2 = time.time()

    res = []
    [res.append(x["website"]) for x in url if x["website"] not in res]
    
    del url

    for result in res:
        print(f"[green]Link: {result}[/green]")

    print(f"[dark_orange]Query : {search} | Total Results : {len(res)} | Time Taken : {t_2 - t_1}s[/dark_orange]")


