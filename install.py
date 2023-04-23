"""
Open Crawler v 1.0.0 Installer
- Linux Installer
"""




import os



os.system("pip3 install rich")

os.system("clear")


from rich import print

print("[green]  [+] Installing Requirements[/green]")


os.system("pip3 install -r requirements.txt")


print("[green]  [+] Installing The Manual | You can run 'man opencrawler' now yey!! [/green]")


os.system("sudo cp opencrawler.1 /usr/local/man/man1/opencrawler.1")

print("[green]  [+] Adding files to path[/green]")

files = ["search.py", "robots_txt.py", "mongo_db.py", "crawler.py", "fix_db.py", "opencrawler", "connection_tree.py", "config.py", "bad_words.txt"] # FIles which will be added to path

for file in files:
      os.system(f"sudo cp {file} /usr/bin/{file}")

os.system("sudo chmod +x /usr/bin/opencrawler")


print("[green] Exited[/green]")


