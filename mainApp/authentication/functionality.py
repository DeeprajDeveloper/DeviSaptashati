import config
from datetime import datetime, timedelta
from flask import abort
from mainApp.constants import (Authentication as Auth)
from utilities import sqlite_util as sql


def generate_bearer_token(serializer, data):

    if not data or 'clientId' not in data:
        abort(400, description="Missing client_id")

    client_id = data['clientId']
    latest_token_date = sql.dql_fetch_all_rows_for_one_input(
        database=config.DATABASE_URL,
        sql_script=Auth.SQL_STATEMENTS['latestToken']['getLatestTokenGenerationDatetime'],
        data_input=client_id
    )

    current_datetime = datetime.now()
    last_generated_token_date = datetime.strptime(latest_token_date[0], "%Y-%m-%d %H:%M:%S.%f")

    if current_datetime > last_generated_token_date:
        active_auth_tokens = sql.dql_fetch_all_rows_for_one_input(
            database=config.DATABASE_URL,
            sql_script=Auth.SQL_STATEMENTS['activeToken']['getTokenByClientId'],
            data_input=client_id
        )

        if len(active_auth_tokens) != 0:
            return {'clientId': client_id, 'message': 'There is an existing active token allocated to this clientId. Please use the /auth/getAllClientTokens to find the active one.'}
        else:
            token = serializer.dumps({'clientId': client_id})
            is_inserted = save_bearer_token_to_database(
                client_id=client_id,
                token=token
            )

            if len(is_inserted) > 0:
                return {'clientId': client_id, 'bearerToken': is_inserted[0], 'expirationTimeInSeconds': Auth.EXPIRATION['inSeconds'], 'isExisting': is_inserted[1]}
            else:
                return {'clientId': client_id, 'bearerToken': None, 'exception': 'unable to generate auth token.'}
    else:
        next_timestamp = last_generated_token_date + timedelta(days=Auth.EXPIRATION['inDays'])
        return {'clientId': client_id, 'bearerToken': None, 'exception': f'New token cannot be generated as it has expired recently. Please wait until {next_timestamp} to regenerate a new token.'}


def save_bearer_token_to_database(client_id, token):
    current_datetime = datetime.now()
    expiration_datetime = current_datetime + timedelta(days=Auth.EXPIRATION['inDays'])

    try:
        existing_token = sql.dql_fetch_all_rows_for_one_input(
            database=config.DATABASE_URL,
            sql_script=Auth.SQL_STATEMENTS['existingToken']['getTokenInformationByClientId'],
            data_input=client_id
        )

        if len(existing_token) > 0 and existing_token[3] == 1 and datetime.strptime(existing_token[2], "%Y-%m-%d %H:%M:%S.%f") > datetime.now():
            return [existing_token[1], existing_token[3]]
        elif len(existing_token) > 0 and existing_token[3] == 1 and datetime.strptime(existing_token[2], "%Y-%m-%d %H:%M:%S.%f") < datetime.now():
            data_input = {
                '@clientId': client_id,
                '@rowId': existing_token[0]
            }
            sql.dml_dql_execute_parameterized_script(
                database=config.DATABASE_URL,
                sql_script=Auth.SQL_STATEMENTS['updateStatements']['deactivateToken'],
                data_input_list=data_input
            )

            inputs = {
                '@clientId': client_id,
                '@bearerToken': token,
                '@creationDtTm': current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
                '@expirationDtTm': expiration_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
                '@isActive': 1
            }
            sql.dml_dql_execute_parameterized_script(
                database=config.DATABASE_URL,
                sql_script=Auth.SQL_STATEMENTS['insertStatements']['insertNewToken'],
                data_input_list=inputs
            )

            return [token, 0]
        else:
            inputs = {
                '@clientId': client_id,
                '@bearerToken': token,
                '@creationDtTm': current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
                '@expirationDtTm': expiration_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
                '@isActive': 1
            }
            sql.dml_dql_execute_parameterized_script(
                database=config.DATABASE_URL,
                sql_script=Auth.SQL_STATEMENTS['insertStatements']['insertNewToken'],
                data_input_list=inputs
            )

            return [token, 0]
    except Exception as err:
        return None


def fetch_all_bearer_tokens_by_client(client_id):
    response_json = []
    retrieved_data = sql.dql_fetch_all_rows_for_one_input(
        database=config.DATABASE_URL,
        sql_script=Auth.SQL_STATEMENTS['existingToken']['getTokenInformationByClientId'],
        data_input=client_id,
        return_list=False
    )
    for data_item in retrieved_data:
        json_data = {
            'clientId': client_id,
            'recordId': int(data_item[0]),
            'isTokenActive': True if data_item[6] == 1 else False,
            'tokenInformation': {
                'bearerToken': data_item[1],
                'creationDatetime': data_item[2],
                'expirationDatetime': data_item[3],
                'lastUsedDatetime': data_item[4],
                'apiUsageCount': data_item[5],
                'allocatedApiUsageCount': data_item[7]
            }
        }
        response_json.append(json_data)
    return response_json

