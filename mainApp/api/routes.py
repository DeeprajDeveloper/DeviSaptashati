from flask import Blueprint, jsonify, request
from mainApp.api import functionality as func

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')


@bp_api.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})


@bp_api.route('/search/versesByName', methods=['GET', 'POST'])
def search_verse_by_name():
    shloka_json = func.search_by_verse_name(json_data_body=request.get_json())
    return shloka_json


@bp_api.route('/search/versesByID', methods=['GET'])
def search_verse_by_id():
    shloka_json = func.search_by_verse_id(json_data_body=request.get_json())
    return shloka_json


@bp_api.route('/update/verseMeaning', methods=['POST'])
def update_verse_meaning():
    shloka_json = func.update_verse_meaning(json_data_body=request.get_json())
    return shloka_json



