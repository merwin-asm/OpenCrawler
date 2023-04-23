"""
Open Crawler v 0.0.1 | CLI 
"""



from rich.table import Table
from rich import print
from mongo_db import *
import robots_txt
import requests
import json
import sys
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




# Finding the location of the file
cur_path = __file__.split("/")
cur_path.remove(cur_path[-1])
cur_path_ = ""
for dir_ in cur_path:
    cur_path_ += "/" + dir_
cur_path = cur_path_



table_commands = Table(title="Help - Open Crawler v 0.0.1")

table_commands.add_column("Command", style="cyan", no_wrap=True)
table_commands.add_column("Use", style="magenta")
table_commands.add_column("No", justify="right", style="green")

table_commands.add_row("help", "Get info about the commands", "1")
table_commands.add_row("v", "Get the version of open crawler", "2")
table_commands.add_row("crawl", "Starts up the normal crawler", "3")
table_commands.add_row("force_crawl <websites>", "Forcefully crawls a website", "4")
table_commands.add_row("crawled_status", "Shows the amount of data in DB , etc", "5")
table_commands.add_row("configure", "Write / reWrite The config file", "6")
table_commands.add_row("connection-tree <website> <no of layers>", "Makes a tree of websites connected to it, layers by default is 2", "7")
table_commands.add_row("check_html <website>", "Checks if a website respond with html content", "8")
table_commands.add_row("crawlable <website>", "Checks if a website is allowed to be crawled", "9")
table_commands.add_row("dissallowed <website>", "Lists the websites not allowed to be crawled", "10")
table_commands.add_row("re-install", "Re installs the Open Crawler", "11")
table_commands.add_row("update", "Updates the open crawler", "12")
table_commands.add_row("install-requirements", "Installs requirements for open crawler", "13")
table_commands.add_row("search <search>", "Search from the crawled data", "14")
table_commands.add_row("fix_db", "Tools to fix the DB", "15")



try:
    main_arg = sys.argv[1]
except:
    print(table_commands)
    quit()

try:
    if main_arg == "help":
        print(table_commands)


    elif main_arg == "v":
        print("""
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
           
           """)
    

    elif main_arg == "fix_db":
        os.system(f"python3 {cur_path}/fix_db.py")

    elif main_arg == "search": 

        pool = False

        try:
            test_arg = sys.argv[2:]
    
        except:
            print("[red]  [-] No Search Text[/red]") 
            quit()

        txt = ""
        for e in test_arg:
            txt += " " + e

        if txt.startswith("--pool"):
            pool = True
        
        if not pool:
            os.system(f"python {cur_path}/search.py {txt}")
        
        else:
            try:
                pool_url = sys.argv[3]
            except:
                print("[red]  [-] Pool URL not given[/red]")
                quit()
            
            txt = txt.replace("--pool", "")
            txt = txt.replace(pool_url, "")

            os.system(f"python {cur_path}/pool_search.py {pool_url} {txt}")


    elif main_arg == "configure":
        os.system(f"python3 {cur_path}/config.py")


    elif main_arg == "crawl":
        os.system(f"python3 {cur_path}/main.py")

    elif main_arg == "forced_crawl":
        try:
            web = sys.argv[2]
        except:
            print("[red]  [-] Link Not Passed In [/red]") 
            quit()

        os.system(f"python3 {cur_path}/main.py {web}")
                

    elif main_arg == "crawled_status":
        mongodb()
        try:
            res = get_info()
        except:
            print("[red]  [-] Couldn't Get The Info[/red]")
            quit()

        print("[yellow3]  [?] The Info Given Wouldn't Be Accurate[/yellow3]\n")

        print(f"[dark_orange] \t : Crawled Sites - > {res[0]} [/dark_orange]")
        print(f"[dark_orange] \t :   Wait list   - > {res[1]} [/dark_orange]")

        print("")

    elif main_arg == "connection-tree":
        try:
            web = sys.argv[2]
        except:
            print("[red]  [-] Link Not Passed In [/red]") 
            quit()
        
        num = 2

        try:
            num = sys.argv[3]
        except:
            pass

        os.system(f"python3 {cur_path}/connection_tree.py {web} {num}")


    elif main_arg == "dissallowed":
        try:
            web = sys.argv[2]
        except:
            print("[red]  [-] Link Not Passed In [/red]") 
            quit()

        try:
            restricted = robots_txt.disallowed(web, None)
        except:
            print("[red]  [-] The site was down or some other error [/red]")
            quit()
        
        print("[green]  [+] Dissallowed : [/green]")
        for e in restricted:
            print(f"[green]  \t\t-------> {e} [/green]")


    elif main_arg == "crawlable":
        try:
            web = sys.argv[2]
        except:
            print("[red]  [-] Link Not Passed In [/red]") 
            quit()

        try:
            restricted = robots_txt.disallowed(web, None)
        except:
            print("[red]  [-] The site was down or some other error [/red]")
            quit()

        site = web
        site = site.replace("https://", "")
        site = site.replace("http://", "")
        web = site.split("/")
        web.remove(web[0])
        site = ""
        for e in web:
            site += e + "/"
        web = site

        A =  True
        for e in restricted:
            if web.startswith(e):
                A = False
                break
        
        if A:
            print(f"[green]  [+] Can Be Crawled [/green]")
        else:
            print(f"[red]  [-] Can't Be Crawled [/red]")


    elif main_arg == "check_html":
        try:
            web = sys.argv[2]
        except:
            print("[red]  [-] Link Not Passed In [/red]") 
            quit()
        
        try:
            is_html =  "html" in requests.get(web).headers["Content-Type"]
        except:
            print("[red]  [-] Can't Be Checked Because the site is down or no content type provided in headers[/red]")
            quit()

        if is_html:
            print(f"[green]  [+] '{web}' Respond With HTML Content [/green]")
        else:
            print(f"[red]  [-] '{web}' Doesn't Respond With HTML Content [/red]")


    elif main_arg == "update":
        os.system("pip3 uninstall opencrawler")
        cur_ver = requests.get("https://raw.githubusercontent.com/merwin-asm/OpenCrawler/main/current.ver").text
        cur_ver = cur_ver.replace("\n", "")
        os.system(f"pip3 install opencrawler=={cur_ver}")


    elif main_arg == "install_requirements":
        os.system(f"pip install -r {cur_path}/requirements.txt")
    

    elif main_arg == "re_install":
        os.system("pip3 uninstall opencrawler")
        os.system("pip3 install opencrawler")


    else:
        print(f"[red]  [-] Command '{main_arg}' Not Found || Use 'opencrawler help' For Commands[/red]")

except:
    print("[red]  [-] Some Error Occurred[/red]")


