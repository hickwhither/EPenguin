# from generator import *
from utils import *
from bs4 import BeautifulSoup
import json
import time

class Luyencode:
    
    session: requests.Session

    def __init__(self):
        self.session = create_session()
        
        self.site = "https://luyencode.net"
        self.signup_site = f"{self.site}/accounts/register/"
        self.login_site = f"{self.site}/accounts/login/"


    # def create_account(self, username:str=None, email:str=None, password:str=None, full_name:str=None) -> tuple:
    #     username = username or randomusername()
    #     email = email or randomemail()
    #     password = password or ''.join(i for i in random.choices(string.ascii_letters+string.digits, k=random.randint(10,20)))
    #     full_name = full_name or ''

    #     self.session = requests.session()
    #     self.session.headers = HEADERSVJP
    #     request: requests.Response = pst(self.session, self.signup_site, data=dict(
    #         username = username.replace('-', ''),
    #         email = email.replace('-', ''),
    #         password1 = password,
    #         password2 = password,
    #         full_name = full_name,
    #         timezone = "Asia/Saigon",
    #         language = 4)
    #     )
    #     if request.url!=f"{self.site}/accounts/register/complete/":
    #         print("error:", username, email, password)
    #         with open("a.html", "w", encoding='utf-8') as f: f.write(request.content.decode())
    #         return None
        
    #     return username, email, password

    def get_cookie(self):
        return self.session.cookies.get('sessionid') or self.session.cookies.get_dict()['sessionid']

    def login(self, username: str, password: str):
        self.session = requests.session()
        self.session.headers = HEADERSVJP
        r = pst(self.session, self.login_site, dict(username=username, password=password))
        return r.url == f"{self.site}/user"
        if r.url == f"{self.site}/user": print(f"{username} logged in")
        else: print(f"{username} failed to login")

    def set_sessionid(self, cookie:str) -> None:
        self.session = requests.session()
        self.session.cookies.set('sessionid', cookie)
        self.session.headers = HEADERSVJP

    def submit(self, id: str, code: str, langcode):
        submit_url = f"{self.site}/problem/{id}/submit"
        
        check = self.session.get(submit_url)
        content = check.content.decode()
        if 'Bài tập này hiện tại không chấm' in content or 'No judge is available for this problem' in content:
            raise SyntaxError("No judge avaiable")

        return pst(self.session, submit_url,
            data=dict(
                source = code,
                language = langcode,)
        )


    def get_problem(self, id: str):
        response = self.session.get(f"{self.site}/problem/{id}")
        content = response.content.decode()
        soup = BeautifulSoup(content, 'html.parser')
        # title = soup.find('div', class_='problem-title').text.strip()
        problem = soup.find('div', class_='content-description').text.strip()[:-15]
        data_specific = {
            "Giớihạnthờigian:": "timelimit",
            "Giớihạnbộnhớ:": "memorylimit",
            "Input:": "input",
            "Output:": "output",
        }
        data = {}
        for div in soup.find_all("div", class_="problem-info-entry"):
            text:str = div.text
            text = text.replace('\n', '').replace(' ', '')
            for k, v in data_specific.items():
                if text.startswith(k):
                    data[v] = text[len(k):]
        return problem, data

    def get_problem_list(self, page: int):
        response = self.session.get(f"{self.site}/problems?page={page}")
        content = response.content.decode()
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('tbody')
        problems = []
        for problem in table.find_all('tr'):
            tds = problem.find_all('td')
            problems.append({
                "id": tds[1].text.strip(),
                "link": f"{self.site}/problem/{tds[1].text.strip()}",
                "title": tds[2].text.strip(),
            })
        return problems

    def page_count(self):
        response = self.session.get(f"{self.site}/problems")
        content = response.content.decode()
        soup = BeautifulSoup(content, 'html.parser')
        s = soup.find_all("div", class_="top-pagination-bar")[0].find_all("li")
        count = int(s[-2].text.strip())
        return count

import os
state_file = os.path.join(os.path.dirname(__file__), 'luyencode.json')
def load_state():
    try:
        with open(state_file, 'r') as f:
            return json.load(f).get('current_page', 1)
    except FileNotFoundError: return 1
def save_state(current_page):
    with open(state_file, 'w') as f:
        json.dump({'current_page': current_page}, f)

def crawler(sessionid, update_func):
    print("Luyencode crawler started!")

    b = Luyencode()
    b.set_sessionid(sessionid)

    def page(p):
        problems = b.get_problem_list(p)
        update_func(problems)
        print(f"Updated {len(problems)} problems from luyencode page {p}")
        # try:
        # except Exception as e:
        #     print(f"Error updating luyencode problems: {e}")
        time.sleep(1)
    
    current_page = load_state()
    while True:
        page_count = b.page_count()
        for i in range(current_page, page_count+1): 
            page(i)
            current_page = i
            save_state(current_page)
        current_page = page_count
        save_state(current_page)
        time.sleep(60)
