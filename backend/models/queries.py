from models.db_config import get_db_connection, close_db_connection
from mysql.connector import Error

def fetch_all(query, params=None):
    """
    Fetch all rows from a SELECT query.
    
    Args:
        query (str): SQL SELECT query
        params (tuple): Query parameters (optional)
    
    Returns:
        list: List of rows as dictionaries, or empty list if error occurs
    """
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        return results
        
    except Error as e:
        print(f"Error executing fetch_all query: {e}")
        return []
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

def fetch_one(query, params=None):
    """
    Fetch a single row from a SELECT query.
    
    Args:
        query (str): SQL SELECT query
        params (tuple): Query parameters (optional)
    
    Returns:
        dict: Single row as dictionary, or None if not found or error occurs
    """
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchone()
        return result
        
    except Error as e:
        print(f"Error executing fetch_one query: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

def execute_query(query, params=None):
    """
    Execute INSERT, UPDATE, DELETE queries.
    
    Args:
        query (str): SQL query (INSERT, UPDATE, DELETE)
        params (tuple): Query parameters (optional)
    
    Returns:
        dict: Dictionary with success status, affected rows, and last inserted ID
              Format: {'success': bool, 'affected_rows': int, 'last_id': int, 'error': str}
    """
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        if not connection:
            return {
                'success': False,
                'affected_rows': 0,
                'last_id': None,
                'error': 'Failed to connect to database'
            }
        
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Get the number of affected rows and last inserted ID
        affected_rows = cursor.rowcount
        last_id = cursor.lastrowid
        
        return {
            'success': True,
            'affected_rows': affected_rows,
            'last_id': last_id if last_id > 0 else None,
            'error': None
        }
        
    except Error as e:
        print(f"Error executing query: {e}")
        return {
            'success': False,
            'affected_rows': 0,
            'last_id': None,
            'error': str(e)
        }
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

def execute_many(query, data_list):
    """
    Execute multiple INSERT/UPDATE queries in batch.
    
    Args:
        query (str): SQL query with placeholders
        data_list (list): List of tuples containing parameters for each query
    
    Returns:
        dict: Dictionary with success status and affected rows
              Format: {'success': bool, 'affected_rows': int, 'error': str}
    """
    connection = None
    cursor = None
    
    try:
        connection = get_db_connection()
        if not connection:
            return {
                'success': False,
                'affected_rows': 0,
                'error': 'Failed to connect to database'
            }
        
        cursor = connection.cursor()
        cursor.executemany(query, data_list)
        
        affected_rows = cursor.rowcount
        
        return {
            'success': True,
            'affected_rows': affected_rows,
            'error': None
        }
        
    except Error as e:
        print(f"Error executing batch query: {e}")
        return {
            'success': False,
            'affected_rows': 0,
            'error': str(e)
        }
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)
