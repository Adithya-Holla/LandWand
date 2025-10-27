"""
MySQL User Setup Helper
Generates SQL commands to create MySQL users with proper permissions.
"""

import sys
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent / 'backend'))

from services.network_utils import get_local_ip, get_hostname

def main():
    device_ip = get_local_ip()
    hostname = get_hostname()
    
    print("\n" + "="*60)
    print("🔐 MySQL User Setup Helper")
    print("="*60)
    
    print(f"\n📍 Your Device IP: {device_ip}")
    print(f"📍 Your Hostname: {hostname}")
    
    print("\n" + "="*60)
    print("📝 MySQL Setup Commands")
    print("="*60)
    
    print("\n1️⃣ Connect to MySQL as root:")
    print("   mysql -u root -p")
    
    print("\n2️⃣ Create user for localhost access:")
    print("   CREATE USER 'root'@'localhost' IDENTIFIED BY 'your_password';")
    print("   GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;")
    
    print(f"\n3️⃣ Create user for device IP ({device_ip}):")
    print(f"   CREATE USER 'root'@'{device_ip}' IDENTIFIED BY 'your_password';")
    print(f"   GRANT ALL PRIVILEGES ON *.* TO 'root'@'{device_ip}' WITH GRANT OPTION;")
    
    print(f"\n4️⃣ Create user for hostname ({hostname}):")
    print(f"   CREATE USER 'root'@'{hostname}' IDENTIFIED BY 'your_password';")
    print(f"   GRANT ALL PRIVILEGES ON *.* TO 'root'@'{hostname}' WITH GRANT OPTION;")
    
    print("\n5️⃣ Create user for any host (for network access):")
    print("   CREATE USER 'root'@'%' IDENTIFIED BY 'your_password';")
    print("   GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;")
    
    print("\n6️⃣ Apply changes:")
    print("   FLUSH PRIVILEGES;")
    
    print("\n7️⃣ Verify users:")
    print("   SELECT User, Host FROM mysql.user;")
    
    print("\n" + "="*60)
    print("💡 Quick Setup (Copy-Paste)")
    print("="*60)
    
    print("\n-- Run these commands in MySQL:")
    print(f"CREATE USER 'root'@'localhost' IDENTIFIED BY 'your_password';")
    print(f"CREATE USER 'root'@'{device_ip}' IDENTIFIED BY 'your_password';")
    print(f"CREATE USER 'root'@'%' IDENTIFIED BY 'your_password';")
    print(f"GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;")
    print(f"GRANT ALL PRIVILEGES ON *.* TO 'root'@'{device_ip}' WITH GRANT OPTION;")
    print(f"GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;")
    print(f"FLUSH PRIVILEGES;")
    
    print("\n" + "="*60)
    print("⚠️ Important Notes")
    print("="*60)
    print("\n• Replace 'your_password' with a strong password")
    print("• Update MYSQL_PASSWORD in backend/.env with the same password")
    print("• For production, avoid using 'root'@'%' (security risk)")
    print("• The '%' wildcard allows connections from any host")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
