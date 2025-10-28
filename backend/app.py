from flask import Flask
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv
from services.network_utils import get_local_ip

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get device IP address
DEVICE_IP = get_local_ip()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Get database host (use device IP if MYSQL_HOST is 'auto' or not set)
db_host = os.getenv('MYSQL_HOST', 'auto')
if db_host.lower() == 'auto':
    db_host = DEVICE_IP

# Configuration
app.config['MYSQL_HOST'] = db_host
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'landwand_db')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', '3306'))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Import and register blueprints
from routes.users import users_bp
from routes.data import data_bp

app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(data_bp, url_prefix='/api/data')

# Health check route
@app.route('/')
def index():
    return {
        'status': 'success',
        'message': 'LandWand API is running',
        'version': '1.0.0',
        'server_ip': DEVICE_IP
    }

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'database': 'connected',
        'db_host': app.config['MYSQL_HOST'],
        'server_ip': DEVICE_IP
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n{'='*60}")
    print(f"🚀 Starting LandWand API Server")
    print(f"{'='*60}")
    print(f"Server IP: {DEVICE_IP}")
    print(f"Server Port: {port}")
    print(f"Database Host: {db_host}")
    print(f"API URL: http://{DEVICE_IP}:{port}")
    print(f"{'='*60}\n")
    
    app.run(debug=True, host='0.0.0.0', port=port)
