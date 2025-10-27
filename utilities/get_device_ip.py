"""
Display device network information
"""

import sys
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent / 'backend'))

from services.network_utils import get_local_ip, get_hostname, get_all_ip_addresses

def main():
    print("\n" + "="*60)
    print("🌐 Device Network Information")
    print("="*60)
    
    hostname = get_hostname()
    primary_ip = get_local_ip()
    all_ips = get_all_ip_addresses()
    
    print(f"\n📍 Hostname: {hostname}")
    print(f"📍 Primary IP Address: {primary_ip}")
    
    if all_ips:
        print(f"\n📍 All IP Addresses:")
        for ip in all_ips:
            print(f"   • {ip}")
    
    print("\n" + "="*60)
    print("💡 Usage Tips:")
    print("="*60)
    print(f"\n1. Set MYSQL_HOST=auto in .env to use: {primary_ip}")
    print(f"2. Access API at: http://{primary_ip}:5000")
    print(f"3. Other devices can connect using: {primary_ip}")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
