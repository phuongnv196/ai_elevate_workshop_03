from flask import Blueprint, jsonify, request
from services.user_service import UserService
from services.data_service import DataService

# Create blueprint for API routes
api_bp = Blueprint('api', __name__)

# User routes
@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = UserService.get_all_users()
        return jsonify({
            'success': True,
            'data': users,
            'message': 'Users retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve users'
        }), 500

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = UserService.get_user_by_id(user_id)
        if user:
            return jsonify({
                'success': True,
                'data': user,
                'message': 'User retrieved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve user'
        }), 500

@api_bp.route('/users', methods=['POST'])
def create_user():
    """Create new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
            
        user = UserService.create_user(data)
        return jsonify({
            'success': True,
            'data': user,
            'message': 'User created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create user'
        }), 500

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
            
        user = UserService.update_user(user_id, data)
        if user:
            return jsonify({
                'success': True,
                'data': user,
                'message': 'User updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update user'
        }), 500

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        success = UserService.delete_user(user_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'User deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to delete user'
        }), 500

# Data routes
@api_bp.route('/data', methods=['GET'])
def get_data():
    """Get all data"""
    try:
        data = DataService.get_all_data()
        return jsonify({
            'success': True,
            'data': data,
            'message': 'Data retrieved successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve data'
        }), 500

@api_bp.route('/data', methods=['POST'])
def create_data():
    """Create new data entry"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
            
        result = DataService.create_data(data)
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Data created successfully'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create data'
        }), 500
