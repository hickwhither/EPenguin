from flask import Blueprint, request
import json

from website import db
from website.models import FreeProblem

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route("/problems")
def get_problem():
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
    
    problems = query.offset((page - 1) * count).limit(count).all()

    problem_json = [
        {
            "oj": p.oj,
            "id": p.id,
            "link": p.link,
            "title": p.title,
            "rating": p.rating,
        }
        for p in problems
    ]
    
    return problem_json