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

        self.set_sessionid("g0br6g3b9bl75ewjzdmjhrrmxk2vdde1")
        self.current_page = 1
    
    def page(p):
        problems = b.get_problem_list(p)
        update_func(problems)
        print(f"Updated {len(problems)} problems from luyencode page {p}")
        # try:
        # except Exception as e:
        #     print(f"Error updating luyencode problems: {e}")
        time.sleep(1)

    def get_cookie(self):
        return self.session.cookies.get('sessionid') or self.session.cookies.get_dict()['sessionid']

    def login(self, username: str, password: str):
        self.session = requests.session()
        self.session.headers = HEADERSVJP
        r = pst(self.session, self.login_site, dict(username=username, password=password))
        return r.url == f"{self.site}/user"

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


def crawler(sessionid, update_func):
    print("Luyencode crawler started!")

    b = Luyencode()
    b.set_sessionid(sessionid)

    
    
    current_page = 1
    while True:
        page_count = b.page_count()
        for i in range(current_page, page_count+1): 
            page(i)
            current_page = i
        current_page = page_count
        time.sleep(60)
