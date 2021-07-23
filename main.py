import requests, sys, colorama, os, socket, random, urllib3
from bs4 import BeautifulSoup
import re
colorama.init()
__author__ = "mb"
color = {"red":colorama.Fore.LIGHTRED_EX,
        "blue":colorama.Fore.LIGHTBLUE_EX,
        "green":colorama.Fore.GREEN,
        "magenta":colorama.Fore.LIGHTMAGENTA_EX,
        "clear":colorama.Fore.LIGHTWHITE_EX,
        "desc":colorama.Fore.LIGHTBLACK_EX,
        "category": colorama.Fore.LIGHTCYAN_EX,
        "module": colorama.Fore.LIGHTRED_EX}

typemails = ["@gmail.com","@protonmail.com",
            "@protonmail.ch", "@outlook.com",
            "@hotmail.com", "@yahoo.com",
            "@zoho.com", "@aol.com",
            "@aim.com",  "@gmx.com",
            "@gmx.us", "@icloud.com",
            "@yandex.com", "@tutanota.com",
            "@tutanota.de", "@tutamail.com",
            "@tuta.io", "@keemail.me",
            "@mac.hush.com", "@hush.ai",
            "@hush.com", "@hushmail.me",
            "@hushmail.com"]
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

moduleList = ["bruteforce/subdomain",
            "worldlist/subdomain",
            "googledork/subdomain",
            "googledork/sensitive",
            "detection/headers",
            "detection/mails"]
sensitive_search = ['intitle:"index of" "/configs"',
                    'intext:"CAD Media Log"',
                    'intitle:"index of" "/.vscode"',
                    'intitle:"index of" intext:"client.key.pem"',
                    'inurl:wp-content/uploads/ intitle:logs',
                    'inurl:tcpconfig.html',
                    'inurl:/certs/server.key',
                    '"-- Dumped from database version" + "-- Dumped by pg_dump version" ext:txt | ext:sql | ext:env | ext:log',
                    'intitle:"index of" "dump.sql"',
                    'intitle:"index of" "WebServers.xml"',
                    'intitle:"index of" "firewall.log" | "firewall.logs"',
                    'intitle:"index of" "app.log"',
                    'Index of: /services/aadhar card/',
                    'index of logs.tar',
                    '"Index of" "sass-cache"',
                    'intitle:"index of" "/sql"',
                    'intitle:"index of" "db.sqlite3"',
                    'index of storage/oauth-private.key',
                    'inurl:/phpmyadmin/server_databases.php',
                    'inurl:/wp-content/uploads/wpdm-cache',
                    'inurl:/wp-content/uploads/ "phpMyAdmin SQL Dump"',
                    'intitle:"index of" "secret.yaml"',
                    'intitle:"index of" intext:"apikey.txt',
                    'allintext:@gmail.com filetype:log',
                    'ext:xlsx inurl:database',
                    'ext:php intitle:phpinfo "published by the PHP Group"',
                    'intitle:"index of" intext:credentials',
                    'allintext:"Index Of" "cookies.txt"',
                    '"putty.log" ext:log | ext:cfg | ext:txt',
                    'intitle:"index of" "phpmyadmin.sql"',
                    'allintext:username,password filetype:log',
                    '"Web Application Assessment Report" ext:pdf',
                    'inurl:statrep.nsf',
                    'intitle:"index of" "*.cert.pem" | "*.key.pem"',
                    '"index of" "email.ini"']
class bruteforce:
    def __init__(self, url):
        self.baseUrl = url
        self.alph = "abcdefghijklmnopqrstuvwxyz"
    def GenerateSubDomain(self):
        lenn = random.randrange(2,5)
        result = ""
        for x in range(lenn):
            result += random.choice(self.alph)
        return result
    def Subdomain(self, protocols):
        """
    u can use this function
        """
        url = protocols + "://" + self.GenerateSubDomain() + "." +self.baseUrl
        if requests.get(url).status_code != 404:
            return url
        else:
            return None
class WordList:
    def __init__(self, url, wordlpass):
        self.baseUrl = url
        with open(wordlpass, "r") as f:
            self.wordlist = f.read().split("\n")
    def subdomain(self):
        for subdomain in self.wordlist:
            pass            
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        print('\x1bc')
def success(text):
    print(color["green"] + " [ + ] " + color["clear"] + "- " + text + color["clear"])
def search_engine_func(engine,search):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
    r = requests.get(f"https://www.{engine}.com/?q={search}", headers=headers)
    bingtext = r.text
    soup = BeautifulSoup(bingtext, features="lxml")
    links = soup.findAll("a")
    urlresult = []
    for link in links:
        try:
            urlsite = link["href"]
            if "https://" in urlsite:
                urlresult.append(link["href"])
        except:
            pass
    return urlresult
def search_mails(site, mails):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
    r = requests.get(f"https://www.bing.com/?q=site:{site} \"{mails}\"", headers=headers)
    bingtext = r.text
    soup = BeautifulSoup(bingtext, features="lxml")
    links = soup.findAll("a")
    urlresult = []
    for link in links:
        try:
            urlsite = link["href"]
            if "https://" in urlsite:
                urlresult.append(link["href"])
        except:
            pass
    i = 0
    for d in urlresult:
        if i > 100:
            pass
        else:
            i += 1
            bingtext += "\n" + requests.get(d).text
    return bingtext.split("\n")
def alert(text, stop=False):
    print(color["red"] + " [ ! ] " + color["clear"] + "- " + text + color["clear"])
    if stop:
        exit(1)

def info(text):
    print(color["blue"] + "\t [ ! ] " + color["clear"] + text)


def FormatText(text):
    printable_text = ""
    text = text.split("%%")
    for x in text:
        if x == "desco":
            printable_text += color["desc"]
        elif x == "descc":
            printable_text += color["clear"]
        else:
            printable_text += x
    return printable_text
def FormatTextList(text):
    printable_text = ""
    text = text.split("nefzefzefffffse")
    for d in text:
        d = str(d).split("/")
        for x in range(len(d)):
            if x == 0:
                printable_text += color["category"]
                printable_text += d[x]
                printable_text += color["clear"] + "/"
            elif x == 1:
                printable_text += color["module"]
                printable_text += d[x]
                printable_text += color["clear"]
    return printable_text
search_engine = ["bing"]
print(color["clear"] + colorama.Style.BRIGHT)
clear()

if len(sys.argv) < 2:
    alert(sys.argv[0] + " <url> (without protocols)", True)
url = sys.argv[1]
def main():
    print(f"""
        
\t\t\t
\t\t\t           #############
\t\t\t      #######         ########
\t\t\t    #####      /###\\      ######
\t\t\t  ###          ## ##           ###
\t\t\t    #####      \\###/      ######
\t\t\t      #######         ########
\t\t\t           #############  
\t          
\t\t\t       -[ {color["magenta"]} Apollon  eyes {color["clear"]}  ]- """)
    while(1):
        print("\n")
        choice = input(color["magenta"] + "\t\t\t    >_" + color["clear"])
        print("\n")
        primaryreq = requests.get("http://" + url)

        if choice == "help":
            print(FormatText("""
\t\t\trun < module name > %%desco%% # use a module %%descc%%
\t\t\tlist %%desco%% # show module list %%descc%%
            """))
        elif choice == "list":
            for module in moduleList:
                print("\t\t\t" + FormatTextList(module))
        elif choice.startswith("run"):
            choice = choice.split(" ")
            choice = str(choice[1])
            choice = choice.split("/")
            if "bruteforce" in choice[0]:
                bf = bruteforce(sys.argv[1])
                if choice[1] == "subdomain":
                    info("this tools can't see some subdomain you not autorized to see")
                    prot = input(color["magenta"] + "\t\t     protocol (http(s)) >_" + color["clear"])
                    info("press ctrl + c to stop")
                    while(1):
                        try:
                            res = bf.Subdomain(prot)
                            if res != None:
                                success(res)
                        except KeyboardInterrupt:
                            info("brutefoce stopped")
                            break
                        except requests.exceptions.ConnectionError:
                            pass
            if "wordlist" in choice[0]:
                if choice[1] == "subdomain":
                    wordlist = [0,1]
                    while(1):
                        path = input(color["magenta"] + "\t\t     path >_" + color["clear"])
                        try:
                            wordlist = open(path, "r").read().split("\n")
                            break
                        except:
                            alert("check the wordlist path")

                    for word in wordlist:
                        try:
                            r = requests.get(f"https://{word}.{url}")
                            if r.status_code == 200:
                                success(f"https://{word}.{url}")
                        except requests.exceptions.ConnectionError:
                            pass
                        except urllib3.exceptions.LocationParseError:
                            pass
                        except Exception as e:
                            alert(e)
                            pass
            if "googledork" in choice[0]:
                if choice[1] == "subdomain":
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
                    for engine in search_engine:
                        r = requests.get(f"https://www.{engine}.com/?q=site:{url}", headers=headers)
                        bingtext = r.text
                        soup = BeautifulSoup(bingtext, features="lxml")
                        links = soup.findAll("a")
                        info(engine)
                        for link in links:
                            try:
                                urlsite = link["href"]
                                if "https://" in urlsite and "microsoft" not in urlsite:
                                        success(link["href"])
                            except:
                                pass
                if choice[1] == "sensitive":
                    try:
                        aldry_views = []
                        for search in sensitive_search:
                            complete_dork = search + " site:" + url
            
                            d = search_engine_func("bing",complete_dork)
                            if len(d) > 0:
                                for sensitive_result in d:
                                    if url in sensitive_result:
                                        for x in search.split(" "):
                                            if x in requests.get(sensitive_result).text:
                                                if sensitive_result in aldry_views:
                                                    pass
                                                else:
                                                    aldry_views.append(sensitive_result)
                                                    success(sensitive_result)
                            else:
                                alert(complete_dork + " : 0 result")
                        if len(aldry_views) < 1:
                            alert("no sensitive file detected")
                    except KeyboardInterrupt:
                        pass
            if choice[0] == "detection":
                if choice[1] == "headers":
                    for head in primaryreq.headers:
                        info(head + ":" + primaryreq.headers[head])
                if choice[1] == "mails":
                    aldry_mails = []
                    for mail in typemails:
                        for ligne in search_mails(url, mail):
                            for re_match in re.finditer(EMAIL_REGEX, ligne):
                                if "%20%22" in re_match.group():
                                    pass
                                elif re_match.group() in aldry_mails:
                                    pass
                                else:
                                    success(re_match.group())
                                    aldry_mails.append(re_match.group())
                    if len(aldry_mails) < 1:
                        alert("sorry i doesn't find mails :'( ")
                    else:
                        success(f"total {len(aldry_mails)}")
main()
