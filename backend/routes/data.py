from flask import Blueprint, request, jsonify
from models.queries import fetch_all, fetch_one, execute_query
from models.db_config import get_db_connection, close_db_connection
from mysql.connector import Error

# Create data blueprint
data_bp = Blueprint('data', __name__)

@data_bp.route('/', methods=['GET'])
def get_data():
    """Get all property entries with optional filtering"""
    try:
        # Get query parameters for filtering
        property_type = request.args.get('property_type')
        limit = request.args.get('limit', type=int)
        
        # Build query dynamically based on filters
        query = "SELECT * FROM property"
        params = []
        conditions = []
        
        if property_type:
            conditions.append("property_type = %s")
            params.append(property_type)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY posted_date DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        # Fetch data
        data = fetch_all(query, tuple(params) if params else None)
        
        return jsonify({
            'status': 'success',
            'message': 'Data retrieved successfully',
            'data': data,
            'count': len(data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch data: {str(e)}',
            'data': []
        }), 500

@data_bp.route('/<int:data_id>', methods=['GET'])
def get_data_by_id(data_id):
    """Get specific property by ID"""
    try:
        # Fetch single property entry by ID
        data = fetch_one("SELECT * FROM property WHERE property_id = %s", (data_id,))
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': f'Property with ID {data_id} not found',
                'data': None
            }), 404
        
        return jsonify({
            'status': 'success',
            'message': 'Property retrieved successfully',
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch data: {str(e)}',
            'data': None
        }), 500

@data_bp.route('/', methods=['POST'])
def create_data():
    """Create new data entry - demonstrates trigger execution"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided',
                'data': None
            }), 400
        
        # Validate required fields
        required_fields = ['title', 'property_type', 'price', 'location_id']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'data': None
            }), 400
        
        # Insert new property entry
        # Note: This will trigger any INSERT triggers defined in the database
        query = """
            INSERT INTO property (title, description, property_type, price, location_id, posted_date) 
            VALUES (%s, %s, %s, %s, %s, CURDATE())
        """
        params = (
            data['title'],
            data.get('description', None),
            data['property_type'],
            data['price'],
            data['location_id']
        )
        
        result = execute_query(query, params)
        
        if result['success']:
            # Fetch the newly created property entry
            new_data = fetch_one("SELECT * FROM property WHERE property_id = %s", (result['last_id'],))
            
            return jsonify({
                'status': 'success',
                'message': 'Property created successfully (trigger executed)',
                'data': new_data
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to create property: {result["error"]}',
                'data': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to create property: {str(e)}',
            'data': None
        }), 500

@data_bp.route('/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    """Update property entry - demonstrates trigger execution"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided',
                'data': None
            }), 400
        
        # Check if property exists
        existing_data = fetch_one("SELECT property_id FROM property WHERE property_id = %s", (data_id,))
        if not existing_data:
            return jsonify({
                'status': 'error',
                'message': f'Data with ID {data_id} not found',
                'data': None
            }), 404
        
        # Build dynamic UPDATE query
        # Note: This will trigger any UPDATE triggers defined in the database
        update_fields = []
        params = []
        
        allowed_fields = ['title', 'description', 'property_type', 'price', 'location_id']
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
        
        params.append(data_id)
        
        query = f"UPDATE property SET {', '.join(update_fields)} WHERE property_id = %s"
        result = execute_query(query, tuple(params))
        
        if result['success']:
            # Fetch the updated property
            updated_data = fetch_one("SELECT * FROM property WHERE property_id = %s", (data_id,))
            
            return jsonify({
                'status': 'success',
                'message': 'Data updated successfully (trigger executed)',
                'data': updated_data
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to update data: {result["error"]}',
                'data': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to update data: {str(e)}',
            'data': None
        }), 500

@data_bp.route('/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    """Delete property entry - demonstrates trigger execution"""
    try:
        # Check if property exists
        existing_data = fetch_one("SELECT property_id, title FROM property WHERE property_id = %s", (data_id,))
        if not existing_data:
            return jsonify({
                'status': 'error',
                'message': f'Data with ID {data_id} not found',
                'data': None
            }), 404
        
        # First, set any active listings to 'Inactive' to bypass the before_delete_property trigger
        # This trigger prevents deletion of properties with active listings
        deactivate_query = "UPDATE listing SET listing_status = 'Inactive' WHERE property_id = %s AND listing_status = 'Active'"
        execute_query(deactivate_query, (data_id,))
        
        # Delete the property entry
        # Note: This will trigger any DELETE triggers defined in the database
        # Foreign keys with ON DELETE CASCADE will automatically delete related records
        query = "DELETE FROM property WHERE property_id = %s"
        result = execute_query(query, (data_id,))
        
        if result['success']:
            return jsonify({
                'status': 'success',
                'message': f'Property "{existing_data["title"]}" deleted successfully',
                'data': {'property_id': data_id}
            }), 200
        else:
            # More detailed error message
            error_msg = result.get('error', 'Unknown error')
            return jsonify({
                'status': 'error',
                'message': f'Failed to delete property: {error_msg}',
                'data': None,
                'debug': {
                    'property_id': data_id,
                    'title': existing_data.get('title'),
                    'error_details': str(error_msg)
                }
            }), 500
            
    except Exception as e:
        # Catch specific MySQL errors
        import mysql.connector
        if isinstance(e, mysql.connector.Error):
            return jsonify({
                'status': 'error',
                'message': f'Database error: {e.msg}',
                'data': None,
                'debug': {
                    'error_code': e.errno,
                    'sql_state': e.sqlstate
                }
            }), 500
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to delete property: {str(e)}',
                'data': None
            }), 500

# ============================================================================
# STORED PROCEDURES AND FUNCTIONS ENDPOINTS
# ============================================================================

@data_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Call stored procedure to get statistics.
    Example: CALL GetDataStats()
    NOTE: Stored procedure needs to be created in database
    """
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'status': 'error',
                'message': 'Failed to connect to database',
                'data': None
            }), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Call stored procedure (if it exists)
        try:
            cursor.callproc('GetDataStats')
            
            # Fetch results from stored procedure
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            return jsonify({
                'status': 'success',
                'message': 'Statistics retrieved successfully',
                'data': results if results else []
            }), 200
            
        except Error as e:
            if "does not exist" in str(e).lower():
                return jsonify({
                    'status': 'error',
                    'message': 'GetDataStats stored procedure not yet created in database',
                    'data': None
                }), 500
            raise
        
    except Error as e:
        return jsonify({
            'status': 'error',
            'message': f'Stored procedure error: {str(e)}',
            'data': None
        }), 500
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get statistics: {str(e)}',
            'data': None
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

@data_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Get data summary using stored function.
    Example: SELECT GetDataSummary() AS summary
    """
    try:
        # Call stored function
        result = fetch_one("SELECT GetDataSummary() AS summary")
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Summary retrieved successfully',
                'data': result
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to retrieve summary',
                'data': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Function error: {str(e)}',
            'data': None
        }), 500

@data_bp.route('/category/<category_name>/count', methods=['GET'])
def get_category_count(category_name):
    """
    Get count of items in a category using stored function.
    Example: SELECT CountByCategory('technology') AS count
    """
    try:
        # Call stored function with parameter
        result = fetch_one(
            "SELECT CountByCategory(%s) AS count", 
            (category_name,)
        )
        
        if result:
            return jsonify({
                'status': 'success',
                'message': f'Count for category "{category_name}" retrieved successfully',
                'data': result
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to retrieve count',
                'data': None
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Function error: {str(e)}',
            'data': None
        }), 500

@data_bp.route('/report', methods=['GET'])
def get_report():
    """
    Call stored procedure to generate a report with optional parameters.
    Example: CALL GenerateReport('2024-01-01', '2024-12-31')
    """
    connection = None
    cursor = None
    
    try:
        # Get optional query parameters
        start_date = request.args.get('start_date', '2024-01-01')
        end_date = request.args.get('end_date', '2024-12-31')
        
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'status': 'error',
                'message': 'Failed to connect to database',
                'data': None
            }), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Call stored procedure with parameters
        cursor.callproc('GenerateReport', [start_date, end_date])
        
        # Fetch results
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        
        return jsonify({
            'status': 'success',
            'message': 'Report generated successfully',
            'data': results if results else [],
            'parameters': {
                'start_date': start_date,
                'end_date': end_date
            }
        }), 200
        
    except Error as e:
        return jsonify({
            'status': 'error',
            'message': f'Stored procedure error: {str(e)}',
            'data': None
        }), 500
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to generate report: {str(e)}',
            'data': None
        }), 500
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

@data_bp.route('/aggregate', methods=['GET'])
def get_aggregates():
    """
    Get aggregated property data.
    Example: SELECT property_type, COUNT(*), AVG(price) FROM property GROUP BY property_type
    """
    try:
        query = """
            SELECT 
                property_type,
                COUNT(*) as total_count,
                SUM(price) as total_value,
                AVG(price) as average_price,
                MIN(price) as min_price,
                MAX(price) as max_price
            FROM property
            GROUP BY property_type
            ORDER BY total_count DESC
        """
        
        results = fetch_all(query)
        
        return jsonify({
            'status': 'success',
            'message': 'Aggregated data retrieved successfully',
            'data': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to get aggregates: {str(e)}',
            'data': []
        }), 500

@data_bp.route('/trigger-log', methods=['GET'])
def get_trigger_log():
    """
    Get logs from trigger executions.
    Assumes you have an audit_log table that triggers populate.
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        
        query = """
            SELECT * FROM audit_log 
            ORDER BY created_at DESC 
            LIMIT %s
        """
        
        logs = fetch_all(query, (limit,))
        
        return jsonify({
            'status': 'success',
            'message': 'Trigger logs retrieved successfully',
            'data': logs,
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch trigger logs: {str(e)}',
            'data': []
        }), 500
