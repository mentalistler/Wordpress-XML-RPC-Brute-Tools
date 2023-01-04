import requests
import useragent
from urllib.parse import urlparse
def send_req(domain):
    try:
        response = requests.get(f"http://{domain}/wp-json/wp/v2/users",headers={'User-agent': useragent.get_useragent()})
    except:
        response = requests.get(f"https://{domain}/wp-json/wp/v2/users",headers={'User-agent': useragent.get_useragent()})
    return response.json()

def url2domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain
def user_check(url):
    domain = url2domain(url)
    users = []
    try:
        response = send_req(domain)
        for i in range(len(response)):
            users.append(response[i]["slug"])
        #print(domain,users)
        return users
    except:
        return None
