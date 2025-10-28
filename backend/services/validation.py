import re
from typing import Dict, Tuple, Optional, Any
from datetime import datetime

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format using regex.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required and must be a string"
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email) is not None:
        return True, ""
    return False, "Invalid email format"

def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format.
    Accepts various formats: +1234567890, 123-456-7890, (123) 456-7890, etc.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not phone or not isinstance(phone, str):
        return False, "Phone number is required and must be a string"
    
    # Remove common separators for validation
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    if len(cleaned) >= 10 and cleaned.isdigit():
        return True, ""
    return False, "Invalid phone number format (minimum 10 digits required)"

def validate_string_length(value: str, min_length: int = 1, max_length: int = 255) -> Tuple[bool, str]:
    """
    Validate string length is within specified range.
    
    Args:
        value (str): String to validate
        min_length (int): Minimum allowed length
        max_length (int): Maximum allowed length
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not value or not isinstance(value, str):
        return False, "Value is required and must be a string"
    
    length = len(value.strip())
    if length < min_length:
        return False, f"Value must be at least {min_length} characters long"
    if length > max_length:
        return False, f"Value must not exceed {max_length} characters"
    return True, ""

def validate_required_field(value: Any, field_name: str) -> Tuple[bool, str]:
    """
    Validate that a required field is present and not empty.
    
    Args:
        value: Field value to validate
        field_name (str): Name of the field for error messages
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if value is None or value == "":
        return False, f"{field_name} is required"
    if isinstance(value, str) and not value.strip():
        return False, f"{field_name} cannot be empty"
    return True, ""

def validate_numeric_range(value: Any, field_name: str, min_val: Optional[float] = None, 
                          max_val: Optional[float] = None) -> Tuple[bool, str]:
    """
    Validate that a numeric value is within a specified range.
    
    Args:
        value: Numeric value to validate
        field_name (str): Name of the field for error messages
        min_val (float, optional): Minimum allowed value
        max_val (float, optional): Maximum allowed value
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    try:
        num_value = float(value)
        
        if min_val is not None and num_value < min_val:
            return False, f"{field_name} must be at least {min_val}"
        
        if max_val is not None and num_value > max_val:
            return False, f"{field_name} must not exceed {max_val}"
        
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number"

def validate_date(date_str: str, field_name: str = "Date", 
                 date_format: str = "%Y-%m-%d") -> Tuple[bool, str]:
    """
    Validate date string format.
    
    Args:
        date_str (str): Date string to validate
        field_name (str): Name of the field for error messages
        date_format (str): Expected date format (default: YYYY-MM-DD)
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not date_str or not isinstance(date_str, str):
        return False, f"{field_name} is required and must be a string"
    
    try:
        datetime.strptime(date_str, date_format)
        return True, ""
    except ValueError:
        return False, f"{field_name} must be in format {date_format}"

def validate_choice(value: Any, choices: list, field_name: str) -> Tuple[bool, str]:
    """
    Validate that a value is within a list of allowed choices.
    
    Args:
        value: Value to validate
        choices (list): List of allowed values
        field_name (str): Name of the field for error messages
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if value not in choices:
        return False, f"{field_name} must be one of: {', '.join(map(str, choices))}"
    return True, ""

def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL format.
    
    Args:
        url (str): URL to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL is required and must be a string"
    
    url_pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    if re.match(url_pattern, url):
        return True, ""
    return False, "Invalid URL format"

def validate_user_data(data: Dict, is_update: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate user data for create or update operations.
    
    Args:
        data (dict): User data to validate
        is_update (bool): Whether this is an update operation (makes fields optional)
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not data or not isinstance(data, dict):
        return False, "Invalid data format"
    
    # Required fields for creation
    if not is_update:
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
    
    # Validate name if provided
    if 'name' in data:
        is_valid, message = validate_string_length(data['name'], min_length=2, max_length=100)
        if not is_valid:
            return False, f"Name: {message}"
    
    # Validate email if provided
    if 'email' in data:
        is_valid, message = validate_email(data['email'])
        if not is_valid:
            return False, message
    
    # Validate phone if provided
    if 'phone' in data and data['phone']:
        is_valid, message = validate_phone(data['phone'])
        if not is_valid:
            return False, message
    
    # Validate address if provided
    if 'address' in data and data['address']:
        is_valid, message = validate_string_length(data['address'], min_length=5, max_length=500)
        if not is_valid:
            return False, f"Address: {message}"
    
    # Validate role if provided
    if 'role' in data and data['role']:
        valid_roles = ['user', 'admin', 'moderator', 'guest']
        is_valid, message = validate_choice(data['role'], valid_roles, 'Role')
        if not is_valid:
            return False, message
    
    # Validate password if provided
    if 'password' in data and data['password']:
        is_valid, message = validate_string_length(data['password'], min_length=6, max_length=255)
        if not is_valid:
            return False, "Password must be at least 6 characters long"
    
    return True, None

def validate_data_entry(data: Dict, is_update: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Validate data entry for create or update operations.
    
    Args:
        data (dict): Data entry to validate
        is_update (bool): Whether this is an update operation (makes fields optional)
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not data or not isinstance(data, dict):
        return False, "Invalid data format"
    
    # Required fields for creation
    if not is_update:
        required_fields = ['title', 'category']
        for field in required_fields:
            is_valid, message = validate_required_field(data.get(field), field.capitalize())
            if not is_valid:
                return False, message
    
    # Validate title if provided
    if 'title' in data:
        is_valid, message = validate_string_length(data['title'], min_length=3, max_length=200)
        if not is_valid:
            return False, f"Title: {message}"
    
    # Validate description if provided
    if 'description' in data and data['description']:
        is_valid, message = validate_string_length(data['description'], min_length=0, max_length=1000)
        if not is_valid:
            return False, f"Description: {message}"
    
    # Validate category if provided
    if 'category' in data:
        valid_categories = ['technology', 'business', 'education', 'health', 'entertainment', 'other']
        is_valid, message = validate_choice(data['category'], valid_categories, 'Category')
        if not is_valid:
            return False, message
    
    # Validate status if provided
    if 'status' in data and data['status']:
        valid_statuses = ['active', 'inactive', 'pending', 'archived']
        is_valid, message = validate_choice(data['status'], valid_statuses, 'Status')
        if not is_valid:
            return False, message
    
    # Validate value if provided
    if 'value' in data and data['value'] is not None:
        is_valid, message = validate_numeric_range(data['value'], 'Value', min_val=0, max_val=999999)
        if not is_valid:
            return False, message
    
    return True, None

def sanitize_string(value: str) -> str:
    """
    Sanitize string input by trimming whitespace and removing potentially harmful characters.
    
    Args:
        value (str): String to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not value or not isinstance(value, str):
        return ""
    
    # Trim whitespace
    sanitized = value.strip()
    
    # Remove null bytes
    sanitized = sanitized.replace('\x00', '')
    
    return sanitized

def sanitize_user_data(data: Dict) -> Dict:
    """
    Sanitize all string fields in user data.
    
    Args:
        data (dict): User data to sanitize
        
    Returns:
        dict: Sanitized user data
    """
    if not data or not isinstance(data, dict):
        return {}
    
    sanitized = {}
    string_fields = ['name', 'email', 'phone', 'address', 'role', 'password']
    
    for field in string_fields:
        if field in data and isinstance(data[field], str):
            sanitized[field] = sanitize_string(data[field])
        elif field in data:
            sanitized[field] = data[field]
    
    return sanitized
