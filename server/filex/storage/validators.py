import os
import pathlib

from flask import request, current_app, g


def validate_folder_request():
    req_data = request.args
    if not req_data:
        return {
            'error': 'Bad request.'
        }
    if not (type(req_data.get('path')) is str):
        return {
            'error': 'Path invalid or not provided.'
        }
    return req_data
