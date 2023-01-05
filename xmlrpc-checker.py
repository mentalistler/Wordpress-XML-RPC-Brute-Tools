import threading
import requests
import useragent
from urllib.parse import urlparse
result = []
def url2domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def req(url):
    url = url2domain(url)
    try:
        try:
            response = requests.get(f"https://{url}/xmlrpc.php", headers={'User-agent': useragent.get_useragent()},timeout=20)
            if(response.text.find("XML-RPC server accepts POST requests only.")>-1):
                print("Potantial xmlrpc vulnerability found!", url)
                result.append(f"https://{url}/xmlrpc.php")
        except:
            response = requests.get(f"http://{url}/xmlrpc.php",  headers={'User-agent': useragent.get_useragent()},timeout=20)
            if(response.text.find("XML-RPC server accepts POST requests only.")>-1):
                print("Potantial xmlrpc vulnerability found!", url)
                result.append(f"http://{url}/xmlrpc.php")
    except:
        pass
def txt_read():
    lines = open("domains.txt", "r").read().splitlines()

    threads = []
    i = 0
    while i < len(lines):
        for j in range(i, min(i + 100, len(lines))):
            try:
                t = threading.Thread(target=req, args=(f"{lines[j]}",))
                threads.append(t)
                t.start()
            except:
                pass
        for t in threads:
            t.join()
        i += 100
        threads = []

def write_list_to_file():
    txt_read()
    list_to_write = result
    with open("files/results.txt", "w") as f:
        for item in list_to_write:
            f.write(f"{item}\n")
write_list_to_file()
