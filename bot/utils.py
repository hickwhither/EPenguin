import requests
from requests.adapters import HTTPAdapter, Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def requestlog(r: requests.Response, file: str):
    with open(file, "w", encoding='utf-8') as f:
        f.write(r.content.decode())

USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
HEADERSVJP = {
    'User-Agent': USERAGENT,
    "Content-type": "application/x-www-form-urlencoded"
}

def create_session():
    s = requests.Session()
    s.headers.update(HEADERSVJP)
    # keep-alive + retry for transient errors
    retries = Retry(total=3, backoff_factor=0.5,
                    status_forcelist=(429, 500, 502, 503, 504),
                    allowed_methods=frozenset(['GET', 'POST', 'HEAD', 'OPTIONS']))
    s.mount("https://", HTTPAdapter(max_retries=retries, pool_maxsize=10))
    s.mount("http://", HTTPAdapter(max_retries=retries, pool_maxsize=10))
    return s

def pst(s: requests.Session, url: str, data: dict = {}, *args, **kwargs) -> requests.Response:
    s.get(url, headers = {
            "X-Requested-With": "XMLHttpRequest",
            'Referer': url,
        }
    )
    data.update({"csrfmiddlewaretoken": s.cookies.get('csrftoken') or s.cookies.get('csrf')})
    # print(data)
    r = s.post(
        url, data=data,
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            'Referer': url,
        },
        *args, **kwargs
    )
    return r

def update_list_api(API_KEY, API_URL, oj, problems: list[str,str,str]): # id link title
    data = {
        "key": API_KEY,
        "oj": oj,
        "problems": problems
    }
        
    response = requests.post(f"{API_URL}/updater/list", json=data)
    if response.status_code != 200:
        raise Exception(f"API error: {response.json().get('error', 'Unknown error')}")
    return response.json()
