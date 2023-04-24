"""
Open Crawler - Robot.txt - Loader
"""

import requests as r




def get_robot_txt(site, proxies):
    site = site.replace("https://", "")
    site = site.replace("http://", "")
    robot_file_url = "https://" + site.split("/")[0] + "/robots.txt"
    

    try:
        res = r.get(robot_file_url, timeout = 3 , proxies = proxies)
    except:
        res = None

    if res == None:
        return ""

    status = int(res.status_code)

    if status == 200:
        return res.text

    else:
        return ""


def get_lines(txt):
    txt = remove_comments(txt)
    
    while "" in txt:
        txt.remove("")

    while "\n" in txt:
        txt.remove("\n")

    while "\t" in txt:
        txt.remove("\t")
    
    return txt


def remove_comments(txt):
    txt = txt.split("\n")
    txt_ = []
    for e in txt:
        txt_.append(e.split("#")[0])

    return txt_


def disallowed(site, proxies):
    
    txt = get_robot_txt(site, proxies)
    txt = get_lines(txt)    
    
    dis = []
    
    if txt == []:
        return txt

    record = False
    for line in txt:
        if line == "User-agent: *":
            record = True
        elif line.startswith("Disallow:"):
            if record:
                dis.append(line.split(" ")[-1])
        elif "User-agent:" in line:
            if record == True:
                break
        
    return dis


if __name__ == "__main__":
    # print(get_robot_txt("https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt"))
    # print(disallowed("https://www.google.com/robots.txt"))
    pass
