from flask import Blueprint, request, jsonify
from models.queries import fetch_all, fetch_one, execute_query
from services.validation import validate_user_data, sanitize_user_data

# Create users blueprint
users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        # Fetch all users from database
        users = fetch_all("SELECT * FROM user_account ORDER BY join_date DESC")
        
        return jsonify({
            'status': 'success',
            'message': 'Users retrieved successfully',
            'data': users,
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch users: {str(e)}',
            'data': []
        }), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        # Fetch single user by ID
        user = fetch_one("SELECT * FROM user_account WHERE user_id = %s", (user_id,))
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User with ID {user_id} not found',
                'data': None
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'User retrieved successfully',
            'data': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch user: {str(e)}',
            'data': None
        }), 500

@users_bp.route('/', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided',
                'data': None
            }), 400
        
        # Sanitize input data
        data = sanitize_user_data(data)
        
        # Validate user data
        is_valid, error_message = validate_user_data(data, is_update=False)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': error_message,
                'data': None
            }), 400
        
        # Check if email already exists
        existing_user = fetch_one("SELECT user_id FROM user_account WHERE email = %s", (data['email'],))
        if existing_user:
            return jsonify({
                'status': 'error',
                'message': 'User with this email already exists',
                'data': None
            }), 409
        
        # Insert new user
        query = """
            INSERT INTO user_account (name, email, phone, password, join_date, buyer, seller) 
            VALUES (%s, %s, %s, %s, CURDATE(), %s, %s)
        """
        params = (
            data['name'],
            data['email'],
            data.get('phone', '0000000000'),
            data.get('password', 'default_password'),
            data.get('buyer', 0),
            data.get('seller', 0)
        )
        
        result = execute_query(query, params)
        
        if result['success']:
            # Fetch the newly created user
            new_user = fetch_one("SELECT * FROM user_account WHERE user_id = %s", (result['last_id'],))
            
            return jsonify({
                'status': 'success',
                'message': 'User created successfully',
                'data': new_user
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to create user: {result["error"]}',
                'data': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to create user: {str(e)}',
            'data': None
        }), 500

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided',
                'data': None
            }), 400
        
        # Check if user exists
        existing_user = fetch_one("SELECT user_id FROM user_account WHERE user_id = %s", (user_id,))
        if not existing_user:
            return jsonify({
                'status': 'error',
                'message': f'User with ID {user_id} not found',
                'data': None
            }), 404
        
        # Sanitize input data
        data = sanitize_user_data(data)
        
        # Validate user data (is_update=True makes all fields optional)
        is_valid, error_message = validate_user_data(data, is_update=True)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': error_message,
                'data': None
            }), 400
        
        # Check if email is being changed and if new email already exists
        if 'email' in data:
            email_exists = fetch_one(
                "SELECT user_id FROM user_account WHERE email = %s AND user_id != %s", 
                (data['email'], user_id)
            )
            if email_exists:
                return jsonify({
                    'status': 'error',
                    'message': 'User with this email already exists',
                    'data': None
                }), 409
        
        # Build dynamic UPDATE query based on provided fields
        update_fields = []
        params = []
        
        allowed_fields = ['name', 'email', 'phone', 'password', 'buyer', 'seller']
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({
                'status': 'error',
                'message': 'No valid fields to update',
                'data': None
            }), 400
        
        # Add user_id to params
        params.append(user_id)
        
        query = f"UPDATE user_account SET {', '.join(update_fields)} WHERE user_id = %s"
        result = execute_query(query, tuple(params))
        
        if result['success']:
            # Fetch the updated user
            updated_user = fetch_one("SELECT * FROM user_account WHERE user_id = %s", (user_id,))
            
            return jsonify({
                'status': 'success',
                'message': 'User updated successfully',
                'data': updated_user
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to update user: {result["error"]}',
                'data': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to update user: {str(e)}',
            'data': None
        }), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        # Check if user exists
        existing_user = fetch_one("SELECT user_id, name FROM user_account WHERE user_id = %s", (user_id,))
        if not existing_user:
            return jsonify({
                'status': 'error',
                'message': f'User with ID {user_id} not found',
                'data': None
            }), 404
        
        # Delete the user
        query = "DELETE FROM user_account WHERE user_id = %s"
        result = execute_query(query, (user_id,))
        
        if result['success']:
            return jsonify({
                'status': 'success',
                'message': f'User {existing_user["name"]} deleted successfully',
                'data': {'user_id': user_id}
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to delete user: {result["error"]}',
                'data': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete user: {str(e)}',
            'data': None
        }), 500
