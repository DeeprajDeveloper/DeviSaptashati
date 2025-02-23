from flask import jsonify


def _status_information(status_code, status_message, is_success):
    response_data = {
        'statusCode': status_code,
        'statusDescription': 'success' if is_success else 'failure',
        'statusMessageText': status_message
    }
    return response_data


def _error_information(error):
    response_data = {
        'errorCode': error.error_code if hasattr(error, 'error_code') else "UNKNOWN",
        'errorDescription': type(error).__name__,
        'errorStacktrace': str(error)
    }
    return response_data


def populate_json_data_extract(data_id, verse_number, shloka_devanagari, shloka_iast, meaning_english, meaning_hindi, name_devanagari, name_iast, name_english, additional_context=None):
    response_data = {
        "id": data_id,
        "verseInformation": {
            "verseNo": verse_number,
            "shlokaDevanagari": shloka_devanagari,
            "shlokaIAST": shloka_iast
        },
        "verseMeanings": {
            "english": meaning_english,
            "hindi": meaning_hindi
        },
        "verseContext": {
            "nameDevanagari": name_devanagari,
            "nameIAST": name_iast,
            "nameEnglish": name_english,
            "additionalContext": additional_context
        }
    }
    return response_data


def response_template(success=True, message="", data=None, error=None, status_code=200, display_error=False):
    if display_error:
        response_body = {
            "statusInformation": _status_information(status_code=status_code, status_message=message, is_success=success),
            "errorInformation": _error_information(error=error),
            "dataExtract": data
        }
    else:
        response_body = {
            "statusInformation": _status_information(status_code=status_code, status_message=message, is_success=success),
            "dataExtract": data
        }
    response_body = {k: v for k, v in response_body.items() if v is not None}
    return jsonify(response_body), status_code
