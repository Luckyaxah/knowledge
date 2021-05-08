from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView

from knowledge.apis.v1 import api_v1
from knowledge.extensions import db
from knowledge.models import User
from knowledge.apis.v1.schemas import user_schema, users_schema

class IndexAPI(MethodView):
    def get(self):
        return jsonify({
            "api_version": "1.0",
        })

class UserAPI(MethodView):
    def get(self):
        page = request.args.get('page', 1, type=int)
        ret = User.query.paginate(page, 5).items
        return jsonify(users_schema(ret, page))



# api_v1.index, api_v1.user
api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/user', view_func=UserAPI.as_view('user'), methods=['GET'])