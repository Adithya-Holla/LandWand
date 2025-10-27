"""
Network utility functions for getting device IP address.
"""

import socket

def get_local_ip():
    """
    Get the local IP address of the current machine.
    
    Returns:
        str: IP address of the machine, or 'localhost' if unable to determine
    """
    try:
        # Create a socket connection to determine the local IP
        # We connect to an external address (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        # Fallback to localhost if unable to determine IP
        return 'localhost'

def get_hostname():
    """
    Get the hostname of the current machine.
    
    Returns:
        str: Hostname of the machine
    """
    try:
        return socket.gethostname()
    except Exception:
        return 'localhost'

def get_all_ip_addresses():
    """
    Get all IP addresses associated with the current machine.
    
    Returns:
        list: List of IP addresses
    """
    try:
        hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
        return [ip for ip in ip_addresses if not ip.startswith("127.")]
    except Exception:
        return []

if __name__ == "__main__":
    print("Device Network Information:")
    print(f"Hostname: {get_hostname()}")
    print(f"Primary IP: {get_local_ip()}")
    print(f"All IPs: {get_all_ip_addresses()}")
