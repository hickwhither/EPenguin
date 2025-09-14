import threading
import json
from utils import *

with open("config.json", "r")as f: data = json.load(f)
API_URL = "http://127.0.0.1:5000"

import luyencode
luyencode.crawler(
    sessionid=data["luyencode"],
    update_func = lambda problems: update_list_api(data["luyencode"], API_URL, "luyencode", problems)
)
# threading.Thread(target=luyencode.crawler, kwargs=dict(
#     sessionid=data["luyencode"],  
#     update_func = lambda oj, problems: update_list_api(data["luyencode"], API_URL, "luyencode", problems)
#     ), daemon=True).start()
