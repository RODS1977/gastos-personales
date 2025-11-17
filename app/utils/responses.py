from flask import jsonify

def success_response(message, data=None, status_code=200):
    response = {
        'status': 'success',
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message, errors=None, status_code=400):
    response = {
        'status': 'error',
        'message': message
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), status_code