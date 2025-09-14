import requests

from website import db
from ..models import CFProblem

def all_problem():
    r = requests.get("https://codeforces.com/api/problemset.problems")
    status, data = (lambda x=r.json(): (x["status"],x["result"]))()
    print(status)
    for problemObject in data["problems"]:
        # {"contestId":2140,"index":"F","name":"Sum Minimisation","type":"PROGRAMMING","points":2750.0,"tags":["number theory"]}
        problemObject: dict
        id = f"codeforces_{problemObject['contestId']}_{problemObject['index']}"
        name = problemObject["name"]
        rating = problemObject.get("rating")
        if not rating: continue

        existing_problem = CFProblem.query.filter_by(id=id).first()
        if existing_problem:
            existing_problem.name = name
            existing_problem.rating = rating
        else:
            new_problem = CFProblem(id=id, name=name, rating=rating)
            db.session.add(new_problem)
            db.session.commit()


