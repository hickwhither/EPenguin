# from generator import *
from ..utils import *
from bs4 import BeautifulSoup
import json, time, os

from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

from website import db, scheduler
from website.models import FreeProblem

from .luyencode import Luyencode

dik = os.path.dirname(os.path.abspath(__file__))
accounts = json.load(open(os.path.join(dik, "luyencode.secret.json"), 'r'))

class Updater(Luyencode):
    
    session: requests.Session

    def __init__(self, app):
        self.app = app
        super().__init__()

        self.login(*accounts[0])
        print(f"logged in {accounts[0][0]}")
        self.current_page = 1
        print('LuyencodeBot started')
        scheduler.task('interval', id='luyencode', seconds=120)(self.task)
    
    def task(self):
        with self.app.app_context():
            page_count = self.page_count()
            problems = self.get_problem_list(self.current_page)
            for problem_dict in problems:
                problem_dict['oj'] = 'luyencode'
                problem_dict['id'] = 'luyencode_' + problem_dict['id']
                
                problem = FreeProblem.query.get(problem_dict['id'])
                if problem: problem.update(**problem_dict)
                else:
                    problem = FreeProblem(**problem_dict)
                    db.session.add(problem)
                
                db.session.commit()
            print(f'LuyencodeBot updated page {self.current_page}/{page_count} with {len(problems)} problem(s)')
            self.current_page += 1
            self.current_page = min(self.current_page, page_count)
    
    def fetch(self, problemid):
        with self.app.app_context():
            print(f'updating problem {problemid} 1')
            if not problemid.startswith('luyencode_'): return
            id = problemid[10:]
            problem_dict = self.get_problem(id)

            print(f'updating problem {problemid} 2')
            
            problem = FreeProblem.query.get(problemid)
            if problem: problem.update(**problem_dict)
            else:
                problem = FreeProblem(**problem_dict)
                db.session.add(problem)
            
            db.session.commit()
            
            print(f'updated problem {problemid}')


def setup(app):
    return Updater(app)
