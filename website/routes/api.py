from flask import *
import json, math

from website import db, scheduler
from website.models import FreeProblem

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route("/problems")
def problem_list():
    try:
        page = int(request.args.get('page') or 1)
        count = int(request.args.get('count') or 20)
        oj = request.args.get("oj")
        prob_id = request.args.get("id")
        title = request.args.get("title")
        rating_start = request.args.get("rating_start", type=int)
        rating_end = request.args.get("rating_end", type=int)
    except Exception as e:
        return {"error": f"invalid type {e}"}, 500

    query = FreeProblem.query

    if oj: query = query.filter(FreeProblem.oj == oj)
    if prob_id: query = query.filter(FreeProblem.id.ilike(f"%{prob_id}%"))
    if title: query = query.filter(FreeProblem.title.ilike(f"%{title}%"))

    if rating_start is not None and rating_end is not None:
        query = query.filter(FreeProblem.rating.between(rating_start, rating_end))
    elif rating_start is not None:
        query = query.filter(FreeProblem.rating >= rating_start)
    elif rating_end is not None:
        query = query.filter(FreeProblem.rating <= rating_end)
    
    total = query.count()
    pages = math.ceil(total / count) if count > 0 else 1

    query = query.order_by(FreeProblem.updated_at.desc())


    problems = query.offset((page - 1) * count).limit(count).all()
    problem_json = [
        {
            "oj": p.oj,
            "id": p.id,
            "link": p.link,
            "updated_at": p.updated_at,
            "title": p.title,
            "rating": p.rating,
        }
        for p in problems
    ]

    data = {
        "ojs": ["luyencode"],
        "pages": pages,
        "problems": problem_json
    }
    
    return data

@bp.route("/problem/<string:id>/update")
def update_problem(id):
    problem:FreeProblem = FreeProblem.query.get(id)
    if not problem: return {"error": "Problem not exists"}, 404
    scheduler.add_job(
        id=problem.id,
        func=current_app.bots[problem.oj].fetch,
        kwargs={"problemid": problem.id},
    )

    return {"success": "Job has been added"}


@bp.route("/problem/<string:id>")
def get_problem(id):
    problem:FreeProblem = FreeProblem.query.get(id)
    if not problem:
        return {"error": "Problem not exists"}, 404
    return {
        "oj": problem.oj,
        "id": problem.id,
        "link": problem.link,
        "updated_at": problem.updated_at,
        "rating": problem.rating,

        "title": problem.title,
        "description": problem.description,
        "translated": problem.translated,
        
        "timelimit": problem.timelimit,
        "memorylimit": problem.memorylimit,
        "input": problem.input,
        "output": problem.output,
    }


