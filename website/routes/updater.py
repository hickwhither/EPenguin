from flask import Blueprint, request
import json

from website import db
from website.models import FreeProblem

bp = Blueprint('updater', __name__, url_prefix='/updater')

def validate_key(oj, key):
    try:
        with open('bot/config.json') as f:
            config = json.load(f)
            return config.get(oj) == key
    except:
        return False

@bp.before_request
def validate_request():
    data = request.get_json()
    
    # Validate request data
    if not data or not isinstance(data, dict):
        return {"error": "Invalid request data"}, 400    
    required_fields = ['key', 'oj']
    if not all(field in data for field in required_fields):
        return {"error": f"Missing required fields. Required: {required_fields}"}, 400
    
    # Validate key
    if not validate_key(data['oj'], data['key']):
        return {"error": "Invalid key"}, 403

@bp.route('/list', methods=['POST'])
def update_list():
    data = request.get_json()
    
    # Validate problems field
    if 'problems' not in data:
        return {"error": "Missing required field: problems"}, 400

    try:
        for p in data["problems"]:
            p['oj'] = data['oj']
            p['id'] = f"{data['oj']}_{p['id']}"
            problem = FreeProblem.query.filter_by(id=p['id']).first()
            if problem: problem.update(**p)
            else:
                problem = FreeProblem(**p)
                db.session.add(problem)
        db.session.commit()
        print(f"{data['oj']} has updated {len(data['problems'])} problems")
        return {"message": "Problem updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

