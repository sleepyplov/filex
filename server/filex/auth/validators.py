from flask import request


def validate_user_data():
    req_data = request.get_json()
    if not req_data:
        return {
            'error': 'Bad request'
        }
    if not (type(req_data.get('username')) is str):
        return {
            'error': 'Username invalid or not provided.'
        }
    if not (type(req_data.get('password')) is str):
        return {
            'error': 'Password invalid or not provided.'
        }
    return req_data
