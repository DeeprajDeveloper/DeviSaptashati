from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import URLSafeTimedSerializer as Serializer
from config import SECRET_KEY
from mainApp.authentication import functionality as func

# Authentication and Token Generation
auth = HTTPTokenAuth(scheme='Bearer')
serializer = Serializer(secret_key=SECRET_KEY)
bp_auth = Blueprint('bp_auth', __name__, url_prefix='/auth')


@bp_auth.route('/generateBearerToken', methods=['PUT'])
def generate_token():
    response_token = func.generate_bearer_token(serializer=serializer, data=request.json)
    return jsonify(response_token)


@bp_auth.route('/getAllClientTokens', methods=['GET'])
def verify_client_auth_token():
    response_json = func.fetch_all_bearer_tokens_by_client(client_id=request.args.get('clientId'))
    return jsonify(response_json)
