from flask import jsonify
from functools import wraps
import traceback

def handle_errors(f):
    """Decorator to handle errors in route functions"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation Error',
                'message': str(e)
            }), 400
        except Exception as e:
            # Log the full traceback for debugging
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500
    return decorated_function

def validate_json(required_fields=None):
    """Decorator to validate JSON input"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'message': 'Content-Type must be application/json'
                }), 400
            
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No JSON data provided'
                }), 400
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        'success': False,
                        'message': f'Missing required fields: {", ".join(missing_fields)}'
                    }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def create_response(success=True, data=None, message=None, error=None, status_code=200):
    """Create standardized API response"""
    response = {
        'success': success,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    if error is not None:
        response['error'] = error
    
    return jsonify(response), status_code
