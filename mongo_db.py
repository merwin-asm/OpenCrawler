"""
Open Crawler v 0.0.1 | Mongo - DB 
"""


from pymongo.mongo_client import MongoClient
from rich import print
import atexit
import time
import json
import os


# Main Variables
CLIENT = None
DB = None



def connect_db(uri, pwd):
    """
    Initializes Connection With MongoDB
    uri : str - > The URI given by MongoDB
    pwd : str - > The password to connect
    """

    global CLIENT, DB
    
    uri = uri.replace("<password>", pwd)
    
    try:
        CLIENT = MongoClient(uri)
        print("[spring_green1]  [+] Connected To MongoDB [/spring_green1]")
        
        DB = CLIENT.Crawledsites


    except Exception as e:
        print("[red]  [-] Error Occured While Connecting To Mongo DB [/red]")
        print(f"[red] [bold] \t\t\t\t Error : {e}[/bold] [/red]")
        quit()
    


def if_waiting(url):
    """
    Checks if a website is in the waiting list
    returns bool 
    """
    try:
        a = DB.waitlist.find_one({"website":url})["website"]
        if a != None:
            return True
        else:
            return False
    except:
        return False


def _DB():
    """
    returns the DB
    """
    return DB


def get_info():
    """
    To get count of docs in main collections
    returns list of int
    """

    a = int(DB.Crawledsites.estimated_document_count())
    b = int(DB.waitlist.estimated_document_count())
    
    a = f" Len : {a} | Storage : {a*257} Bytes"
    b = f" Len : {b} | Storage : {b*618} Bytes"

    return [a, b]



def get_last():
    """
    Last crawled site
    returns str
    """
    a = DB.Crawledsites.find().sort("_id", -1)
    return a[0]["website"]



def get_crawl(website):
    """
    Get crawled info of a site
    returns dict
    """

    return dict(DB.Crawledsites.find_one({"website":website}))



def if_crawled(url):
    """
    Checks if a site was crawled
    returns Bool , time/None (last crawled time)
    """
    try:
        a = DB.Crawledsites.find_one({"website":url})
        return True, a["time"]

    except:
        return False, None



def update_crawl(website, time, mal, offn, ln, key, desc, recc):
    """
    Updates a crawl
    """
    DB.Crawledsites.delete_many({"website":website})
    DB.Crawledsites.insert_one({"website":website, "time":time, "mal":mal, "offn":offn, "ln":ln, "key":key, "desc":desc, "recc":recc})




def save_crawl(website, time, mal, offn, ln, key, desc, recc):
    """
    Saves a crawl
    """
    DB.Crawledsites.insert_one({"website":website, "time":time, "mal":mal, "offn":offn, "ln":ln, "key":key, "desc":desc, "recc":recc})



def save_robots(website, robots):
    """
    Saves dissallowed sites
    """

    DB.Robots.insert_one({"website":website, "restricted":robots})




def get_robots(website):
    """
    Gets dissallowed sites from the database
    """
    return DB.Robots.find_one({"website":website})["restricted"]
    


def get_wait_list(num):
    """
    Gets websites to crawl
    num : int - > number of websites to recv
    returns list - > list of websites
    """

    wait =  list(DB.waitlist.find().limit(num))

    for e in wait:
        DB.waitlist.delete_many({"website":e["website"]})
    
    return wait



def write_to_wait_list(list_):
    """
    Writes to collection of websites to get crawled
    list_ : list - > website urls
    """

    list_ = set(list_)
    list__ = []



    for e in list_:
        if not if_waiting(e):
            list__.append({"website": e})


    try:
        DB.waitlist.insert_many(list__)
    except:
        pass



# Part of testings
if __name__ == "__main__":

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

    connect_db(MONGODB_URI, MONGODB_PWD)

    # save_crawl("w1",1,0,1,3,4,5,5)
    # save_crawl("w2",4,0,1,3,4,5,5)
    # save_crawl("w3",10,0,1,3,4,5,5)
    # print(if_crawled("w"))
    # update_crawl("w",1,1,1,3,4,5,5)
    # print(get_last())
    # print(if_crawled("https://darkmash-org.github.io/"))
    # print(get_robots("www.bfi.org.uk"))    
    # print(if_waiting("https://www.w3.org/blog/2015/01/"))
