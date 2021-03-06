from app.api import api
from app.models import File
from flask import jsonify, abort, request
from playhouse.shortcuts import model_to_dict
from app.utils.search import search_files


@api.route('/',  methods=['GET'])
def index():
    return "pong!"


@api.route('/file', methods=['GET'])
def list_all_files():
    query = File.select()
    data = [i.serialize for i in query]
    return jsonify(data)


@api.route('/file/<int:file_id>', methods=['GET'])
def get_file(file_id):
    try:
        file = File.get_by_id(file_id)
        file_contents = open(file.full_path, "r").read()
        json = file.serialize
        json['contents'] = file_contents
        return jsonify(json)
    except File.DoesNotExist:
        return abort(404)


@api.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    if q:
        results = search_files(q)
        return jsonify(results)
    else:
        return jsonify([])
