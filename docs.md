# Open Crawler 1.0.0 - Documentation 


## Table Of Contents

* [Getting Started](#getting-started)
  * [Installation](#installation)
  * [Uses](#uses)
* [Commands](#commands)
  * [Find Commands](#find-Commands)
  * [About Commands](#about-Commands)
* [Working](#working)


## Getting Started

### Installation

##### Linux

```shell
git clone https://github.com/merwin-asm/OpenCrawler.git
```
```shell
cd OpenCrawler
```
```shell
chmod +x install.sh && ./install.sh
```

##### Windows

*You need git, python3 and pip installed*

```shell
git clone https://github.com/merwin-asm/OpenCrawler.git
```
```shell
cd OpenCrawler
```
```shell
pip install -r requirements.txt
```

### Uses

#### Making A (Not that good) Search engine :

This can be easily done with verry less modifications if required 

- We also provide an inbuild search function , which may not be good enough but does do the thing ( the search topic be discussed below )

#### Osint Tool : 

You can make use of the tool to crawl through sites related to someone and do osint by using the search utility or make custom code for it

#### Pentesting Tool :

Find all websites related to one site , this can be achieved using the connection tree command ( this topic be discussed below )

#### Crawler As It says..

## Commands

### Find Commands
To find the commands you can use any of these 2 methods,

*warning  : this only works in linux*
```sh
man opencrawler
```

For Linux:
```sh
opencrawler help
```
For Windows:
```sh
python opencrawler help
```

### About Commands

#####  help

Shows the commands available

##### v

Shows the current version of opencrawler

##### crawl

This would start the normal crawler

##### forced_crawl \<website\>

Forcefully crawl a site , the site crawled is \<website\>

##### crawled_status

*warning : the data shown aint exact*

Gives the info on the mongoDB..
This will show the number of sites crawled and the avg ammount of storage used.

Show the info for both collections : (more info on the collections are given in the *working* section) 
- crawledsites
- waitlist

##### search \<search\>

Uses basic filturing methods to search , this command aint meant for anything like search engine
(the working of search be discussed in *working* section)


##### configure

Configures the opencrawler... 
The same is also used to re configure...
It will ask all the info required to start the crawler and save it in json file (config.json) (more info in the *config* section)

Its ok if you are running crawl command without configs because it will ask you to .. xd

##### connection-tree \<website\> \<no of layers\>

A tree of websites connected to \<website\> be shown

\<no of layers\> is how deep you want to crawl a site.
The default depth is 2

##### check_html \<website\>

Checks if a website is returning html

##### crawlable \<website\>

Checks if a website is allowed to be crawled
It checks the robot.txt , to find if disallowed

##### dissallowed \<website\>

Shows the disallowed urls of a website
The results are based on robots.txt

##### fix_db 

Starts the fix db program
This can be used to resolve bugs present in the code , which could contaminate the DB

##### re-install 

Re installs the opencrawler

##### update

Installs new version of the opencrawler | reinstalls 

##### install-requirements

Installs the requirements..
These requirements are mentioned in requirements.txt

## Working
bla bla bla
