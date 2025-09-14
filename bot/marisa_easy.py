from .utils import *
# from generator import *
from bs4 import BeautifulSoup

class MARIA_SITE:
    
    session: requests.Session

    def __init__(self, site:str=None):
        self.site = site or "https://marisaoj.com"

        self.signup_site = f"{site}/accounts/register/"
        self.login_site = f"{site}/accounts/login/"

    def get_cookie(self):
        return self.session.cookies.get('sessionid') or self.session.cookies.get_dict()['sessionid']

    def login(self, username: str, password: str):
        self.session = requests.session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        r = pst(self.session, self.login_site, dict(username=username, password=password))
        if r.url == f"{self.site}/user": print(f"{username} logged in")
        else: print(f"{username} failed to login")

    def by_cookie(self, cookie:str) -> None:
        self.session = requests.session()
        self.session.cookies.set('sessionid', cookie)
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    def submit(self, id: str, code: str, langcode, mashup:int = None):
        if mashup: submit_url = f"{self.site}/mashup/{mashup}/submit/{id}"
        else: submit_url = f"{self.site}/submit/{id}"

        print(submit_url, "SUBMIT NE")

        return pst(self.session, submit_url,
            data=dict(
                problem=id,
                source = code,
                language = langcode,
            ), verify=False
        )

    def get_problem(self, id: str, mashup:int = None):
        if mashup: url = f"{self.site}/mashup/{mashup}/problem/{id}"
        else: url = f"{self.site}/problem/{id}"
        content = self.session.get(url, verify=False).content.decode()
        # get div tag with class="problem"
        soup = BeautifulSoup(content, 'html.parser')
        problem = soup.find('div', class_='problem')
        return problem.text

    def get_problem_list(self, page: int):
        content = self.session.get(f"{self.site}/problemset/{page}", verify=False).content.decode()
        soup = BeautifulSoup(content, 'html.parser')
        problems = []
        status = {
            'status-2': 'Not submitted',
            'status-0': 'Accepted',
            'status-1': 'Not finished',
        }
        for problem in soup.find('table').find_all('tr'):
            problems.append((problem.find('a')['href'].split('/')[-1], status.get(problem.find_all('td')[0]['class'][0]) ))
        return problems
