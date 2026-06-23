import telebot
import subprocess
import os
import zipfile
import tempfile
import shutil
from telebot import types
import time
from datetime import datetime, timedelta
import psutil
import sqlite3
import logging
import threading
import re
import sys
import atexit
import requests
import random
import string
import json
import ast
from flask import Flask
from threading import Thread
import hashlib
import hmac
import secrets
import asyncio
import aiohttp
import docker
import yaml
import git
import schedule
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import signal
import traceback
import platform
import socket
import netifaces
import speedtest
from cryptography.fernet import Fernet
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import io
import pandas as pd
import numpy as np
from functools import wraps
import cachetools
import redis
import pymongo
from motor import motor_asyncio
import bcrypt
import jwt
from email.mime.text import MIMEText
import smtplib
import dns.resolver
import whois
import ssl
import certifi

# --- Flask Keep Alive ---
app = Flask('')

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>☁️ KELVIN CLOUD - Premium Hosting Environment</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { max-width: 800px; margin: 0 auto; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px; }
                h1 { font-size: 3em; }
                .status { display: inline-block; padding: 10px 20px; background: #4CAF50; border-radius: 5px; }
                .stats { margin-top: 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
                .stat { padding: 15px; background: rgba(255,255,255,0.2); border-radius: 5px; text-align: center; }
                .stat-value { font-size: 2em; font-weight: bold; }
                .stat-label { font-size: 0.9em; opacity: 0.8; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>☁️ KELVIN CLOUD</h1>
                <p>Premium Hosting Environment</p>
                <div class="status">🟢 ONLINE</div>
                <div class="stats" id="stats">
                    <div class="stat">
                        <div class="stat-value" id="users">-</div>
                        <div class="stat-label">Active Users</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="files">-</div>
                        <div class="stat-label">Total Files</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value" id="uptime">-</div>
                        <div class="stat-label">Uptime</div>
                    </div>
                </div>
                <p>🚀 Advanced Cloud Execution Platform</p>
            </div>
            <script>
                setInterval(() => {
                    fetch('/stats').then(r => r.json()).then(data => {
                        document.getElementById('users').textContent = data.users;
                        document.getElementById('files').textContent = data.files;
                        document.getElementById('uptime').textContent = data.uptime;
                    });
                }, 5000);
            </script>
        </body>
    </html>
    """

@app.route('/stats')
def stats():
    try:
        stats = get_bot_statistics()
        return {
            'users': stats['total_users'],
            'files': stats['total_files'],
            'uptime': str(timedelta(seconds=int(time.time() - start_time)))
        }
    except:
        return {'users': 0, 'files': 0, 'uptime': '0:00:00'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'timestamp': time.time()}

@app.route('/metrics')
def metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"""
# HELP cpu_usage CPU usage percentage
# TYPE cpu_usage gauge
cpu_usage {cpu}
# HELP memory_usage Memory usage percentage
# TYPE memory_usage gauge
memory_usage {memory}
# HELP disk_usage Disk usage percentage
# TYPE disk_usage gauge
disk_usage {disk}
"""

def run_flask():
    port = 8080  # တိုက်ရိုက် Port ထည့်ထားတယ်
    app.run(host='0.0.0.0', port=port, threaded=True)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("☁️ Cloud Keep-Alive server started on port 8080")

# ============================================
# တိုက်ရိုက် Configuration ထည့်ထားတဲ့ အပိုင်း
# ============================================

# --- Bot Configuration ---
BOT_TOKEN = "8863011906:AAEi3j9eQ5sKdH32VN0BWxAP4qOXK2AK154"  # ခင်ဗျားရဲ့ Bot Token ထည့်ပါ
OWNER_ID = 6873534451  # Owner ID ထည့်ပါ
ADMIN_ID = 6873534451  # Admin ID ထည့်ပါ (Owner နဲ့တူရင် ဒီအတိုင်းထား)
YOUR_USERNAME = "@zinko158"  # Support Username ထည့်ပါ

# --- Force Join Configuration ---
FORCE_CHANNEL_ID = -1002756417115
FORCE_GROUP_ID = -1002756417115
FORCE_CHANNEL_LINK = 'https://t.me/+NLb-9NFUSiY1YjVl'
FORCE_GROUP_LINK = 'https://t.me/+KT3SAWDdC-MxNjJl'

# --- Optional Features (သုံးချင်မှ ထည့်၊ မသုံးရင် None ထား) ---
REDIS_URL = None  # ဥပမာ: "redis://localhost:6379"
MONGODB_URI = None  # ဥပမာ: "mongodb://localhost:27017"
WEBHOOK_URL = None
SMTP_SERVER = None  # ဥပမာ: "smtp.gmail.com"
SMTP_PORT = None  # ဥပမာ: 587
SMTP_USERNAME = None  # ဥပမာ: "your-email@gmail.com"
SMTP_PASSWORD = None  # ဥပမာ: "your-app-password"
FROM_EMAIL = None  # ဥပမာ: "noreply@kelvin.cloud"

# --- Security Keys (Auto-generated) ---
ENCRYPTION_KEY = Fernet.generate_key().decode()  # Auto generate
JWT_SECRET = secrets.token_urlsafe(32)  # Auto generate

# ============================================
# စစ်ဆေးခြင်း
# ============================================

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN ထည့်ဖို့လိုတယ်!")
if not OWNER_ID:
    raise ValueError("❌ OWNER_ID ထည့်ဖို့လိုတယ်!")
if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID ထည့်ဖို့လိုတယ်!")
if not YOUR_USERNAME:
    raise ValueError("❌ YOUR_USERNAME ထည့်ဖို့လိုတယ်!")

# Convert to int
try:
    OWNER_ID = int(OWNER_ID)
    ADMIN_ID = int(ADMIN_ID)
    FORCE_CHANNEL_ID = int(FORCE_CHANNEL_ID)
    FORCE_GROUP_ID = int(FORCE_GROUP_ID)
except ValueError:
    raise ValueError("❌ ID တွေကို ဂဏန်းထည့်ပေးပါ!")

# --- Rest of your code continues here ---
# (အောက်က ကျန်တဲ့ Code တွေ အကုန်ဆက်ထည့်ပါ)

# Base Directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BOTS_DIR = os.path.join(BASE_DIR, 'kelvin_uploads')
KELVIN_DIR = os.path.join(BASE_DIR, 'kelvin_data')
DATABASE_PATH = os.path.join(KELVIN_DIR, 'kelvin_host.db')
BACKUP_DIR = os.path.join(KELVIN_DIR, 'backups')
LOGS_DIR = os.path.join(KELVIN_DIR, 'logs')
TEMP_DIR = os.path.join(KELVIN_DIR, 'temp')
CACHE_DIR = os.path.join(KELVIN_DIR, 'cache')
PLUGINS_DIR = os.path.join(KELVIN_DIR, 'plugins')
DOCKER_DIR = os.path.join(KELVIN_DIR, 'docker')

# Create necessary directories
for dir_path in [UPLOAD_BOTS_DIR, KELVIN_DIR, BACKUP_DIR, LOGS_DIR, TEMP_DIR, CACHE_DIR, PLUGINS_DIR, DOCKER_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# File upload limits
FREE_USER_LIMIT = 3
PREMIUM_USER_LIMIT = 999
ADMIN_LIMIT = 999
OWNER_LIMIT = float('inf')

# Security configuration
MAX_WARNINGS = 3
RATE_LIMIT = 10  # messages per second
RATE_WINDOW = 60  # seconds
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_IPS = ['127.0.0.1']
BLOCKED_IPS = []

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Data structures with thread safety
bot_scripts = {}
user_subscriptions = {}
user_files = {}
active_users = set()
admin_ids = {ADMIN_ID, OWNER_ID}
bot_locked = False
force_join_enabled = True
broadcast_messages = {}
rate_limits = defaultdict(list)
start_time = time.time()

# Thread pools
executor = ThreadPoolExecutor(max_workers=10)
task_queue = Queue()
cleanup_queue = Queue()

# Cache
cache = cachetools.TTLCache(maxsize=100, ttl=300)

# Initialize encryption
if ENCRYPTION_KEY:
    cipher_suite = Fernet(ENCRYPTION_KEY.encode())
else:
    cipher_suite = Fernet(Fernet.generate_key())

# Initialize Redis for caching
redis_client = None
if REDIS_URL:
    try:
        redis_client = redis.from_url(REDIS_URL)
        logger.info("✅ Redis connected")
    except:
        logger.warning("⚠️ Redis connection failed")

# Initialize MongoDB for advanced storage
mongodb_client = None
if MONGODB_URI:
    try:
        mongodb_client = pymongo.MongoClient(MONGODB_URI)
        db = mongodb_client.kelvin_cloud
        logger.info("✅ MongoDB connected")
    except:
        logger.warning("⚠️ MongoDB connection failed")

# Initialize Docker client
docker_client = None
try:
    docker_client = docker.from_env()
    logger.info("✅ Docker client initialized")
except:
    logger.warning("⚠️ Docker not available")

# Security scan patterns
SUSPICIOUS_PATTERNS = {
    'source_reading': [
        r'kelvinhost\.py', r'open.*kelvinhost', r'read.*kelvinhost',
        r'import.*kelvinhost', r'from.*kelvinhost', r'__file__.*kelvinhost',
        r'os\.path\.dirname.*kelvinhost', r'\.\./kelvinhost', r'\./kelvinhost',
        r'/kelvinhost\.py', r'kelvin_host\.py', r'this.*bot.*source',
        r'host.*bot.*code', r'telegram\.send_document.*kelvinhost'
    ],
    'file_exfiltration': [
        r'telegram\.send_document', r'send_document', r'upload.*file',
        r'export.*file', r'copy.*file', r'shutil\.copy', r'os\.system.*cp',
        r'wget.*\.py', r'curl.*\.py', r'requests\.post.*file',
        r'base64.*encode.*file', r'send.*file.*telegram', r'forward.*file',
        r'download.*file', r'ftp\.', r'sftp\.', r'scp '
    ],
    'directory_traversal': [
        r'os\.listdir', r'os\.walk', r'glob\.glob', r'Path\(.*\)\.rglob',
        r'find.*\.py', r'scan.*directory', r'explore.*files',
        r'get.*all.*files', r'search.*files', r'enumerate.*files',
        r'\.\./\.\./', r'\.\.\\\\\.\.\\\\', r'/etc/passwd', r'C:\\\\Windows'
    ],
    'sensitive_access': [
        r'DATABASE_PATH', r'UPLOAD_BOTS_DIR', r'KELVIN_DIR', r'user_files',
        r'user_subscriptions', r'admin_ids', r'BOT_TOKEN', r'OWNER_ID',
        r'API_KEY', r'PASSWORD', r'SECRET', r'TOKEN', r'DATABASE'
    ],
    'obfuscation': [
        r'exec\(', r'eval\(', r'__import__\(', r'compile\(', r'base64\.b64decode',
        r'codecs\.decode', r'getattr.*__', r'setattr.*__', r'bytearray.*decode',
        r'str.*decode', r'chr\(', r'hex\(', r'oct\(', r'bin\('
    ],
    'backdoor': [
        r'socket\.connect', r'bind.*port', r'listen.*port', r'accept\(\)',
        r'shell.*true', r'pty\.spawn', r'subprocess\.Popen.*shell',
        r'os\.system', r'os\.popen', r'backconnect', r'reverse.*shell',
        r'metasploit', r'empire', r'cobalt', r'beacon'
    ],
    'crypto_mining': [
        r'miner', r'monero', r'xmrig', r'cpuminer', r'stratum',
        r'cryptonight', r'ethminer', r'claymore', r'mining'
    ],
    'ddos_tools': [
        r'slowloris', r'goldeneye', r'hulk', r'torshammer',
        r'loic', r'hoic', r'xoic', r'ddos', r'flood'
    ]
}

SUSPICIOUS_IMPORTS = [
    'os', 'sys', 'subprocess', 'pathlib', 'zipfile', 'tempfile',
    'requests', 'base64', 'codecs', 'pickle', 'marshal', 'ctypes',
    'pty', 'telnetlib', 'ftplib', 'smtplib', 'socket', 'ssl',
    'cryptography', 'Crypto', 'hashlib', 'hmac', 'secrets'
]

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.py': 'Python', '.java': 'Java', '.html': 'HTML', '.htm': 'HTML',
    '.js': 'JavaScript', '.css': 'CSS', '.txt': 'Text', '.json': 'JSON',
    '.xml': 'XML', '.php': 'PHP', '.c': 'C', '.cpp': 'C++', '.cs': 'C#',
    '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust', '.md': 'Markdown',
    '.yaml': 'YAML', '.yml': 'YAML', '.sql': 'SQL', '.sh': 'Shell',
    '.bat': 'Batch', '.ps1': 'PowerShell', '.r': 'R', '.swift': 'Swift',
    '.kt': 'Kotlin', '.scala': 'Scala', '.pl': 'Perl', '.lua': 'Lua',
    '.ts': 'TypeScript', '.jsx': 'React JSX', '.tsx': 'React TSX',
    '.vue': 'Vue', '.svelte': 'Svelte', '.dart': 'Dart', '.scss': 'SCSS',
    '.less': 'Less', '.styl': 'Stylus', '.coffee': 'CoffeeScript',
    '.dockerfile': 'Dockerfile', '.yml': 'Docker Compose', '.tf': 'Terraform',
    '.tfvars': 'Terraform', '.tfstate': 'Terraform', '.tfstate.backup': 'Terraform'
}

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, 'bot.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Database Functions ---
DB_LOCK = threading.Lock()

def init_db():
    """Initialize database with all tables"""
    logger.info(f"🛢️ Initializing database at: {DATABASE_PATH}")
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verified INTEGER DEFAULT 0,
            key_used TEXT,
            key_used_date TIMESTAMP,
            language TEXT DEFAULT 'en',
            timezone TEXT DEFAULT 'UTC',
            notification_pref INTEGER DEFAULT 1,
            email TEXT,
            phone TEXT,
            api_key TEXT,
            last_active TIMESTAMP,
            total_uploads INTEGER DEFAULT 0,
            total_downloads INTEGER DEFAULT 0,
            bandwidth_used INTEGER DEFAULT 0,
            storage_used INTEGER DEFAULT 0
        )''')
        
        # Subscriptions table
        c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
            user_id INTEGER PRIMARY KEY,
            expiry TEXT,
            file_limit INTEGER DEFAULT 999,
            redeemed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            plan_type TEXT DEFAULT 'premium',
            auto_renew INTEGER DEFAULT 0,
            payment_method TEXT,
            payment_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        # Files table
        c.execute('''CREATE TABLE IF NOT EXISTS user_files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            chat_id INTEGER,
            file_name TEXT,
            file_type TEXT,
            file_path TEXT,
            original_filename TEXT,
            file_size INTEGER,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            is_pending INTEGER DEFAULT 0,
            is_public INTEGER DEFAULT 0,
            downloads INTEGER DEFAULT 0,
            last_download TIMESTAMP,
            checksum TEXT,
            version INTEGER DEFAULT 1,
            tags TEXT,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        # Active users table
        c.execute('''CREATE TABLE IF NOT EXISTS active_users (
            user_id INTEGER PRIMARY KEY
        )''')
        
        # Admins table
        c.execute('''CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            role TEXT DEFAULT 'admin',
            permissions TEXT,
            added_by INTEGER,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Subscription keys table
        c.execute('''CREATE TABLE IF NOT EXISTS subscription_keys (
            key_value TEXT PRIMARY KEY,
            created_by INTEGER,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            days_valid INTEGER,
            max_uses INTEGER DEFAULT 1,
            used_count INTEGER DEFAULT 0,
            file_limit INTEGER DEFAULT 999,
            is_active INTEGER DEFAULT 1,
            used_by_user INTEGER,
            used_date TIMESTAMP,
            key_type TEXT DEFAULT 'premium',
            price REAL,
            currency TEXT DEFAULT 'USD'
        )''')
        
        # Key usage table
        c.execute('''CREATE TABLE IF NOT EXISTS key_usage (
            key_value TEXT,
            user_id INTEGER,
            used_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            PRIMARY KEY (key_value, user_id)
        )''')
        
        # Bot settings table
        c.execute('''CREATE TABLE IF NOT EXISTS bot_settings (
            setting_key TEXT PRIMARY KEY,
            setting_value TEXT,
            updated_by INTEGER,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT
        )''')
        
        # Banned users table
        c.execute('''CREATE TABLE IF NOT EXISTS banned_users (
            user_id INTEGER PRIMARY KEY,
            banned_by INTEGER,
            ban_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reason TEXT,
            ban_type TEXT DEFAULT 'permanent',
            ban_expiry TIMESTAMP
        )''')
        
        # Security logs table
        c.execute('''CREATE TABLE IF NOT EXISTS security_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            file_name TEXT,
            threat_count INTEGER,
            risk_level TEXT,
            action_taken TEXT,
            log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            details TEXT
        )''')
        
        # API keys table
        c.execute('''CREATE TABLE IF NOT EXISTS api_keys (
            api_key TEXT PRIMARY KEY,
            user_id INTEGER,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_date TIMESTAMP,
            last_used TIMESTAMP,
            permissions TEXT,
            requests_count INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        # Webhooks table
        c.execute('''CREATE TABLE IF NOT EXISTS webhooks (
            webhook_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            url TEXT,
            events TEXT,
            secret TEXT,
            is_active INTEGER DEFAULT 1,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        # Notifications table
        c.execute('''CREATE TABLE IF NOT EXISTS notifications (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            message TEXT,
            type TEXT,
            is_read INTEGER DEFAULT 0,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        # Backups table
        c.execute('''CREATE TABLE IF NOT EXISTS backups (
            backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT,
            backup_path TEXT,
            size INTEGER,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            restore_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')
        
        # Statistics table
        c.execute('''CREATE TABLE IF NOT EXISTS statistics (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            total_users INTEGER,
            new_users INTEGER,
            total_files INTEGER,
            new_files INTEGER,
            total_downloads INTEGER,
            bandwidth_used INTEGER,
            storage_used INTEGER,
            premium_users INTEGER,
            active_sessions INTEGER
        )''')
        
        # Insert default settings
        default_settings = [
            ('free_user_limit', str(FREE_USER_LIMIT), 'Free user file limit'),
            ('force_join_enabled', '1', 'Force join requirement'),
            ('maintenance_mode', '0', 'Maintenance mode status'),
            ('bot_version', '3.0.0', 'Bot version'),
            ('max_file_size', str(MAX_FILE_SIZE), 'Maximum file size'),
            ('rate_limit', str(RATE_LIMIT), 'Rate limit per user'),
            ('rate_window', str(RATE_WINDOW), 'Rate limit window'),
            ('backup_enabled', '1', 'Auto backup enabled'),
            ('backup_interval', '24', 'Backup interval in hours'),
            ('log_level', 'INFO', 'Logging level')
        ]
        
        for key, value, desc in default_settings:
            c.execute('''INSERT OR IGNORE INTO bot_settings 
                        (setting_key, setting_value, description) VALUES (?, ?, ?)''',
                     (key, value, desc))
        
        # Insert owner and admin
        c.execute('INSERT OR IGNORE INTO admins (user_id, role) VALUES (?, ?)', (OWNER_ID, 'owner'))
        if ADMIN_ID != OWNER_ID:
            c.execute('INSERT OR IGNORE INTO admins (user_id, role) VALUES (?, ?)', (ADMIN_ID, 'admin'))
        
        conn.commit()
        conn.close()
        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}", exc_info=True)

def load_data():
    """Load data from database into memory with caching"""
    logger.info("📥 Loading data from database...")
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()

        # Load subscriptions
        c.execute('SELECT user_id, expiry, file_limit FROM subscriptions')
        for user_id, expiry, file_limit in c.fetchall():
            try:
                user_subscriptions[user_id] = {
                    'expiry': datetime.fromisoformat(expiry),
                    'file_limit': file_limit if file_limit else 999
                }
            except ValueError:
                logger.warning(f"⚠️ Invalid expiry for user {user_id}")

        # Load files
        c.execute('SELECT user_id, file_name, file_type, file_path FROM user_files WHERE is_pending = 0')
        for user_id, file_name, file_type, file_path in c.fetchall():
            if user_id not in user_files:
                user_files[user_id] = []
            user_files[user_id].append((file_name, file_type, file_path))

        # Load active users
        c.execute('SELECT user_id FROM active_users')
        active_users.update(user_id for (user_id,) in c.fetchall())

        # Load admins
        c.execute('SELECT user_id FROM admins')
        admin_ids.update(user_id for (user_id,) in c.fetchall())

        # Load settings
        c.execute('SELECT setting_key, setting_value FROM bot_settings')
        for key, value in c.fetchall():
            if key == 'free_user_limit':
                global FREE_USER_LIMIT
                FREE_USER_LIMIT = int(value) if value.isdigit() else 1
            elif key == 'force_join_enabled':
                global force_join_enabled
                force_join_enabled = value == '1'

        conn.close()
        logger.info(f"📊 Data loaded: {len(active_users)} users, {len(user_subscriptions)} subscriptions, {len(admin_ids)} admins")
    except Exception as e:
        logger.error(f"❌ Error loading data: {e}", exc_info=True)

# --- Security Functions ---
def rate_limit_check(user_id):
    """Check if user has exceeded rate limit"""
    now = time.time()
    user_requests = rate_limits[user_id]
    
    # Remove old requests
    user_requests = [t for t in user_requests if now - t < RATE_WINDOW]
    rate_limits[user_id] = user_requests
    
    if len(user_requests) >= RATE_LIMIT:
        return False
    
    user_requests.append(now)
    return True

def generate_api_key(user_id):
    """Generate API key for user"""
    key = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(days=365)
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO api_keys (api_key, user_id, expires_date, permissions)
                 VALUES (?, ?, ?, ?)''',
              (key, user_id, expiry.isoformat(), 'read,write'))
    conn.commit()
    conn.close()
    
    return key

def validate_api_key(api_key):
    """Validate API key"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''SELECT user_id, expires_date, permissions FROM api_keys 
                 WHERE api_key = ? AND expires_date > ?''',
              (api_key, datetime.now().isoformat()))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {'user_id': result[0], 'permissions': result[2]}
    return None

def encrypt_data(data):
    """Encrypt sensitive data"""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt sensitive data"""
    return cipher_suite.decrypt(data.encode()).decode()

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_jwt_token(user_id, expiry_hours=24):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=expiry_hours)
    }
    return jwt.encode(payload, JWT_SECRET or 'secret', algorithm='HS256')

def verify_jwt_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET or 'secret', algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

def get_client_ip(message):
    """Get client IP from message context"""
    # This is a simplified version - in production, you'd get this from request context
    return '127.0.0.1'

def is_ip_blocked(ip):
    """Check if IP is blocked"""
    return ip in BLOCKED_IPS

def scan_file_for_threats(file_path, user_id, username, file_name):
    """Advanced security scan with ML-based detection"""
    threats_found = []
    file_content = ""
    
    try:
        security_scans['total_scans'] += 1
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file_content = f.read()
        
        if not file_content.strip():
            return threats_found
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            threats_found.append({
                'category': 'file_size',
                'line': 0,
                'content': f'File size {file_size} exceeds limit {MAX_FILE_SIZE}',
                'pattern': 'file_size_exceeded'
            })
        
        # Check for suspicious patterns
        lines = file_content.split('\n')
        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # Check imports
            if any(imp in line_lower for imp in ['import ', 'from ']):
                for sus_import in SUSPICIOUS_IMPORTS:
                    if sus_import in line_lower and 'telebot' not in line_lower:
                        threats_found.append({
                            'category': 'suspicious_imports',
                            'line': i,
                            'content': line.strip()[:100],
                            'pattern': f'import_{sus_import}'
                        })
            
            # Check patterns
            for category, patterns in SUSPICIOUS_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, line_lower, re.IGNORECASE):
                        threats_found.append({
                            'category': category,
                            'line': i,
                            'content': line.strip()[:100],
                            'pattern': pattern
                        })
        
        # Python AST analysis
        if file_path.endswith('.py'):
            try:
                tree = ast.parse(file_content)
                threats_found.extend(analyze_ast(tree))
            except SyntaxError as e:
                threats_found.append({
                    'category': 'syntax_error',
                    'line': e.lineno or 0,
                    'content': str(e)[:100],
                    'pattern': 'syntax_error'
                })
        
        # Check for known malware signatures
        malware_signatures = load_malware_signatures()
        for signature in malware_signatures:
            if signature in file_content:
                threats_found.append({
                    'category': 'malware',
                    'line': 0,
                    'content': f'Known malware signature: {signature[:50]}',
                    'pattern': 'malware_signature'
                })
        
        if threats_found:
            security_scans['threats_found'] += 1
        
    except Exception as e:
        logger.error(f"❌ Error scanning file {file_path}: {e}")
    
    return threats_found

def analyze_ast(tree):
    """Enhanced AST analysis"""
    threats = []
    
    class ThreatVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            try:
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    dangerous_calls = ['exec', 'eval', '__import__', 'compile', 
                                     'system', 'popen', 'call', 'run', 'spawn',
                                     'open', 'file', 'input', 'raw_input']
                    
                    if func_name in dangerous_calls:
                        threats.append({
                            'category': 'dangerous_call',
                            'line': node.lineno if hasattr(node, 'lineno') else 0,
                            'content': f"{func_name}() called",
                            'pattern': f'dangerous_function_{func_name}'
                        })
                
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['open', 'read', 'write', 'remove', 'unlink']:
                        threats.append({
                            'category': 'file_operation',
                            'line': node.lineno if hasattr(node, 'lineno') else 0,
                            'content': f"{node.func.attr}() called",
                            'pattern': f'file_operation_{node.func.attr}'
                        })
            except:
                pass
            self.generic_visit(node)
        
        def visit_Import(self, node):
            for alias in node.names:
                if alias.name in SUSPICIOUS_IMPORTS:
                    threats.append({
                        'category': 'suspicious_import',
                        'line': node.lineno if hasattr(node, 'lineno') else 0,
                        'content': f"import {alias.name}",
                        'pattern': f'import_{alias.name}'
                    })
            self.generic_visit(node)
        
        def visit_ImportFrom(self, node):
            if node.module and node.module in SUSPICIOUS_IMPORTS:
                threats.append({
                    'category': 'suspicious_import',
                    'line': node.lineno if hasattr(node, 'lineno') else 0,
                    'content': f"from {node.module} import ...",
                    'pattern': f'from_{node.module}'
                })
            self.generic_visit(node)
    
    try:
        visitor = ThreatVisitor()
        visitor.visit(tree)
    except:
        pass
    
    return threats

def load_malware_signatures():
    """Load known malware signatures"""
    # In production, this would load from a database or external service
    return [
        'XMrig', 'CryptoNight', 'Monero', 'Stratum',
        'ReverseShell', 'BackConnect', 'Meterpreter'
    ]

def generate_threat_report(threats, user_id, username, file_name, file_path):
    """Generate detailed threat report"""
    if not threats:
        return None
    
    report = {
        'user_id': user_id,
        'username': username or 'Unknown',
        'file_name': file_name,
        'file_path': file_path,
        'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'threat_count': len(threats),
        'threats_by_category': {},
        'high_risk': False,
        'critical_risk': False,
        'risk_score': 0
    }
    
    risk_weights = {
        'source_reading': 10,
        'file_exfiltration': 8,
        'directory_traversal': 7,
        'sensitive_access': 9,
        'obfuscation': 6,
        'backdoor': 10,
        'crypto_mining': 8,
        'ddos_tools': 9,
        'dangerous_call': 7,
        'suspicious_imports': 5
    }
    
    total_score = 0
    for threat in threats:
        category = threat['category']
        if category not in report['threats_by_category']:
            report['threats_by_category'][category] = []
        report['threats_by_category'][category].append(threat)
        
        weight = risk_weights.get(category, 5)
        total_score += weight
        
        if weight >= 9:
            report['critical_risk'] = True
        elif weight >= 7:
            report['high_risk'] = True
    
    report['risk_score'] = min(100, total_score)
    
    return report

def log_security_event(user_id, username, file_name, threat_count, risk_level, action_taken, details=None):
    """Log security event to database"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO security_logs 
                     (user_id, username, file_name, threat_count, risk_level, action_taken, details)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, username, file_name, threat_count, risk_level, action_taken, details))
        conn.commit()
    except Exception as e:
        logger.error(f"❌ Error logging security event: {e}")
    finally:
        conn.close()

# --- Database helper functions ---
def save_user(user_id, username, first_name, last_name):
    """Save user with enhanced fields"""
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            c.execute('''INSERT OR REPLACE INTO users 
                        (user_id, username, first_name, last_name, last_active, storage_used)
                        VALUES (?, ?, ?, ?, ?, 
                                COALESCE((SELECT storage_used FROM users WHERE user_id = ?), 0))''',
                      (user_id, username, first_name, last_name, datetime.now().isoformat(), user_id))
            conn.commit()
        except Exception as e:
            logger.error(f"❌ Error saving user: {e}")
        finally:
            conn.close()

def save_user_file(user_id, file_name, file_type='unknown', file_path='', pending=False):
    """Save user file with metadata"""
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            c.execute('SELECT username, first_name FROM users WHERE user_id = ?', (user_id,))
            user_info = c.fetchone()
            username = user_info[0] if user_info else None
            
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            checksum = hashlib.sha256(open(file_path, 'rb').read()).hexdigest() if os.path.exists(file_path) else ''
            
            c.execute('''INSERT INTO user_files 
                        (user_id, username, chat_id, file_name, file_type, file_path, 
                         original_filename, file_size, is_pending, checksum, upload_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (user_id, username, user_id, file_name, file_type, file_path,
                      file_name, file_size, 1 if pending else 0, checksum, datetime.now().isoformat()))
            
            # Update user stats
            c.execute('''UPDATE users SET total_uploads = total_uploads + 1,
                        storage_used = storage_used + ?
                        WHERE user_id = ?''', (file_size, user_id))
            
            conn.commit()
            
            if not pending:
                if user_id not in user_files:
                    user_files[user_id] = []
                user_files[user_id].append((file_name, file_type, file_path))
            
            logger.info(f"✅ File saved for user {user_id}: {file_name}")
            
        except Exception as e:
            logger.error(f"❌ Error saving file: {e}")
        finally:
            conn.close()

def approve_pending_file(user_id, file_name):
    """Approve pending file"""
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            c.execute('UPDATE user_files SET is_pending = 0 WHERE user_id = ? AND file_name = ?',
                     (user_id, file_name))
            
            c.execute('SELECT file_type, file_path FROM user_files WHERE user_id = ? AND file_name = ?',
                     (user_id, file_name))
            result = c.fetchone()
            
            if result:
                file_type, file_path = result
                if user_id not in user_files:
                    user_files[user_id] = []
                user_files[user_id].append((file_name, file_type, file_path))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Error approving file: {e}")
            return False
        finally:
            conn.close()

def remove_user_file_db(user_id, file_name):
    """Remove user file and update stats"""
    file_path = None
    file_size = 0
    
    if user_id in user_files:
        for fn, ft, fp in user_files[user_id]:
            if fn == file_name:
                file_path = fp
                if os.path.exists(fp):
                    file_size = os.path.getsize(fp)
                break
    
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            if not file_path:
                c.execute('SELECT file_path, file_size FROM user_files WHERE user_id = ? AND file_name = ?',
                         (user_id, file_name))
                result = c.fetchone()
                if result:
                    file_path, file_size = result
            
            c.execute('DELETE FROM user_files WHERE user_id = ? AND file_name = ?', (user_id, file_name))
            
            if file_size > 0:
                c.execute('UPDATE users SET storage_used = storage_used - ? WHERE user_id = ?',
                         (file_size, user_id))
            
            conn.commit()
            
            if user_id in user_files:
                user_files[user_id] = [f for f in user_files[user_id] if f[0] != file_name]
                if not user_files[user_id]:
                    del user_files[user_id]
            
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.error(f"❌ Error deleting file: {e}")
            
        except Exception as e:
            logger.error(f"❌ Error removing file: {e}")
        finally:
            conn.close()

def add_active_user(user_id):
    """Add user to active users"""
    active_users.add(user_id)
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            c.execute('INSERT OR IGNORE INTO active_users (user_id) VALUES (?)', (user_id,))
            conn.commit()
        except Exception as e:
            logger.error(f"❌ Error adding active user: {e}")
        finally:
            conn.close()

def save_subscription(user_id, expiry, file_limit=999):
    """Save subscription"""
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            expiry_str = expiry.isoformat()
            c.execute('INSERT OR REPLACE INTO subscriptions (user_id, expiry, file_limit) VALUES (?, ?, ?)',
                     (user_id, expiry_str, file_limit))
            conn.commit()
            user_subscriptions[user_id] = {'expiry': expiry, 'file_limit': file_limit}
        except Exception as e:
            logger.error(f"❌ Error saving subscription: {e}")
        finally:
            conn.close()

def add_notification(user_id, title, message, type='info'):
    """Add notification for user"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO notifications (user_id, title, message, type)
                     VALUES (?, ?, ?, ?)''', (user_id, title, message, type))
        conn.commit()
    except Exception as e:
        logger.error(f"❌ Error adding notification: {e}")
    finally:
        conn.close()

def get_user_notifications(user_id):
    """Get user notifications"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''SELECT notification_id, title, message, type, is_read, created_date
                     FROM notifications WHERE user_id = ? ORDER BY created_date DESC LIMIT 50''',
                  (user_id,))
        return c.fetchall()
    finally:
        conn.close()

def mark_notification_read(user_id, notification_id):
    """Mark notification as read"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ? AND notification_id = ?',
                 (user_id, notification_id))
        conn.commit()
    finally:
        conn.close()

# --- Key Management ---
def generate_subscription_key(days, max_uses=1, file_limit=999, created_by=None, key_type='premium', price=None):
    """Generate subscription key with enhanced options"""
    part1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    part3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    key = f"KELVIN-{part1}-{part2}-{part3}"
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO subscription_keys 
                 (key_value, days_valid, max_uses, file_limit, created_by, key_type, price)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (key, days, max_uses, file_limit, created_by, key_type, price))
    conn.commit()
    conn.close()
    
    return key

def redeem_subscription_key(key_value, user_id, ip_address=None, user_agent=None):
    """Redeem subscription key with tracking"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''SELECT days_valid, max_uses, used_count, file_limit, is_active, used_by_user, key_type
                     FROM subscription_keys WHERE key_value = ?''', (key_value,))
        key_data = c.fetchone()
        
        if not key_data:
            return False, "❌ Invalid Key"
        
        days_valid, max_uses, used_count, file_limit, is_active, used_by_user, key_type = key_data
        
        if is_active != 1:
            return False, "❌ Key Inactive"
        
        if used_count >= max_uses:
            return False, f"❌ Key Already Used ({used_count}/{max_uses} uses)"
        
        if used_by_user and used_by_user != user_id:
            return False, "❌ Key already assigned to another user"
        
        # Check if user already has a key
        c.execute('SELECT key_used FROM users WHERE user_id = ?', (user_id,))
        user_key = c.fetchone()
        
        if user_key and user_key[0]:
            return False, "❌ You already have an active key"
        
        # Calculate new expiry
        current_expiry = user_subscriptions.get(user_id, {}).get('expiry', datetime.now())
        if current_expiry < datetime.now():
            current_expiry = datetime.now()
        
        new_expiry = current_expiry + timedelta(days=days_valid)
        
        # Save subscription
        save_subscription(user_id, new_expiry, file_limit)
        
        # Update key usage
        current_time = datetime.now().isoformat()
        c.execute('''UPDATE subscription_keys 
                     SET used_count = used_count + 1,
                         used_by_user = ?,
                         used_date = ?
                     WHERE key_value = ?''',
                  (user_id, current_time, key_value))
        
        # Insert key usage
        c.execute('''INSERT INTO key_usage (key_value, user_id, ip_address, user_agent, used_date)
                     VALUES (?, ?, ?, ?, ?)''',
                  (key_value, user_id, ip_address, user_agent, current_time))
        
        # Update user
        c.execute('''UPDATE users 
                     SET key_used = ?,
                         key_used_date = ?
                     WHERE user_id = ?''',
                  (key_value, current_time, user_id))
        
        conn.commit()
        
        # Notify admin
        try:
            user_info = bot.get_chat(user_id)
            admin_msg = f"""
💳 **NEW PREMIUM ACTIVATION**

👤 **User:** {user_info.first_name} (@{user_info.username})
🆔 **ID:** `{user_id}`
🔑 **Key:** `{key_value}`
📅 **Duration:** {days_valid} Days
🗃 **Files:** {file_limit}
⏳ **Expires:** {new_expiry.strftime('%Y-%m-%d %H:%M:%S')}
🔢 **Usage:** {used_count + 1}/{max_uses}
📱 **IP:** {ip_address or 'N/A'}
"""
            bot.send_message(OWNER_ID, admin_msg, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"❌ Failed to notify admin: {e}")
        
        return True, f"""
✨ **PREMIUM ACTIVATED!** ✨

🔑 **Key:** `{key_value}`
📅 **Duration:** {days_valid} Days
🗃 **File Limit:** {file_limit}
⏳ **Expires:** {new_expiry.strftime('%Y-%m-%d %H:%M:%S')}

✅ Your account has been upgraded to {key_type.upper()}
"""
    
    except Exception as e:
        return False, f"❌ Error: {str(e)}"
    finally:
        conn.close()

def get_all_subscription_keys():
    """Get all subscription keys"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''SELECT key_value, days_valid, max_uses, used_count, file_limit, 
                        created_date, key_type, price, is_active
                 FROM subscription_keys ORDER BY created_date DESC''')
    keys = c.fetchall()
    conn.close()
    return keys

def delete_subscription_key(key_value):
    """Delete subscription key and remove premium status"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Get users who used this key
    c.execute('SELECT user_id FROM key_usage WHERE key_value = ?', (key_value,))
    users = c.fetchall()
    
    for (user_id,) in users:
        # Remove subscription
        if user_id in user_subscriptions:
            del user_subscriptions[user_id]
        c.execute('DELETE FROM subscriptions WHERE user_id = ?', (user_id,))
        
        # Update user
        c.execute('UPDATE users SET key_used = NULL, key_used_date = NULL WHERE user_id = ?', (user_id,))
        
        try:
            bot.send_message(user_id, "⚠️ **Your Premium Access has been Revoked**\n\nThe key you used has been deactivated.")
        except:
            pass
    
    # Delete key
    c.execute('DELETE FROM subscription_keys WHERE key_value = ?', (key_value,))
    c.execute('DELETE FROM key_usage WHERE key_value = ?', (key_value,))
    
    conn.commit()
    conn.close()

def get_key_stats():
    """Get statistics about keys"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM subscription_keys')
    total_keys = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM subscription_keys WHERE is_active = 1')
    active_keys = c.fetchone()[0]
    
    c.execute('SELECT SUM(used_count) FROM subscription_keys')
    total_used = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(DISTINCT used_by_user) FROM subscription_keys WHERE used_by_user IS NOT NULL')
    unique_users = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_keys': total_keys,
        'active_keys': active_keys,
        'total_used': total_used,
        'unique_users': unique_users
    }

# --- Bot Statistics ---
def get_bot_statistics():
    """Get comprehensive bot statistics"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Basic stats
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    
    active_files = 0
    for script_key in bot_scripts:
        if is_bot_running(int(script_key.split('_')[0]), bot_scripts[script_key]['file_name']):
            active_files += 1
    
    premium_users = sum(1 for user_id in active_users if is_premium_user(user_id))
    
    # Database stats
    c.execute('SELECT COUNT(*) FROM security_logs')
    security_alerts = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM banned_users')
    banned_users = c.fetchone()[0]
    
    c.execute('SELECT SUM(file_size) FROM user_files')
    total_storage = c.fetchone()[0] or 0
    
    c.execute('SELECT SUM(downloads) FROM user_files')
    total_downloads = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(*) FROM api_keys')
    total_api_keys = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM webhooks')
    total_webhooks = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM notifications WHERE is_read = 0')
    unread_notifications = c.fetchone()[0]
    
    conn.close()
    
    # System stats
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    uptime = time.time() - start_time
    
    return {
        'total_users': total_users,
        'total_files': total_files,
        'active_files': active_files,
        'premium_users': premium_users,
        'security_alerts': security_alerts,
        'banned_users': banned_users,
        'total_storage': format_file_size(total_storage),
        'total_downloads': total_downloads,
        'total_api_keys': total_api_keys,
        'total_webhooks': total_webhooks,
        'unread_notifications': unread_notifications,
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_used': format_file_size(memory.used),
        'memory_total': format_file_size(memory.total),
        'disk_percent': disk.percent,
        'disk_used': format_file_size(disk.used),
        'disk_total': format_file_size(disk.total),
        'uptime': str(timedelta(seconds=int(uptime))),
        'security_scans': security_scans
    }

def get_user_statistics(user_id):
    """Get statistics for specific user"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    c.execute('''SELECT total_uploads, total_downloads, bandwidth_used, storage_used, join_date
                 FROM users WHERE user_id = ?''', (user_id,))
    user_stats = c.fetchone()
    
    c.execute('SELECT COUNT(*) FROM user_files WHERE user_id = ?', (user_id,))
    total_files = c.fetchone()[0]
    
    c.execute('SELECT SUM(downloads) FROM user_files WHERE user_id = ?', (user_id,))
    total_downloads = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(*) FROM user_files WHERE is_active = 1 AND user_id = ?', (user_id,))
    active_files = c.fetchone()[0]
    
    conn.close()
    
    if user_stats:
        return {
            'total_uploads': user_stats[0],
            'total_downloads': user_stats[1],
            'bandwidth_used': format_file_size(user_stats[2]),
            'storage_used': format_file_size(user_stats[3]),
            'join_date': user_stats[4][:10],
            'current_files': total_files,
            'file_downloads': total_downloads,
            'active_files': active_files
        }
    return None

def get_all_users_details():
    """Get details of all users"""
    users_list = []
    for user_id in active_users:
        try:
            chat = bot.get_chat(user_id)
            users_list.append({
                'user_id': user_id,
                'first_name': chat.first_name,
                'username': chat.username,
                'is_premium': is_premium_user(user_id)
            })
        except:
            users_list.append({
                'user_id': user_id,
                'first_name': 'Unknown',
                'username': None,
                'is_premium': is_premium_user(user_id)
            })
    return users_list

def get_premium_users_details():
    """Get details of premium users"""
    premium_users = []
    for user_id in active_users:
        if is_premium_user(user_id):
            try:
                chat = bot.get_chat(user_id)
                user_files_list = user_files.get(user_id, [])
                running_files = sum(1 for file_name, _, _ in user_files_list if is_bot_running(user_id, file_name))
                subscription_info = user_subscriptions.get(user_id, {})
                file_limit = subscription_info.get('file_limit', PREMIUM_USER_LIMIT)
                
                premium_users.append({
                    'user_id': user_id,
                    'first_name': chat.first_name,
                    'username': chat.username,
                    'file_count': len(user_files_list),
                    'file_limit': file_limit,
                    'running_files': running_files,
                    'expiry': subscription_info['expiry']
                })
            except Exception as e:
                logger.error(f"❌ Error getting user details: {e}")
    
    return premium_users

def get_all_admins():
    """Get all admin IDs"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id, role FROM admins')
    admins = c.fetchall()
    conn.close()
    return admins

def add_admin_to_db(admin_id, role='admin', added_by=None):
    """Add admin to database"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT OR IGNORE INTO admins (user_id, role, added_by) VALUES (?, ?, ?)',
                  (admin_id, role, added_by))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"❌ Error adding admin: {e}")
        return False
    finally:
        conn.close()

def remove_admin_from_db(admin_id):
    """Remove admin from database"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('DELETE FROM admins WHERE user_id = ?', (admin_id,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"❌ Error removing admin: {e}")
        return False
    finally:
        conn.close()

# --- Ban Management ---
def ban_user(user_id, reason=None, ban_type='permanent', ban_expiry=None):
    """Ban user with options"""
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            # Check if already banned
            c.execute('SELECT user_id FROM banned_users WHERE user_id = ?', (user_id,))
            if c.fetchone():
                return False, "User already banned"
            
            # Insert ban record
            c.execute('''INSERT INTO banned_users 
                        (user_id, banned_by, reason, ban_type, ban_expiry)
                        VALUES (?, ?, ?, ?, ?)''',
                     (user_id, OWNER_ID, reason, ban_type, ban_expiry))
            
            # Remove from active users
            c.execute('DELETE FROM active_users WHERE user_id = ?', (user_id,))
            if user_id in active_users:
                active_users.remove(user_id)
            
            # Stop all processes
            cleanup_user_processes(user_id)
            
            # Get user files
            c.execute('SELECT file_path FROM user_files WHERE user_id = ?', (user_id,))
            files = c.fetchall()
            for file_path, in files:
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass
            
            # Delete user data
            c.execute('DELETE FROM user_files WHERE user_id = ?', (user_id,))
            c.execute('DELETE FROM subscriptions WHERE user_id = ?', (user_id,))
            c.execute('DELETE FROM api_keys WHERE user_id = ?', (user_id,))
            c.execute('DELETE FROM webhooks WHERE user_id = ?', (user_id,))
            
            # Remove from memory
            if user_id in user_files:
                del user_files[user_id]
            if user_id in user_subscriptions:
                del user_subscriptions[user_id]
            
            conn.commit()
            
            # Notify user
            try:
                ban_msg = f"""
🚫 **YOU HAVE BEEN BANNED**

⚠️ Your access has been revoked
"""
                if reason:
                    ban_msg += f"📝 **Reason:** {reason}\n"
                if ban_type == 'temporary' and ban_expiry:
                    ban_msg += f"⏳ **Ban expires:** {ban_expiry[:16]}"
                else:
                    ban_msg += "⏳ **Ban type:** Permanent"
                ban_msg += f"\n\n👑 **Contact:** {YOUR_USERNAME}"
                
                bot.send_message(user_id, ban_msg, parse_mode='Markdown')
            except:
                pass
            
            return True, "User banned successfully"
            
        except Exception as e:
            logger.error(f"❌ Error banning user: {e}")
            return False, f"Error: {str(e)}"
        finally:
            conn.close()

def unban_user(user_id):
    """Unban user"""
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        try:
            c.execute('DELETE FROM banned_users WHERE user_id = ?', (user_id,))
            
            c.execute('INSERT OR IGNORE INTO active_users (user_id) VALUES (?)', (user_id,))
            active_users.add(user_id)
            
            conn.commit()
            
            # Notify user
            try:
                bot.send_message(user_id,
                               f"""
✅ **YOU HAVE BEEN UNBANNED**

✨ Your access has been restored
Use /start to begin again
                               """,
                               parse_mode='Markdown')
            except:
                pass
            
            return True, "User unbanned successfully"
        except Exception as e:
            logger.error(f"❌ Error unbanning user: {e}")
            return False, f"Error: {str(e)}"
        finally:
            conn.close()

def get_banned_users():
    """Get all banned users"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''SELECT bu.user_id, bu.ban_date, bu.reason, bu.ban_type, bu.ban_expiry,
                            u.username, u.first_name
                     FROM banned_users bu
                     LEFT JOIN users u ON bu.user_id = u.user_id
                     ORDER BY bu.ban_date DESC''')
        return c.fetchall()
    finally:
        conn.close()

# --- File Management ---
def format_file_size(size_bytes):
    """Format file size"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def get_user_file_limit(user_id):
    """Get user file limit"""
    if user_id == OWNER_ID:
        return OWNER_LIMIT
    if user_id in admin_ids:
        return ADMIN_LIMIT
    if is_premium_user(user_id):
        subscription_info = user_subscriptions.get(user_id, {})
        return subscription_info.get('file_limit', PREMIUM_USER_LIMIT)
    return FREE_USER_LIMIT

def get_user_file_count(user_id):
    """Get user file count"""
    return len(user_files.get(user_id, []))

def is_premium_user(user_id):
    """Check if user is premium"""
    if user_id in user_subscriptions:
        expiry = user_subscriptions[user_id]['expiry']
        return expiry > datetime.now()
    return False

def get_user_status(user_id):
    """Get user status"""
    if user_id == OWNER_ID:
        return "👑 System Owner"
    if user_id in admin_ids:
        return "🛡️ Administrator"
    if is_premium_user(user_id):
        return "💎 Premium"
    return "👤 Standard User"

def get_user_folder(user_id):
    """Get user folder"""
    user_folder = os.path.join(UPLOAD_BOTS_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def get_user_files_with_details(user_id):
    """Get user files with details"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''SELECT file_id, file_name, file_type, file_path, 
                            original_filename, file_size, upload_date, is_active, downloads
                     FROM user_files 
                     WHERE user_id = ? AND is_pending = 0
                     ORDER BY upload_date DESC''', (user_id,))
        files = c.fetchall()
        
        file_details = []
        for file in files:
            file_id, file_name, file_type, file_path, original_filename, file_size, upload_date, is_active, downloads = file
            
            file_details.append({
                'file_id': file_id,
                'file_name': file_name,
                'file_type': file_type,
                'file_path': file_path,
                'original_filename': original_filename,
                'file_size': format_file_size(file_size),
                'upload_date': upload_date[:16],
                'is_active': bool(is_active),
                'is_running': is_bot_running(user_id, file_name),
                'downloads': downloads
            })
        
        return file_details
    except Exception as e:
        logger.error(f"❌ Error getting user files: {e}")
        return []
    finally:
        conn.close()

def get_all_user_files_for_owner():
    """Get all files for owner"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''SELECT u.user_id, u.username, u.first_name, 
                            f.file_name, f.file_type, f.file_size, f.upload_date, 
                            f.is_active, f.is_pending, f.downloads
                     FROM user_files f
                     JOIN users u ON f.user_id = u.user_id
                     ORDER BY f.upload_date DESC''')
        return c.fetchall()
    finally:
        conn.close()

def get_user_by_key(key_value):
    """Get user by key"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''SELECT u.user_id, u.username, u.first_name, u.key_used_date,
                            k.days_valid, k.file_limit, k.used_date, k.key_type
                     FROM users u
                     JOIN subscription_keys k ON u.key_used = k.key_value
                     WHERE u.key_used = ?''', (key_value,))
        user = c.fetchone()
        
        if user:
            return {
                'user_id': user[0],
                'username': user[1],
                'first_name': user[2],
                'key_used_date': user[3][:16] if user[3] else None,
                'days_valid': user[4],
                'file_limit': user[5],
                'key_activation_date': user[6][:16] if user[6] else None,
                'key_type': user[7]
            }
        return None
    finally:
        conn.close()

# --- Process Management ---
def is_bot_running(user_id, file_name):
    """Check if bot is running"""
    script_key = f"{user_id}_{file_name}"
    script_info = bot_scripts.get(script_key)
    if script_info and script_info.get('process'):
        try:
            proc = psutil.Process(script_info['process'].pid)
            return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            return False
    return False

def kill_process_tree(process_info):
    """Kill process tree"""
    try:
        process = process_info.get('process')
        if process and hasattr(process, 'pid'):
            pid = process.pid
            try:
                parent = psutil.Process(pid)
                
                # Kill children first
                try:
                    children = parent.children(recursive=True)
                    for child in children:
                        try:
                            child.terminate()
                        except:
                            pass
                    
                    time.sleep(1)
                    
                    for child in children:
                        try:
                            if child.is_running():
                                child.kill()
                        except:
                            pass
                except:
                    pass
                
                # Kill parent
                try:
                    parent.terminate()
                    parent.wait(timeout=5)
                except:
                    pass
                
                try:
                    if parent.is_running():
                        parent.kill()
                except:
                    pass
                
            except psutil.NoSuchProcess:
                pass
            
            # Kill using process object
            try:
                if process.poll() is None:
                    process.terminate()
                    time.sleep(2)
                    if process.poll() is None:
                        process.kill()
            except:
                pass
            
            # Close log file
            if process_info.get('log_file'):
                try:
                    process_info['log_file'].close()
                except:
                    pass
                
    except Exception as e:
        logger.error(f"❌ Error killing process: {e}")

def force_cleanup_process(process_info):
    """Force cleanup process"""
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            kill_process_tree(process_info)
            
            if process_info.get('process'):
                try:
                    pid = process_info['process'].pid
                    psutil.Process(pid)
                    time.sleep(1)
                    continue
                except psutil.NoSuchProcess:
                    return True
            
            return True
            
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)
    
    return False

def cleanup_user_processes(user_id):
    """Clean up all processes for user"""
    keys_to_remove = []
    for script_key, process_info in list(bot_scripts.items()):
        if script_key.startswith(f"{user_id}_"):
            if force_cleanup_process(process_info):
                keys_to_remove.append(script_key)
    
    for key in keys_to_remove:
        if key in bot_scripts:
            del bot_scripts[key]
    
    return len(keys_to_remove)

def cleanup_zombie_processes():
    """Clean up zombie processes"""
    for script_key in list(bot_scripts.keys()):
        try:
            script_info = bot_scripts.get(script_key)
            if script_info and script_info.get('process'):
                pid = script_info['process'].pid
                try:
                    proc = psutil.Process(pid)
                    if not proc.is_running() or proc.status() == psutil.STATUS_ZOMBIE:
                        if script_info.get('log_file'):
                            try:
                                script_info['log_file'].close()
                            except:
                                pass
                        if script_key in bot_scripts:
                            del bot_scripts[script_key]
                except psutil.NoSuchProcess:
                    if script_key in bot_scripts:
                        if script_info.get('log_file'):
                            try:
                                script_info['log_file'].close()
                            except:
                                pass
                        del bot_scripts[script_key]
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")

# --- Script Execution ---
TELEGRAM_MODULES = {
    'telebot': 'pyTelegramBotAPI',
    'telegram': 'python-telegram-bot',
    'python_telegram_bot': 'python-telegram-bot',
    'aiogram': 'aiogram',
    'pyrogram': 'pyrogram',
    'telethon': 'telethon',
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'pillow': 'Pillow',
    'cv2': 'opencv-python',
    'yaml': 'PyYAML',
    'dotenv': 'python-dotenv',
    'dateutil': 'python-dateutil',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'flask': 'Flask',
    'django': 'Django',
    'sqlalchemy': 'SQLAlchemy',
    'psutil': 'psutil',
    'asyncio': None,
    'json': None,
    'datetime': None,
    'os': None,
    'sys': None,
    're': None,
    'time': None,
    'math': None,
    'random': None,
    'logging': None,
    'threading': None,
    'subprocess': None,
    'zipfile': None,
    'tempfile': None,
    'shutil': None,
    'sqlite3': None,
    'hashlib': None,
    'hmac': None,
    'secrets': None,
    'functools': None,
    'collections': None,
    'itertools': None,
    'fractions': None,
    'decimal': None
}

def attempt_install_pip(module_name, message):
    """Attempt to install pip package"""
    package_name = TELEGRAM_MODULES.get(module_name.lower(), module_name)
    if package_name is None:
        return False
    
    try:
        try:
            bot.send_message(message.from_user.id, f"🔧 Installing `{package_name}`...", parse_mode='Markdown')
        except Exception as e:
            logger.error(f"❌ Failed to send install message: {e}")
            return False
        
        command = [sys.executable, '-m', 'pip', 'install', package_name, '--timeout', '60', '--retries', '3']
        logger.info(f"🔨 Running install: {' '.join(command)}")
        
        result = subprocess.run(command, capture_output=True, text=True, check=False, 
                              encoding='utf-8', errors='ignore', timeout=120)
        
        if result.returncode == 0:
            logger.info(f"✅ Installed {package_name}")
            try:
                bot.send_message(message.from_user.id, f"✅ Installed `{package_name}`", parse_mode='Markdown')
            except Exception as e:
                logger.error(f"❌ Failed to send success message: {e}")
            return True
        else:
            error_msg = f"❌ Failed `{package_name}`\n```\n{result.stderr or result.stdout}\n```"
            logger.error(error_msg)
            if len(error_msg) > 4000:
                error_msg = error_msg[:4000] + "\n... (Truncated)"
            try:
                bot.send_message(message.from_user.id, error_msg, parse_mode='Markdown')
            except Exception as e:
                logger.error(f"❌ Failed to send error message: {e}")
            return False
            
    except subprocess.TimeoutExpired:
        error_msg = f"❌ Timeout `{package_name}`"
        logger.error(error_msg)
        try:
            bot.send_message(message.from_user.id, error_msg)
        except:
            pass
        return False
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        try:
            bot.send_message(message.from_user.id, error_msg)
        except:
            pass
        return False

def attempt_install_npm(module_name, user_folder, message):
    """Attempt to install npm package"""
    try:
        try:
            bot.send_message(message.from_user.id, f"📦 Installing `{module_name}`...", parse_mode='Markdown')
        except Exception as e:
            logger.error(f"❌ Failed to send install message: {e}")
            return False
        
        command = ['npm', 'install', module_name, '--save', '--no-audit', '--no-fund']
        logger.info(f"🔨 Running npm install: {' '.join(command)} in {user_folder}")
        
        result = subprocess.run(command, capture_output=True, text=True, check=False,
                              cwd=user_folder, encoding='utf-8', errors='ignore', timeout=120)
        
        if result.returncode == 0:
            logger.info(f"✅ Installed {module_name}")
            try:
                bot.send_message(message.from_user.id, f"✅ Installed `{module_name}`", parse_mode='Markdown')
            except Exception as e:
                logger.error(f"❌ Failed to send success message: {e}")
            return True
        else:
            error_msg = f"❌ Failed `{module_name}`\n```\n{result.stderr or result.stdout}\n```"
            logger.error(error_msg)
            if len(error_msg) > 4000:
                error_msg = error_msg[:4000] + "\n... (Truncated)"
            try:
                bot.send_message(message.from_user.id, error_msg, parse_mode='Markdown')
            except Exception as e:
                logger.error(f"❌ Failed to send error message: {e}")
            return False
            
    except FileNotFoundError:
        error_msg = "❌ Node.js not found"
        logger.error(error_msg)
        try:
            bot.send_message(message.from_user.id, error_msg)
        except:
            pass
        return False
    except subprocess.TimeoutExpired:
        error_msg = f"❌ Timeout `{module_name}`"
        logger.error(error_msg)
        try:
            bot.send_message(message.from_user.id, error_msg)
        except:
            pass
        return False
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        try:
            bot.send_message(message.from_user.id, error_msg)
        except:
            pass
        return False

def run_script(script_path, script_owner_id, user_folder, file_name, message_obj_for_reply, attempt=1):
    """Run Python script"""
    max_attempts = 2
    if attempt > max_attempts:
        try:
            bot.send_message(script_owner_id, f"❌ Failed to start `{file_name}`")
        except:
            pass
        return

    script_key = f"{script_owner_id}_{file_name}"
    logger.info(f"Attempt {attempt} to run Python script: {script_path}")

    try:
        if not os.path.exists(script_path):
            try:
                bot.send_message(script_owner_id, f"❌ File `{file_name}` not found", parse_mode='Markdown')
            except:
                pass
            return

        if attempt == 1:
            check_command = [sys.executable, script_path]
            logger.info(f"🔍 Running Python pre-check: {' '.join(check_command)}")
            check_proc = None
            try:
                check_proc = subprocess.Popen(check_command, cwd=user_folder, 
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            text=True, encoding='utf-8', errors='ignore')
                stdout, stderr = check_proc.communicate(timeout=10)
                return_code = check_proc.returncode
                logger.info(f"🔍 Python pre-check. rc: {return_code}")
                
                if return_code != 0 and stderr:
                    match_py = re.search(r"ModuleNotFoundError: No module named '(.+?)'", stderr)
                    if match_py:
                        module_name = match_py.group(1).strip().strip("'\"")
                        logger.info(f"📦 Detected missing Python module: {module_name}")
                        
                        try:
                            bot.send_message(script_owner_id, f"🔧 Installing `{module_name}`...")
                        except:
                            pass
                        
                        if attempt_install_pip(module_name, message_obj_for_reply):
                            logger.info(f"✅ Install ok for {module_name}. Retrying...")
                            try:
                                bot.send_message(script_owner_id, f"⚡ Restarting `{file_name}`...")
                            except:
                                pass
                            time.sleep(2)
                            threading.Thread(target=run_script, 
                                           args=(script_path, script_owner_id, user_folder, 
                                                file_name, message_obj_for_reply, attempt + 1)).start()
                            return
                        else:
                            try:
                                bot.send_message(script_owner_id, 
                                               f"❌ Cannot run `{file_name}` - installation failed")
                            except:
                                pass
                            return
            except subprocess.TimeoutExpired:
                logger.info("⏱️ Python pre-check timed out, imports likely ok.")
                if check_proc and check_proc.poll() is None:
                    check_proc.kill()
                    check_proc.communicate()
            except Exception as e:
                logger.error(f"❌ Error in Python pre-check: {e}")
                return

        logger.info(f"🚀 Starting Python process for {script_key}")
        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = None
        process = None
        
        try:
            log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"❌ Failed to open log file: {e}")
            try:
                bot.send_message(script_owner_id, f"❌ Log file error for `{file_name}`")
            except:
                pass
            return
            
        try:
            startupinfo = None
            creationflags = 0
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
            process = subprocess.Popen(
                [sys.executable, script_path],
                cwd=user_folder,
                stdout=log_file,
                stderr=log_file,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo,
                creationflags=creationflags,
                encoding='utf-8',
                errors='ignore',
                bufsize=1
            )
            
            logger.info(f"✅ Started Python process {process.pid} for {script_key}")
            bot_scripts[script_key] = {
                'process': process,
                'log_file': log_file,
                'file_name': file_name,
                'chat_id': script_owner_id,
                'script_owner_id': script_owner_id,
                'start_time': datetime.now(),
                'user_folder': user_folder,
                'type': 'py',
                'script_key': script_key,
                'pid': process.pid
            }
            
            try:
                bot.send_message(script_owner_id, 
                               f"✅ `{file_name}` Running (PID: {process.pid})",
                               parse_mode='Markdown')
            except Exception as e:
                logger.error(f"❌ Failed to send success message: {e}")
                
            try:
                bot.delete_message(message_obj_for_reply.chat.id, message_obj_for_reply.message_id)
            except:
                pass
                
        except Exception as e:
            if log_file and not log_file.closed:
                log_file.close()
            error_msg = f"❌ Error starting `{file_name}`: {str(e)[:100]}"
            logger.error(error_msg, exc_info=True)
            try:
                bot.send_message(script_owner_id, error_msg, parse_mode='Markdown')
            except:
                pass
            if script_key in bot_scripts:
                del bot_scripts[script_key]
                
    except Exception as e:
        error_msg = f"❌ Error with `{file_name}`: {str(e)[:100]}"
        logger.error(error_msg, exc_info=True)
        try:
            bot.send_message(script_owner_id, error_msg, parse_mode='Markdown')
        except:
            pass

def run_js_script(script_path, script_owner_id, user_folder, file_name, message_obj_for_reply, attempt=1):
    """Run JavaScript script"""
    max_attempts = 2
    if attempt > max_attempts:
        try:
            bot.send_message(script_owner_id, f"❌ Failed to start `{file_name}`", parse_mode='Markdown')
        except:
            pass
        return

    script_key = f"{script_owner_id}_{file_name}"
    logger.info(f"Attempt {attempt} to run JS script: {script_path}")

    current_env = os.environ.copy()
    node_bin_path = os.path.join(user_folder, 'node_modules', '.bin')
    if 'PATH' in current_env:
        current_env['PATH'] = node_bin_path + os.pathsep + current_env['PATH']
    else:
        current_env['PATH'] = node_bin_path
    
    node_modules_path = os.path.join(user_folder, 'node_modules')
    current_env['NODE_PATH'] = node_modules_path

    try:
        if not os.path.exists(script_path):
            try:
                bot.send_message(script_owner_id, f"❌ File `{file_name}` not found", parse_mode='Markdown')
            except:
                pass
            return

        # Check Node.js
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True, timeout=10)
        except (subprocess.CalledProcessError, FileNotFoundError):
            bot.send_message(script_owner_id, "❌ Node.js is not installed", parse_mode='Markdown')
            return
        except subprocess.TimeoutExpired:
            bot.send_message(script_owner_id, "❌ Node.js check timed out", parse_mode='Markdown')
            return

        # Check package.json
        package_json_path = os.path.join(user_folder, 'package.json')
        if os.path.exists(package_json_path) and attempt == 1:
            logger.info(f"📦 Found package.json in {user_folder}")
            try:
                if not os.path.exists(node_modules_path):
                    status_msg = bot.send_message(script_owner_id, 
                                                f"📦 Installing dependencies from package.json...\nThis may take a few minutes...",
                                                parse_mode='Markdown')
                    
                    install_process = subprocess.run(
                        ['npm', 'install', '--no-audit', '--no-fund'],
                        cwd=user_folder,
                        capture_output=True,
                        text=True,
                        env=current_env,
                        timeout=300
                    )
                    
                    if install_process.returncode == 0:
                        logger.info(f"✅ npm install completed successfully")
                        bot.edit_message_text(
                            f"✅ Dependencies installed successfully\nRestarting {file_name}...",
                            status_msg.chat.id,
                            status_msg.message_id,
                            parse_mode='Markdown'
                        )
                        time.sleep(2)
                        threading.Thread(target=run_js_script, 
                                       args=(script_path, script_owner_id, user_folder, 
                                            file_name, message_obj_for_reply, attempt + 1)).start()
                        return
                    else:
                        error_msg = install_process.stderr[:200] if install_process.stderr else "Unknown error"
                        logger.error(f"❌ npm install failed: {error_msg}")
                        bot.edit_message_text(
                            f"❌ Failed to install dependencies:\n```\n{error_msg}\n```",
                            status_msg.chat.id,
                            status_msg.message_id,
                            parse_mode='Markdown'
                        )
            except subprocess.TimeoutExpired:
                logger.error("❌ npm install timed out")
                bot.send_message(script_owner_id, 
                               "❌ npm install timed out after 5 minutes.\nTry installing manually or check your package.json",
                               parse_mode='Markdown')
                return
            except Exception as e:
                logger.error(f"❌ Error during npm install: {e}")
                bot.send_message(script_owner_id, f"❌ Error during npm install: {str(e)[:100]}", parse_mode='Markdown')

        if attempt == 1:
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                require_pattern = r"require\(['\"]([^'\"]+)['\"]\)"
                imports = re.findall(require_pattern, content)
                
                import_pattern = r"from\s+['\"]([^'\"]+)['\"]"
                imports += re.findall(import_pattern, content)
                
                core_modules = ['fs', 'path', 'http', 'https', 'url', 'util', 'events',
                               'stream', 'crypto', 'zlib', 'os', 'child_process', 'buffer',
                               'timers/promises', 'worker_threads', 'perf_hooks']
                
                builtin_patterns = ['timers/', 'stream/', 'fs/', 'path/', 'node:']
                
                missing_modules = []
                for module in imports:
                    if module.startswith('.') or module.startswith('/'):
                        continue
                    
                    is_builtin = False
                    if module in core_modules:
                        is_builtin = True
                    
                    for pattern in builtin_patterns:
                        if module.startswith(pattern):
                            is_builtin = True
                            break
                    
                    if is_builtin:
                        continue
                    
                    module_path = os.path.join(node_modules_path, module)
                    if not os.path.exists(module_path):
                        missing_modules.append(module)
                
                if missing_modules:
                    logger.info(f"📦 Detected missing node modules: {missing_modules}")
                    
                    for module in missing_modules[:3]:
                        try:
                            status_msg = bot.send_message(script_owner_id, 
                                                        f"📦 Installing `{module}`...\nThis may take a moment...",
                                                        parse_mode='Markdown')
                            
                            install_result = subprocess.run(
                                ['npm', 'install', module, '--save', '--no-audit', '--no-fund'],
                                cwd=user_folder,
                                capture_output=True,
                                text=True,
                                env=current_env,
                                timeout=120
                            )
                            
                            if install_result.returncode == 0:
                                logger.info(f"✅ Installed {module}")
                                bot.edit_message_text(
                                    f"✅ Installed `{module}`",
                                    status_msg.chat.id,
                                    status_msg.message_id,
                                    parse_mode='Markdown'
                                )
                            else:
                                error_msg = install_result.stderr[:150] if install_result.stderr else "Unknown error"
                                logger.error(f"❌ Failed to install {module}: {error_msg}")
                                bot.edit_message_text(
                                    f"❌ Failed to install `{module}`\n```\n{error_msg}\n```",
                                    status_msg.chat.id,
                                    status_msg.message_id,
                                    parse_mode='Markdown'
                                )
                                
                        except subprocess.TimeoutExpired:
                            logger.error(f"❌ Timeout installing {module}")
                            bot.edit_message_text(
                                f"❌ Timeout installing `{module}`\nThis could be due to network issues or large package size.",
                                status_msg.chat.id,
                                status_msg.message_id,
                                parse_mode='Markdown'
                            )
                        except Exception as e:
                            logger.error(f"❌ Error installing {module}: {e}")
                            bot.edit_message_text(
                                f"❌ Error installing `{module}`: {str(e)[:100]}",
                                status_msg.chat.id,
                                status_msg.message_id,
                                parse_mode='Markdown'
                            )
                    
                    if missing_modules:
                        bot.send_message(script_owner_id, 
                                       f"🔄 Restarting `{file_name}` after module installation...",
                                       parse_mode='Markdown')
                        time.sleep(3)
                        threading.Thread(target=run_js_script, 
                                       args=(script_path, script_owner_id, user_folder, 
                                            file_name, message_obj_for_reply, attempt + 1)).start()
                        return
                        
            except Exception as e:
                logger.error(f"❌ Error analyzing file for imports: {e}")

        logger.info(f"🚀 Starting JS process for {script_key}")
        
        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = None
        
        try:
            log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"❌ Failed to open log file: {e}")
            try:
                bot.send_message(script_owner_id, f"❌ Log file error for `{file_name}`", parse_mode='Markdown')
            except:
                pass
            return

        try:
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            process = subprocess.Popen(
                ['node', script_path],
                cwd=user_folder,
                stdout=log_file,
                stderr=log_file,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo,
                encoding='utf-8',
                errors='ignore',
                bufsize=1,
                env=current_env
            )
            
            logger.info(f"✅ Started JS process {process.pid} for {script_key}")
            
            bot_scripts[script_key] = {
                'process': process,
                'log_file': log_file,
                'file_name': file_name,
                'chat_id': script_owner_id,
                'script_owner_id': script_owner_id,
                'start_time': datetime.now(),
                'user_folder': user_folder,
                'type': 'js',
                'script_key': script_key,
                'pid': process.pid
            }
            
            try:
                bot.send_message(
                    script_owner_id,
                    f"✅ `{file_name}` is Running!\n"
                    f"📊 PID: {process.pid}\n"
                    f"📁 Check logs for output",
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"❌ Failed to send success message: {e}")
            
            try:
                bot.delete_message(message_obj_for_reply.chat.id, message_obj_for_reply.message_id)
            except:
                pass

        except Exception as e:
            if log_file and not log_file.closed:
                log_file.close()
            error_msg = f"❌ Error starting `{file_name}`: {str(e)[:100]}"
            logger.error(error_msg, exc_info=True)
            try:
                bot.send_message(script_owner_id, error_msg, parse_mode='Markdown')
            except:
                pass
            if script_key in bot_scripts:
                del bot_scripts[script_key]

    except Exception as e:
        error_msg = f"❌ Critical Error with `{file_name}`: {str(e)[:100]}"
        logger.error(error_msg, exc_info=True)
        try:
            bot.send_message(script_owner_id, error_msg, parse_mode='Markdown')
        except:
            pass

# --- Docker Support ---
def run_docker_container(image, command, user_folder, env_vars=None):
    """Run Docker container"""
    if not docker_client:
        return None, "Docker not available"
    
    try:
        container = docker_client.containers.run(
            image,
            command,
            working_dir='/app',
            volumes={user_folder: {'bind': '/app', 'mode': 'rw'}},
            environment=env_vars or {},
            detach=True,
            remove=True,
            mem_limit='512m',
            cpu_period=100000,
            cpu_quota=50000
        )
        return container, None
    except Exception as e:
        return None, str(e)

def build_docker_image(user_folder, dockerfile_content):
    """Build Docker image from Dockerfile"""
    if not docker_client:
        return None, "Docker not available"
    
    try:
        dockerfile_path = os.path.join(user_folder, 'Dockerfile')
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        image, logs = docker_client.images.build(
            path=user_folder,
            dockerfile='Dockerfile',
            tag=f"user_{int(time.time())}"
        )
        return image, None
    except Exception as e:
        return None, str(e)

# --- Backup Functions ---
def create_backup(user_id=None):
    """Create backup of user data or entire system"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if user_id:
        # Backup single user
        backup_file = os.path.join(BACKUP_DIR, f"user_{user_id}_{timestamp}.zip")
        user_folder = get_user_folder(user_id)
        
        with zipfile.ZipFile(backup_file, 'w') as zipf:
            for root, dirs, files in os.walk(user_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, user_folder)
                    zipf.write(file_path, arcname)
        
        # Save backup record
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO backups (user_id, file_name, backup_path, size)
                     VALUES (?, ?, ?, ?)''',
                  (user_id, f"user_{user_id}_{timestamp}.zip", backup_file, os.path.getsize(backup_file)))
        conn.commit()
        conn.close()
        
        return backup_file
    else:
        # Backup entire system
        backup_file = os.path.join(BACKUP_DIR, f"full_backup_{timestamp}.zip")
        
        with zipfile.ZipFile(backup_file, 'w') as zipf:
            # Backup database
            zipf.write(DATABASE_PATH, 'database/kelvin_host.db')
            
            # Backup uploads
            for root, dirs, files in os.walk(UPLOAD_BOTS_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, BASE_DIR)
                    zipf.write(file_path, arcname)
            
            # Backup configs
            config_files = ['.env', 'config.json', 'settings.json']
            for config_file in config_files:
                if os.path.exists(os.path.join(BASE_DIR, config_file)):
                    zipf.write(os.path.join(BASE_DIR, config_file), f'config/{config_file}')
        
        return backup_file

def restore_backup(backup_path, user_id=None):
    """Restore from backup"""
    if not os.path.exists(backup_path):
        return False, "Backup file not found"
    
    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            if user_id:
                # Restore single user
                user_folder = get_user_folder(user_id)
                for file in zipf.namelist():
                    if not file.startswith('database/'):
                        zipf.extract(file, user_folder)
            else:
                # Restore entire system
                extract_dir = os.path.join(TEMP_DIR, 'restore')
                zipf.extractall(extract_dir)
                
                # Restore database
                if os.path.exists(os.path.join(extract_dir, 'database/kelvin_host.db')):
                    shutil.copy2(os.path.join(extract_dir, 'database/kelvin_host.db'), DATABASE_PATH)
                
                # Restore uploads
                if os.path.exists(os.path.join(extract_dir, UPLOAD_BOTS_DIR)):
                    shutil.rmtree(UPLOAD_BOTS_DIR)
                    shutil.copytree(os.path.join(extract_dir, UPLOAD_BOTS_DIR), UPLOAD_BOTS_DIR)
                
                shutil.rmtree(extract_dir)
        
        return True, "Restore completed successfully"
    except Exception as e:
        return False, str(e)

def schedule_backup():
    """Schedule automatic backups"""
    while True:
        try:
            # Check if backup is enabled
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            c.execute('SELECT setting_value FROM bot_settings WHERE setting_key = "backup_enabled"')
            result = c.fetchone()
            backup_enabled = result and result[0] == '1'
            
            if backup_enabled:
                c.execute('SELECT setting_value FROM bot_settings WHERE setting_key = "backup_interval"')
                result = c.fetchone()
                backup_interval = int(result[0]) if result else 24
                
                create_backup()
                logger.info(f"✅ Automatic backup completed")
            
            conn.close()
            time.sleep(3600 * backup_interval)  # Sleep for backup_interval hours
        except Exception as e:
            logger.error(f"❌ Error in scheduled backup: {e}")
            time.sleep(3600)

# --- Monitoring Functions ---
def monitor_system():
    """Monitor system resources"""
    while True:
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            if cpu_percent > 90:
                logger.warning(f"⚠️ High CPU usage: {cpu_percent}%")
                # Notify owner
                try:
                    bot.send_message(OWNER_ID, f"⚠️ High CPU usage: {cpu_percent}%")
                except:
                    pass
            
            if memory.percent > 90:
                logger.warning(f"⚠️ High memory usage: {memory.percent}%")
                try:
                    bot.send_message(OWNER_ID, f"⚠️ High memory usage: {memory.percent}%")
                except:
                    pass
            
            if disk.percent > 90:
                logger.warning(f"⚠️ High disk usage: {disk.percent}%")
                try:
                    bot.send_message(OWNER_ID, f"⚠️ High disk usage: {disk.percent}%")
                except:
                    pass
            
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"❌ Error in system monitoring: {e}")
            time.sleep(60)

# --- Webhook Functions ---
def create_webhook(user_id, url, events, secret=None):
    """Create webhook for user"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO webhooks (user_id, url, events, secret, is_active)
                     VALUES (?, ?, ?, ?, 1)''',
                  (user_id, url, json.dumps(events), secret))
        conn.commit()
        webhook_id = c.lastrowid
        return True, webhook_id
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def trigger_webhook(webhook_id, event_type, data):
    """Trigger webhook"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT url, events, secret FROM webhooks WHERE webhook_id = ? AND is_active = 1',
                  (webhook_id,))
        result = c.fetchone()
        if not result:
            return
        
        url, events, secret = result
        events = json.loads(events)
        
        if event_type not in events:
            return
        
        # Prepare payload
        payload = {
            'event': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add signature if secret provided
        headers = {'Content-Type': 'application/json'}
        if secret:
            signature = hmac.new(secret.encode(), json.dumps(payload).encode(), hashlib.sha256).hexdigest()
            headers['X-Webhook-Signature'] = signature
        
        # Send webhook asynchronously
        threading.Thread(target=send_webhook, args=(url, payload, headers)).start()
        
    except Exception as e:
        logger.error(f"❌ Error triggering webhook: {e}")
    finally:
        conn.close()

def send_webhook(url, payload, headers):
    """Send webhook request"""
    try:
        requests.post(url, json=payload, headers=headers, timeout=5)
    except Exception as e:
        logger.error(f"❌ Error sending webhook: {e}")

# --- Email Functions ---
def send_email(to_email, subject, body):
    """Send email notification"""
    try:
        # This is a placeholder - configure with your email settings
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        from_email = os.environ.get('FROM_EMAIL', 'noreply@kelvin.cloud')
        
        if not all([smtp_username, smtp_password]):
            logger.warning("⚠️ Email not configured")
            return
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            
        logger.info(f"✅ Email sent to {to_email}")
    except Exception as e:
        logger.error(f"❌ Error sending email: {e}")

# --- Menu Functions ---
def create_main_menu_keyboard(user_id):
    """Create main menu keyboard"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    buttons = [
        '📤 Upload File',
        '📂 My Files',
        '🔑 Redeem Key',
        '💎 Upgrade',
        '👤 Profile',
        '📊 Statistics',
        '🔧 Tools',
        '🌐 Webhooks',
        '💾 Backup',
        '📡 Monitor'
    ]
    
    if user_id in admin_ids:
        buttons.append('⚙️ Admin Dashboard')
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i+1])
        else:
            markup.row(buttons[i])
    
    return markup

def create_force_join_message():
    """Create force join message"""
    return f"""
🔒 *ACCESS RESTRICTED* 🔒

👋 **Welcome to KELVIN Cloud Hosting!**

To access our premium cloud services, please join our community:

🌐 **Official Channel:** [Join Channel]({FORCE_CHANNEL_LINK})
👥 **Community Group:** [Join Group]({FORCE_GROUP_LINK})

---
📋 **Instructions:**
1. Tap the buttons below to join
2. Wait a few seconds for Telegram to update
3. Tap "✅ Verify Access"
4. Enjoy unlimited cloud hosting!
    """

def create_force_join_keyboard():
    """Create force join keyboard"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🌐 Join Channel", url=FORCE_CHANNEL_LINK))
    markup.add(types.InlineKeyboardButton("👥 Join Group", url=FORCE_GROUP_LINK))
    markup.add(types.InlineKeyboardButton("✅ Verify Access", callback_data='check_membership'))
    return markup

def create_manage_files_keyboard(user_id):
    """Create manage files keyboard"""
    user_files_list = user_files.get(user_id, [])
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if not user_files_list:
        markup.add(types.InlineKeyboardButton("📭 No Files", callback_data='no_files'))
    else:
        for file_name, file_type, file_path in user_files_list:
            is_running = is_bot_running(user_id, file_name)
            status_emoji = "🟢" if is_running else "🔴"
            button_text = f"{status_emoji} {file_name}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=f'file_{user_id}_{file_name}'))
    
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data='back_to_main'))
    return markup

def create_file_management_buttons(user_id, file_name, is_running=True):
    """Create file management buttons"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    if is_running:
        markup.row(
            types.InlineKeyboardButton("⏸️ Stop", callback_data=f'stop_{user_id}_{file_name}'),
            types.InlineKeyboardButton("🔄 Restart", callback_data=f'restart_{user_id}_{file_name}')
        )
    else:
        markup.row(
            types.InlineKeyboardButton("▶️ Start", callback_data=f'start_{user_id}_{file_name}'),
        )
    markup.row(
        types.InlineKeyboardButton("🗑️ Delete", callback_data=f'delete_{user_id}_{file_name}'),
        types.InlineKeyboardButton("📋 Logs", callback_data=f'logs_{user_id}_{file_name}')
    )
    markup.row(
        types.InlineKeyboardButton("📦 Backup", callback_data=f'backup_{user_id}_{file_name}'),
        types.InlineKeyboardButton("🔗 Share", callback_data=f'share_{user_id}_{file_name}')
    )
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data='manage_files'))
    return markup

def create_admin_panel_keyboard(user_id=None):
    """Create admin panel keyboard"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    buttons = [
        '📊 Users Stats',
        '👥 Users',
        '💎 Premium Users',
        '🔑 Generate',
        '🔍 Key-User',
        '🗑️ Revoke',
        '🔢 Keys',
        '📊 Analytics',
        '⚙️ Settings',
        '📡 Monitor',
        '💾 Backup',
        '⬅️ Back'
    ]
    
    if user_id == OWNER_ID:
        owner_buttons = [
            '➕ Add Admin',
            '➖ Remove Admin',
            '🚫 Ban User',
            '✅ Unban User',
            '📋 Banned',
            '📢 Broadcast',
            '📈 Limits',
            '📁 All Files',
            '🛡️ Security Logs',
            '🛑 Force Stop',
            '🔧 System',
            '🌐 Webhooks',
            '📧 Email',
            '📊 Reports',
            '🔐 API Keys',
            '📦 Docker'
        ]
        buttons = owner_buttons + buttons
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i+1])
        else:
            markup.row(buttons[i])
    
    return markup

# --- Message Handlers ---
@bot.message_handler(commands=['start', 'help'])
def command_send_welcome(message):
    """Handle /start and /help commands"""
    user_id = message.from_user.id
    
    if message.chat.type in ['group', 'supergroup']:
        return

    # Rate limit check
    if not rate_limit_check(user_id):
        bot.send_message(message.chat.id, "⚠️ Rate limit exceeded. Please slow down.")
        return

    # Ban check
    if is_user_banned(user_id):
        bot.send_message(message.chat.id,
                        f"""
🚫 *YOU ARE BANNED*
⚠️ Your access has been revoked.

👑 **Contact Support:** {YOUR_USERNAME}
                        """,
                        parse_mode='Markdown')
        return

    # Bot lock check
    if bot_locked and user_id not in admin_ids:
        bot.send_message(message.chat.id,
                        f"""
🔒 *MAINTENANCE MODE*
⚠️ Temporarily unavailable.
Please try again later.

👑 **Contact Support:** {YOUR_USERNAME}
                        """,
                        parse_mode='Markdown')
        return

    # Force join check
    if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
        force_message = create_force_join_message()
        force_markup = create_force_join_keyboard()
        bot.send_message(message.chat.id, force_message, reply_markup=force_markup, parse_mode='Markdown')
        return
    
    # Add user
    add_active_user(user_id)
    save_user(user_id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    
    # Get user stats
    user_file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)
    user_stats = get_user_statistics(user_id)
    
    if user_file_limit == float('inf'):
        limit_display = '∞ Unlimited'
    else:
        limit_display = user_file_limit
    
    # Create welcome message
    welcome_text = f"""
☁️ **KELVIN CLOUD HOSTING** ☁️
*Version 3.0 - Enterprise Edition*

✨ *Welcome back, {message.from_user.first_name}!*

━━━━━━━━━━━━━━━━━━━━━
🚀 **PLATFORM FEATURES**
━━━━━━━━━━━━━━━━━━━━━
├─📦 30+ Languages Supported
├─⚡ Auto Dependency Install
├─🔧 Real-Time Monitoring
├─🛡️ Advanced Security Scanner
├─🌐 Webhook Integration
├─💾 Automated Backups
└─📊 Analytics Dashboard

━━━━━━━━━━━━━━━━━━━━━
👤 **ACCOUNT STATUS**
━━━━━━━━━━━━━━━━━━━━━
├─ Plan: {get_user_status(user_id)}
├─ Storage: {current_files}/{limit_display}
├─ Uploads: {user_stats['total_uploads'] if user_stats else 0}
└─ Downloads: {user_stats['total_downloads'] if user_stats else 0}

━━━━━━━━━━━━━━━━━━━━━
💎 **PREMIUM PLANS**
━━━━━━━━━━━━━━━━━━━━━
├─ 7 Days: 2000Ks / $0.50 (5 Files)
├─ 30 Days: 8000Ks / $2.00 (15 Files)
├─ 90 Days: 23000Ks / $5.50 (Unlimited)
├─ 1 Year: 80000Ks / $20.00 (Unlimited)
└─ Lifetime: 200000Ks / $50.00 (Unlimited)

Select an option below to begin.
    """
    
    markup = create_main_menu_keyboard(user_id)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_document_secure(message):
    """Handle file uploads with security scanning"""
    user_id = message.from_user.id

    if message.chat.type in ['group', 'supergroup']:
        return

    # Rate limit check
    if not rate_limit_check(user_id):
        bot.reply_to(message, "⚠️ Rate limit exceeded. Please slow down.")
        return

    # Ban check
    if is_user_banned(user_id):
        bot.reply_to(message,
                    f"""
🚫 *YOU ARE BANNED*
⚠️ Your access has been revoked.

👑 **Contact Support:** {YOUR_USERNAME}
                    """,
                    parse_mode='Markdown')
        return

    # Bot lock check
    if bot_locked and user_id not in admin_ids:
        bot.reply_to(message,
                    f"""
🔒 *MAINTENANCE MODE*
⚠️ Temporarily unavailable.
Please try again later.

👑 **Contact Support:** {YOUR_USERNAME}
                    """,
                    parse_mode='Markdown')
        return
    
    # Force join check
    if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
        force_message = create_force_join_message()
        force_markup = create_force_join_keyboard()
        bot.send_message(message.chat.id, force_message, reply_markup=force_markup, parse_mode='Markdown')
        return
    
    # File limit check
    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)
    
    if current_files >= file_limit:
        if is_premium_user(user_id):
            bot.reply_to(message, f"❌ Storage limit reached ({file_limit} files).\n💎 Contact admin to increase limit.")
        else:
            bot.reply_to(message, f"❌ Storage limit reached ({FREE_USER_LIMIT} files).\n💎 Upgrade to Premium for more space.")
        return
    
    # Process file
    doc = message.document
    file_name = doc.file_name
    file_ext = os.path.splitext(file_name)[1].lower()
    
    # Check file extension
    if file_ext not in SUPPORTED_EXTENSIONS:
        supported_list = ", ".join([f"`{ext}`" for ext in sorted(SUPPORTED_EXTENSIONS.keys())])
        bot.reply_to(message, f"❌ Unsupported File Type\n\nSupported: {supported_list}", parse_mode='Markdown')
        return
    
    try:
        # Download file
        file_info = bot.get_file(doc.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, file_name)
        
        temp_path = file_path + '.scan'
        with open(temp_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Scan file for threats
        threats = scan_file_for_threats(temp_path, user_id, message.from_user.username, file_name)
        
        if threats:
            report = generate_threat_report(threats, user_id, message.from_user.username, file_name, temp_path)
            
            if report and report['critical_risk']:
                os.remove(temp_path)
                security_scans['blocked_files'] += 1
                security_scans['high_risk_files'] += 1
                
                bot.reply_to(message,
                    f"""🚨 **SECURITY ALERT** 🚨

❌ File `{file_name}` BLOCKED
⛔ Critical threat detected (Score: {report['risk_score']})
🔒 File deleted for security.

📞 Contact admin immediately.
                    """,
                    parse_mode='Markdown'
                )
                
                send_threat_alert_to_owner(report)
                return
            
            elif report and report['high_risk']:
                os.remove(temp_path)
                security_scans['blocked_files'] += 1
                security_scans['high_risk_files'] += 1
                
                bot.reply_to(message,
                    f"""🚨 **SECURITY ALERT** 🚨

❌ File `{file_name}` BLOCKED
⚠️ High risk threat detected (Score: {report['risk_score']})
🔒 File deleted for security.

📞 Contact admin if this is a mistake.
                    """,
                    parse_mode='Markdown'
                )
                
                send_threat_alert_to_owner(report)
                return
            
            elif report:
                os.rename(temp_path, file_path)
                
                file_type = SUPPORTED_EXTENSIONS.get(file_ext, 'Unknown')
                save_user_file(user_id, file_name, file_type, file_path, pending=True)
                
                # Notify owner
                try:
                    bot.forward_message(OWNER_ID, message.chat.id, message.message_id)
                    user_mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
                    bot.send_message(OWNER_ID,
                                   f"""
📤 **FILE UPLOADED - PENDING REVIEW**

👤 User: {user_mention}
🆔 ID: `{user_id}`
📄 File: `{file_name}`
📦 Type: {file_type}
⚠️ Risk Score: {report['risk_score']}
🔍 Threats: {len(threats)}

🔒 Status: **PENDING OWNER REVIEW**
                                   """,
                                   parse_mode='Markdown')
                except Exception as e:
                    logger.error(f"❌ Failed to notify owner: {e}")

                bot.reply_to(message,
                    f"""⚠️ **UPLOAD PENDING REVIEW** ⚡

`{file_name}` uploaded successfully.
⚠️ Suspicious patterns detected (Score: {report['risk_score']})
👑 Admin has been notified.
🛡️ File will be reviewed shortly.
                    """,
                    parse_mode='Markdown'
                )

                send_threat_alert_to_owner(report)
                
        else:
            os.rename(temp_path, file_path)
            
            file_type = SUPPORTED_EXTENSIONS.get(file_ext, 'Unknown')
            save_user_file(user_id, file_name, file_type, file_path, pending=False)
            
            # Notify owner
            try:
                bot.forward_message(OWNER_ID, message.chat.id, message.message_id)
                user_mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
                bot.send_message(OWNER_ID,
                               f"""
📤 **NEW FILE UPLOADED**

👤 User: {user_mention}
🆔 ID: `{user_id}`
📄 File: `{file_name}`
📦 Type: {file_type}
✅ Status: **CLEAN - AUTO APPROVED**
                               """,
                               parse_mode='Markdown')
            except Exception as e:
                logger.error(f"❌ Failed to notify owner: {e}")
            
            limit_display = str(file_limit) if file_limit != float('inf') else "Unlimited"
            
            success_text = f"""
✅ **UPLOAD SUCCESSFUL**

📄 File: `{file_name}`
📦 Type: {file_type}
🛡️ Security: ✅ Clean

━━━━━━━━━━━━━━━━━━━━━
📊 **STORAGE USAGE**
━━━━━━━━━━━━━━━━━━━━━
├─ Used: {current_files + 1}/{limit_display}
└─ Free: {file_limit - (current_files + 1) if file_limit != float('inf') else '∞'}

Tap Deploy to start your application.
            """
            
            markup = create_start_hosting_keyboard()
            bot.reply_to(message, success_text, reply_markup=markup, parse_mode='Markdown')
            
            # Trigger webhook
            trigger_webhook(user_id, 'file_uploaded', {
                'file_name': file_name,
                'file_type': file_type,
                'file_size': os.path.getsize(file_path)
            })
        
    except Exception as e:
        logger.error(f"❌ Error uploading file: {e}")
        bot.reply_to(message, f"❌ Error: {str(e)}")

# --- Callback Handlers ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    """Handle all callback queries"""
    user_id = call.from_user.id

    if call.message.chat.type in ['group', 'supergroup']:
        bot.answer_callback_query(call.id, "❌ This bot only works in private chats", show_alert=True)
        return

    # Rate limit check
    if not rate_limit_check(user_id):
        bot.answer_callback_query(call.id, "⚠️ Rate limit exceeded", show_alert=True)
        return

    # Ban check
    if not (user_id in admin_ids or user_id == OWNER_ID) and is_user_banned(user_id):
        bot.answer_callback_query(call.id,
                                 f"""
🚫 YOU ARE BANNED
⚠️ YOUR ACCESS HAS BEEN REVOKED
                                 """,
                                 show_alert=True)
        return

    # Bot lock check
    if bot_locked and user_id not in admin_ids:
        bot.answer_callback_query(call.id,
                                 f"🔒 MAINTENANCE MODE",
                                 show_alert=True)
        return
    
    data = call.data
    
    try:
        # Membership verification
        if data == 'check_membership':
            handle_check_membership(call)
        
        # Main menu actions
        elif data == 'start_hosting':
            handle_start_hosting_callback(call)
        elif data == 'manage_files':
            handle_manage_files_callback(call)
        elif data.startswith('file_'):
            handle_file_click(call)
        elif data == 'redeem_key':
            msg = bot.send_message(call.message.chat.id, "🔑 Enter Key (KELVIN-XXXX-XXXX-XXXX):")
            bot.register_next_step_handler(msg, process_redeem_key)
        elif data == 'buy_subscription':
            handle_buy_subscription_text(call.message)
        elif data == 'back_to_main':
            handle_back_to_main_callback(call)
        
        # File management actions
        elif data.startswith('start_'):
            handle_start_file(call)
        elif data.startswith('stop_'):
            handle_stop_file(call)
        elif data.startswith('restart_'):
            handle_restart_file(call)
        elif data.startswith('delete_'):
            handle_delete_file(call)
        elif data.startswith('logs_'):
            handle_logs_file(call)
        elif data.startswith('backup_'):
            handle_backup_file(call)
        elif data.startswith('share_'):
            handle_share_file(call)
        
        # Admin actions
        elif data.startswith('security_'):
            handle_security_actions(call)
        elif data.startswith('confirm_broadcast_'):
            handle_confirm_broadcast(call)
        elif data == 'cancel_broadcast':
            handle_cancel_broadcast(call)
        elif data == 'no_files':
            bot.answer_callback_query(call.id, "📭 No Files", show_alert=True)
        
        # Settings actions
        elif data == 'toggle_force_join':
            handle_toggle_force_join(call)
        elif data == 'toggle_bot_lock':
            handle_toggle_bot_lock(call)
        elif data == 'change_file_limit':
            handle_change_file_limit(call)
        elif data == 'security_stats':
            handle_security_stats(call)
        elif data == 'broadcast_settings':
            handle_broadcast_settings(call)
        elif data == 'system_info':
            handle_system_info(call)
        elif data == 'view_security_logs':
            handle_view_security_logs(call)
        elif data == 'back_to_admin_settings':
            handle_back_to_admin_settings(call)
        elif data == 'back_to_admin':
            handle_back_to_admin(call)
            
    except Exception as e:
        logger.error(f"❌ Error in callback handler: {e}")
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)

def handle_check_membership(call):
    """Handle membership verification"""
    user_id = call.from_user.id
    
    if user_id in admin_ids:
        bot.answer_callback_query(call.id, "✅ Admin Access", show_alert=True)
        return
    
    if check_force_join(user_id):
        bot.answer_callback_query(call.id, "✅ Verified", show_alert=True)
        
        add_active_user(user_id)
        save_user(user_id, call.from_user.username, call.from_user.first_name, call.from_user.last_name)
        
        welcome_text = f"""
☁️ **KELVIN CLOUD HOSTING** ☁️

✨ *Welcome, {call.from_user.first_name}!*

✅ **MEMBERSHIP VERIFIED**

📊 **Status:** {get_user_status(user_id)}
📁 **Files:** {get_user_file_count(user_id)}/{get_user_file_limit(user_id) if get_user_file_limit(user_id) != float('inf') else '∞'}

Tap buttons to start hosting.
        """
        
        markup = create_main_menu_keyboard(user_id)

        try:
            bot.send_message(call.message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            logger.error(f"❌ Error sending welcome message: {e}")
            try:
                bot.edit_message_text(welcome_text, call.message.chat.id, call.message.message_id,
                                     reply_markup=markup, parse_mode='Markdown')
            except Exception as e2:
                logger.error(f"❌ Error editing message: {e2}")
                bot.send_message(call.message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')
    else:
        bot.answer_callback_query(call.id, "❌ Please join the group and channel first", show_alert=True)

def handle_manage_files_callback(call):
    """Handle manage files callback"""
    user_id = call.from_user.id
    
    if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
        force_message = create_force_join_message()
        force_markup = create_force_join_keyboard()
        bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                             reply_markup=force_markup, parse_mode='Markdown')
        return
    
    user_files_list = user_files.get(user_id, [])
    
    if not user_files_list:
        bot.answer_callback_query(call.id, "📭 No Files", show_alert=True)
        return
    
    files_text = f"📂 **MY FILES:**\n\n"
    
    for file_name, file_type, file_path in user_files_list:
        is_running = is_bot_running(user_id, file_name)
        status = "🟢 Running" if is_running else "🔴 Stopped"
        file_size = format_file_size(os.path.getsize(file_path)) if os.path.exists(file_path) else "Unknown"
        files_text += f"• `{file_name}`\n  ├─ {status}\n  └─ Size: {file_size}\n\n"
    
    files_text += "\nTap a file to manage it."
    
    markup = create_manage_files_keyboard(user_id)
    bot.edit_message_text(files_text, call.message.chat.id, call.message.message_id,
                         reply_markup=markup, parse_mode='Markdown')

def handle_file_click(call):
    """Handle file click"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        
        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, "❌ Access Denied", show_alert=True)
            return
        
        if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
            force_message = create_force_join_message()
            force_markup = create_force_join_keyboard()
            bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                                 reply_markup=force_markup, parse_mode='Markdown')
            return
        
        file_details = None
        for fn, ft, fp in user_files.get(user_id, []):
            if fn == file_name:
                file_details = (fn, ft, fp)
                break
        
        if not file_details:
            bot.answer_callback_query(call.id, "❌ File Not Found", show_alert=True)
            return
        
        file_name, file_type, file_path = file_details
        is_running = is_bot_running(user_id, file_name)
        file_size = format_file_size(os.path.getsize(file_path)) if os.path.exists(file_path) else "Unknown"
        
        file_text = f"""
📄 **FILE DETAILS**

━━━━━━━━━━━━━━━━━━━━━
📌 **Name:** `{file_name}`
📦 **Type:** {file_type}
📊 **Size:** {file_size}
🔧 **Status:** {'🟢 Running' if is_running else '🔴 Stopped'}
━━━━━━━━━━━━━━━━━━━━━

Select an action below:
        """
        
        markup = create_file_management_buttons(user_id, file_name, is_running)
        bot.edit_message_text(file_text, call.message.chat.id, call.message.message_id,
                             reply_markup=markup, parse_mode='Markdown')
        
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_start_hosting_callback(call):
    """Handle start hosting callback"""
    user_id = call.from_user.id
    
    if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
        force_message = create_force_join_message()
        force_markup = create_force_join_keyboard()
        bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                             reply_markup=force_markup, parse_mode='Markdown')
        return
    
    user_files_list = user_files.get(user_id, [])
    
    if not user_files_list:
        bot.answer_callback_query(call.id, "❌ No Files to Deploy", show_alert=True)
        return
    
    bot.answer_callback_query(call.id, "🚀 Starting deployment...")
    
    started_count = 0
    for file_name, file_type, file_path in user_files_list:
        if not is_bot_running(user_id, file_name):
            user_folder = get_user_folder(user_id)
            
            if os.path.exists(file_path):
                file_ext = os.path.splitext(file_name)[1].lower()
                if file_ext == '.py':
                    threading.Thread(target=run_script, 
                                   args=(file_path, user_id, user_folder, file_name, call.message)).start()
                    started_count += 1
                elif file_ext == '.js':
                    threading.Thread(target=run_js_script,
                                   args=(file_path, user_id, user_folder, file_name, call.message)).start()
                    started_count += 1
                time.sleep(1)
    
    if started_count > 0:
        bot.send_message(call.message.chat.id, f"✅ Deployed {started_count} files")
    else:
        bot.send_message(call.message.chat.id, "ℹ️ All files are already running")

def handle_back_to_main_callback(call):
    """Handle back to main callback"""
    user_id = call.from_user.id
    
    if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
        force_message = create_force_join_message()
        force_markup = create_force_join_keyboard()
        bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                             reply_markup=force_markup, parse_mode='Markdown')
        return
    
    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)
    limit_str = str(file_limit) if file_limit != float('inf') else "∞"
    user_stats = get_user_statistics(user_id)
    
    main_menu_text = f"""
☁️ **KELVIN CLOUD HOSTING**

👋 *{call.from_user.first_name}*

━━━━━━━━━━━━━━━━━━━━━
📊 **ACCOUNT INFO**
━━━━━━━━━━━━━━━━━━━━━
├─ ID: `{user_id}`
├─ Status: {get_user_status(user_id)}
├─ Files: {current_files} / {limit_str}
├─ Uploads: {user_stats['total_uploads'] if user_stats else 0}
└─ Downloads: {user_stats['total_downloads'] if user_stats else 0}

Select an option below.
    """
    
    markup = create_main_menu_keyboard(user_id)
    bot.edit_message_text(main_menu_text, call.message.chat.id, call.message.message_id,
                         reply_markup=markup, parse_mode='Markdown')

def handle_start_file(call):
    """Handle start file"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        
        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, "❌ Access Denied", show_alert=True)
            return
        
        if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
            force_message = create_force_join_message()
            force_markup = create_force_join_keyboard()
            bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                                 reply_markup=force_markup, parse_mode='Markdown')
            return
        
        file_path = None
        for fn, ft, fp in user_files.get(user_id, []):
            if fn == file_name:
                file_path = fp
                break
        
        if not file_path or not os.path.exists(file_path):
            bot.answer_callback_query(call.id, "❌ File Not Found", show_alert=True)
            return
        
        user_folder = get_user_folder(user_id)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        if file_ext == '.py':
            threading.Thread(target=run_script, 
                           args=(file_path, user_id, user_folder, file_name, call.message)).start()
            bot.answer_callback_query(call.id, f"🚀 Starting Python script...")
        elif file_ext == '.js':
            threading.Thread(target=run_js_script,
                           args=(file_path, user_id, user_folder, file_name, call.message)).start()
            bot.answer_callback_query(call.id, f"🚀 Starting JavaScript...")
        else:
            bot.answer_callback_query(call.id, f"✅ File ready")
        
        time.sleep(1)
        handle_file_click(call)
        
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_stop_file(call):
    """Handle stop file"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        script_key = f"{user_id}_{file_name}"
        
        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, "❌ Access Denied", show_alert=True)
            return
        
        if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
            force_message = create_force_join_message()
            force_markup = create_force_join_keyboard()
            bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                                 reply_markup=force_markup, parse_mode='Markdown')
            return
        
        process_info = bot_scripts.get(script_key)
        if process_info:
            success = force_cleanup_process(process_info)
            
            if script_key in bot_scripts:
                del bot_scripts[script_key]
            
            if success:
                bot.answer_callback_query(call.id, f"⏸️ Stopped successfully")
            else:
                bot.answer_callback_query(call.id, f"⚠️ Partially stopped")
        else:
            bot.answer_callback_query(call.id, f"ℹ️ Not running")
        
        time.sleep(1)
        handle_file_click(call)
            
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_restart_file(call):
    """Handle restart file"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        
        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, "❌ Access Denied", show_alert=True)
            return
        
        if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
            force_message = create_force_join_message()
            force_markup = create_force_join_keyboard()
            bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                                 reply_markup=force_markup, parse_mode='Markdown')
            return
        
        script_key = f"{user_id}_{file_name}"
        process_info = bot_scripts.get(script_key)
        if process_info:
            force_cleanup_process(process_info)
            if script_key in bot_scripts:
                del bot_scripts[script_key]
            time.sleep(1)
        
        file_path = None
        for fn, ft, fp in user_files.get(user_id, []):
            if fn == file_name:
                file_path = fp
                break
        
        if file_path and os.path.exists(file_path):
            user_folder = get_user_folder(user_id)
            file_ext = os.path.splitext(file_name)[1].lower()
            if file_ext == '.py':
                threading.Thread(target=run_script, 
                               args=(file_path, user_id, user_folder, file_name, call.message)).start()
            elif file_ext == '.js':
                threading.Thread(target=run_js_script,
                               args=(file_path, user_id, user_folder, file_name, call.message)).start()
            bot.answer_callback_query(call.id, f"🔄 Restarting...")
        else:
            bot.answer_callback_query(call.id, "❌ File Not Found", show_alert=True)
        
        time.sleep(1)
        handle_file_click(call)
            
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_delete_file(call):
    """Handle delete file"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        
        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, "❌ Access Denied", show_alert=True)
            return
        
        if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
            force_message = create_force_join_message()
            force_markup = create_force_join_keyboard()
            bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                                 reply_markup=force_markup, parse_mode='Markdown')
            return
        
        file_path = None
        for fn, ft, fp in user_files.get(user_id, []):
            if fn == file_name:
                file_path = fp
                break
        
        if not file_path:
            bot.answer_callback_query(call.id, "❌ File Not Found", show_alert=True)
            return
        
        script_key = f"{user_id}_{file_name}"
        process_info = bot_scripts.get(script_key)
        if process_info:
            force_cleanup_process(process_info)
            if script_key in bot_scripts:
                del bot_scripts[script_key]
        
        remove_user_file_db(user_id, file_name)
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error(f"❌ Error deleting file: {e}")
        
        user_folder = get_user_folder(user_id)
        log_file = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            except Exception as e:
                logger.error(f"❌ Error deleting log file: {e}")
        
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            logger.error(f"❌ Error deleting message: {e}")
            bot.edit_message_text(
                f"✅ **{file_name}** Deleted Successfully",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            return
        
        bot.send_message(
            call.message.chat.id,
            f"🗑️ **{file_name}** Deleted Successfully",
            parse_mode='Markdown'
        )
        
        handle_manage_files_callback(call)
        
    except Exception as e:
        logger.error(f"❌ Error in handle_delete_file: {e}")
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_logs_file(call):
    """Handle view logs"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        
        if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
            force_message = create_force_join_message()
            force_markup = create_force_join_keyboard()
            bot.edit_message_text(force_message, call.message.chat.id, call.message.message_id,
                                 reply_markup=force_markup, parse_mode='Markdown')
            return
        
        user_folder = get_user_folder(user_id)
        log_file = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                logs = f.read()
            
            if len(logs) > 4000:
                logs = logs[:4000] + "\n\n... (Truncated)"
            
            log_text = f"📋 **{file_name} Logs:**\n\n```\n{logs}\n```"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f'file_{user_id}_{file_name}'))
            
            bot.edit_message_text(log_text, call.message.chat.id, call.message.message_id,
                                 reply_markup=markup, parse_mode='Markdown')
        else:
            bot.answer_callback_query(call.id, "📭 No Logs Found", show_alert=True)
            
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_backup_file(call):
    """Handle backup file"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        
        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, "❌ Access Denied", show_alert=True)
            return
        
        backup_file = create_backup(user_id)
        
        if backup_file and os.path.exists(backup_file):
            with open(backup_file, 'rb') as f:
                bot.send_document(
                    call.message.chat.id,
                    f,
                    caption=f"📦 Backup of {file_name}\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
            bot.answer_callback_query(call.id, "✅ Backup created")
        else:
            bot.answer_callback_query(call.id, "❌ Backup failed", show_alert=True)
            
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_share_file(call):
    """Handle share file"""
    try:
        _, user_id_str, file_name = call.data.split('_', 2)
        user_id = int(user_id_str)
        
        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, "❌ Access Denied", show_alert=True)
            return
        
        file_path = None
        for fn, ft, fp in user_files.get(user_id, []):
            if fn == file_name:
                file_path = fp
                break
        
        if file_path and os.path.exists(file_path):
            # Make file public
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            c.execute('UPDATE user_files SET is_public = 1 WHERE user_id = ? AND file_name = ?',
                     (user_id, file_name))
            conn.commit()
            conn.close()
            
            # Generate share link
            share_link = f"https://t.me/{bot.get_me().username}?start=share_{user_id}_{file_name}"
            
            bot.send_message(
                call.message.chat.id,
                f"""
🔗 **Share Link Generated**

📄 File: `{file_name}`
🔗 Link: `{share_link}`

Anyone with this link can download the file.
Share at your own risk!
                """,
                parse_mode='Markdown'
            )
            
            bot.answer_callback_query(call.id, "✅ Share link created")
        else:
            bot.answer_callback_query(call.id, "❌ File not found", show_alert=True)
            
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

# --- Text Message Handlers ---
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    """Handle text messages"""
    user_id = message.from_user.id

    if message.chat.type in ['group', 'supergroup']:
        return

    # Rate limit check
    if not rate_limit_check(user_id):
        bot.send_message(message.chat.id, "⚠️ Rate limit exceeded. Please slow down.")
        return

    # Ban check
    if not (user_id in admin_ids or user_id == OWNER_ID) and is_user_banned(user_id):
        bot.send_message(message.chat.id,
                        f"""
🚫 *YOU ARE BANNED*
⚠️ Your access has been revoked.

👑 **Contact Support:** {YOUR_USERNAME}
                        """,
                        parse_mode='Markdown')
        return

    # Bot lock check
    if bot_locked and user_id not in admin_ids:
        bot.send_message(message.chat.id,
                        f"""
🔧 *MAINTENANCE MODE*
⚠️ Temporarily unavailable.
Please try again later.

👑 **Contact Support:** {YOUR_USERNAME}
                        """,
                        parse_mode='Markdown')
        return
        
    # Force join check
    if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
        force_message = create_force_join_message()
        force_markup = create_force_join_keyboard()
        bot.send_message(message.chat.id, force_message, reply_markup=force_markup, parse_mode='Markdown')
        return
    
    text = message.text

    # Admin commands
    if text == '📁 All Files' and user_id == OWNER_ID:
        handle_admin_files_text(message)
    elif text == '🛡️ Security Logs' and user_id == OWNER_ID:
        handle_security_logs_text(message)
    elif text == '🔍 Key-User' and user_id in admin_ids:
        handle_key_user_info_text(message)
    elif text == '📊 Users Stats' and user_id in admin_ids:
        handle_bot_statistics_text(message)
    elif text == '👥 Users' and user_id in admin_ids:
        handle_all_users_text(message)
    elif text == '💎 Premium Users' and user_id in admin_ids:
        handle_premium_users_text(message)
    elif text == '📢 Broadcast' and user_id in admin_ids:
        handle_broadcast_text(message)
    elif text == '🔑 Generate' and user_id in admin_ids:
        handle_generate_key_text(message)
    elif text == '🗑️ Revoke' and user_id in admin_ids:
        handle_delete_key_text(message)
    elif text == '🔢 Keys' and user_id in admin_ids:
        handle_total_keys_text(message)
    elif text == '📈 Limits' and user_id in admin_ids:
        handle_file_limit_text(message)
    elif text == '⚙️ Settings' and user_id in admin_ids:
        handle_bot_settings_text(message)
    elif text == '➕ Add Admin' and user_id == OWNER_ID:
        handle_add_admin_text(message)
    elif text == '➖ Remove Admin' and user_id == OWNER_ID:
        handle_remove_admin_text(message)
    elif text == '🚫 Ban User' and user_id == OWNER_ID:
        handle_ban_user_text(message)
    elif text == '✅ Unban User' and user_id == OWNER_ID:
        handle_unban_user_text(message)
    elif text == '📋 Banned' and user_id == OWNER_ID:
        handle_view_banned_users_text(message)
    elif text == '🛑 Force Stop' and user_id in admin_ids:
        handle_force_stop_user_text(message)
    elif text == '📊 Analytics' and user_id in admin_ids:
        handle_analytics_text(message)
    elif text == '🔐 API Keys' and user_id == OWNER_ID:
        handle_api_keys_text(message)
    elif text == '🌐 Webhooks' and user_id in admin_ids:
        handle_webhooks_text(message)
    elif text == '📦 Docker' and user_id == OWNER_ID:
        handle_docker_text(message)
    elif text == '📧 Email' and user_id == OWNER_ID:
        handle_email_text(message)
    elif text == '📊 Reports' and user_id == OWNER_ID:
        handle_reports_text(message)
    elif text == '🔧 System' and user_id == OWNER_ID:
        handle_system_text(message)
    elif text == '📡 Monitor' and user_id in admin_ids:
        handle_monitor_text(message)
    elif text == '💾 Backup' and user_id in admin_ids:
        handle_backup_text(message)
    
    # User commands
    elif text == '⬅️ Back':
        handle_back_to_main_text(message)
    elif text == '📤 Upload File':
        handle_upload_file_text(message)
    elif text == '📂 My Files':
        handle_manage_files_text(message)
    elif text == '🔑 Redeem Key':
        handle_redeem_key_text(message)
    elif text == '💎 Upgrade':
        handle_buy_subscription_text(message)
    elif text == '👤 Profile':
        handle_my_info_text(message)
    elif text == '📊 Statistics':
        handle_status_text(message)
    elif text == '🔧 Tools':
        handle_tools_text(message)
    elif text == '🌐 Webhooks':
        handle_user_webhooks_text(message)
    elif text == '💾 Backup':
        handle_user_backup_text(message)
    elif text == '📡 Monitor':
        handle_user_monitor_text(message)
    elif text == '⚙️ Admin Dashboard' and user_id in admin_ids:
        handle_admin_panel_text(message)
    else:
        bot.send_message(message.chat.id, "❌ Invalid Command. Please use the menu buttons.")

# --- Admin Text Handlers ---
def handle_admin_panel_text(message):
    """Handle admin panel"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    markup = create_admin_panel_keyboard(message.from_user.id)
    
    if message.from_user.id == OWNER_ID:
        role_text = "👑 Owner"
        features = "• Full system access\n• Security monitoring\n• User management\n• Key generation"
    else:
        role_text = "🛡️ Admin"
        features = "• User management\n• Key management\n• View statistics"
    
    stats = get_bot_statistics()
    
    admin_text = f"""
🛡️ **ADMIN DASHBOARD**

━━━━━━━━━━━━━━━━━━━━━
👤 **User:** {message.from_user.first_name}
🆔 **ID:** `{message.from_user.id}`
📋 **Role:** {role_text}

━━━━━━━━━━━━━━━━━━━━━
📊 **SYSTEM STATS**
━━━━━━━━━━━━━━━━━━━━━
├─ Users: {stats['total_users']}
├─ Premium: {stats['premium_users']}
├─ Files: {stats['total_files']}
├─ Active: {stats['active_files']}
├─ CPU: {stats['cpu_percent']}%
└─ Memory: {stats['memory_percent']}%

━━━━━━━━━━━━━━━━━━━━━
⚙️ **Your Features:**
{features}

Select an option below.
    """
    
    bot.send_message(message.chat.id, admin_text, reply_markup=markup, parse_mode='Markdown')

def handle_bot_statistics_text(message):
    """Handle bot statistics"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    stats = get_bot_statistics()
    key_stats = get_key_stats()
    
    html_text = f"""
<b>📊 SYSTEM STATISTICS</b>

━━━━━━━━━━━━━━━━━━━━━
<b>👥 USERS</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>Total Users:</b> <code>{stats['total_users']}</code>
├─ <b>Premium Users:</b> <code>{stats['premium_users']}</code>
└─ <b>Banned Users:</b> <code>{stats['banned_users']}</code>

━━━━━━━━━━━━━━━━━━━━━
<b>📁 FILES</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>Total Files:</b> <code>{stats['total_files']}</code>
├─ <b>Active Files:</b> <code>{stats['active_files']}</code>
├─ <b>Total Downloads:</b> <code>{stats['total_downloads']}</code>
└─ <b>Storage Used:</b> <code>{stats['total_storage']}</code>

━━━━━━━━━━━━━━━━━━━━━
<b>🔑 KEYS</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>Total Keys:</b> <code>{key_stats['total_keys']}</code>
├─ <b>Active Keys:</b> <code>{key_stats['active_keys']}</code>
├─ <b>Keys Used:</b> <code>{key_stats['total_used']}</code>
└─ <b>Unique Users:</b> <code>{key_stats['unique_users']}</code>

━━━━━━━━━━━━━━━━━━━━━
<b>⚙️ SYSTEM</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>CPU Usage:</b> <code>{stats['cpu_percent']}%</code>
├─ <b>Memory Usage:</b> <code>{stats['memory_percent']}% ({stats['memory_used']}/{stats['memory_total']})</code>
├─ <b>Disk Usage:</b> <code>{stats['disk_percent']}% ({stats['disk_used']}/{stats['disk_total']})</code>
└─ <b>Uptime:</b> <code>{stats['uptime']}</code>

━━━━━━━━━━━━━━━━━━━━━
<b>🛡️ SECURITY</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>Total Scans:</b> <code>{stats['security_scans']['total_scans']}</code>
├─ <b>Threats Found:</b> <code>{stats['security_scans']['threats_found']}</code>
├─ <b>High Risk:</b> <code>{stats['security_scans']['high_risk_files']}</code>
├─ <b>Blocked Files:</b> <code>{stats['security_scans']['blocked_files']}</code>
└─ <b>Security Alerts:</b> <code>{stats['security_alerts']}</code>

━━━━━━━━━━━━━━━━━━━━━
<b>🔌 INTEGRATIONS</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>API Keys:</b> <code>{stats['total_api_keys']}</code>
├─ <b>Webhooks:</b> <code>{stats['total_webhooks']}</code>
└─ <b>Notifications:</b> <code>{stats['unread_notifications']} unread</code>
    """
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_all_users_text(message):
    """Handle all users list"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    users = get_all_users_details()
    if not users:
        bot.send_message(message.chat.id, "📭 No Users Found")
        return
    
    html_text = "<b>👥 ALL USERS LIST</b>\n\n"
    
    for user in users[:50]:
        status = "💎" if user['is_premium'] else "👤"
        username = f"@{user['username']}" if user['username'] else "-"
        
        html_text += f"""
{status} <b>{user['first_name']}</b>
├─ <b>ID:</b> <code>{user['user_id']}</code>
└─ <b>Username:</b> {username}
"""
        html_text += "─" * 25 + "\n"
    
    if len(users) > 50:
        html_text += f"\n<b>📈 ... {len(users) - 50} more users</b>"
    
    html_text += f"\n<b>📊 TOTAL USERS:</b> {len(users)}"
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_premium_users_text(message):
    """Handle premium users list"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    premium_users = get_premium_users_details()
    if not premium_users:
        bot.send_message(message.chat.id, "📭 No Premium Users")
        return
    
    html_text = "<b>💎 PREMIUM USERS</b>\n\n"
    
    for user in premium_users:
        days_left = (user['expiry'] - datetime.now()).days
        
        html_text += f"""
<b>👤 {user['first_name']}</b> (@{user['username']})
├─ <b>ID:</b> <code>{user['user_id']}</code>
├─ <b>Files:</b> {user['file_count']}/{user['file_limit']}
├─ <b>Running:</b> 🟢 {user['running_files']}
└─ <b>Days Left:</b> {days_left}
"""
    
    html_text += f"\n<b>📊 TOTAL PREMIUM:</b> {len(premium_users)} users"
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_key_user_info_text(message):
    """Handle key-user info"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    msg = bot.send_message(message.chat.id, "<b>🔑 Enter key to check:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_key_user_info_html)

def process_key_user_info_html(message):
    """Process key-user info"""
    key_value = message.text.strip().upper()
    
    user_info = get_user_by_key(key_value)
    
    if not user_info:
        bot.reply_to(message, f"❌ No user found for key <code>{key_value}</code>", parse_mode='HTML')
        return
    
    html_text = f"""
<b>🔑 KEY-USER INFORMATION</b>

<b>Key:</b> <code>{key_value}</code>

━━━━━━━━━━━━━━━━━━━━━
<b>👤 USER DETAILS</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>ID:</b> <code>{user_info['user_id']}</code>
├─ <b>Name:</b> {user_info['first_name']}
├─ <b>Username:</b> @{user_info['username'] if user_info['username'] else 'N/A'}
├─ <b>Key Type:</b> {user_info['key_type']}
├─ <b>Duration:</b> {user_info['days_valid']} Days
├─ <b>File Limit:</b> {user_info['file_limit']}
├─ <b>Key Activated:</b> {user_info['key_activation_date']}
└─ <b>User Data Saved:</b> {user_info['key_used_date']}

<b>📝 Note:</b> 1 Key = 1 User (Strict Enforcement)
    """
    
    user_files_list = get_user_files_with_details(user_info['user_id'])
    
    if user_files_list:
        html_text += f"\n<b>📁 FILES ({len(user_files_list)}):</b>\n"
        for file in user_files_list[:10]:
            status = "🟢" if file['is_running'] else "🔴"
            html_text += f"├─ {status} <code>{file['file_name']}</code> ({file['file_size']})\n"
        
        if len(user_files_list) > 10:
            html_text += f"└─ <b>... {len(user_files_list) - 10} more files</b>\n"
    else:
        html_text += "\n<b>📭 NO FILES</b>"
    
    bot.reply_to(message, html_text, parse_mode='HTML')

def handle_broadcast_text(message):
    """Handle broadcast"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    msg = bot.send_message(message.chat.id, "📢 Enter message to broadcast:")
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    """Process broadcast message"""
    broadcast_messages[message.message_id] = message.text
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Send", callback_data=f'confirm_broadcast_{message.message_id}'),
        types.InlineKeyboardButton("❌ Cancel", callback_data='cancel_broadcast')
    )
    
    bot.send_message(message.chat.id,
                    f"📢 **PREVIEW:**\n\n{message.text}\n\nSend to all {len(active_users)} users?",
                    reply_markup=markup, parse_mode='Markdown')

def handle_generate_key_text(message):
    """Handle generate key"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("7 Days", callback_data='gen_key_7'),
        types.InlineKeyboardButton("30 Days", callback_data='gen_key_30'),
        types.InlineKeyboardButton("90 Days", callback_data='gen_key_90'),
        types.InlineKeyboardButton("365 Days", callback_data='gen_key_365'),
        types.InlineKeyboardButton("Lifetime", callback_data='gen_key_lifetime'),
        types.InlineKeyboardButton("Custom", callback_data='gen_key_custom')
    )
    
    bot.send_message(message.chat.id, "📅 Select key duration:", reply_markup=markup)

def handle_delete_key_text(message):
    """Handle delete key"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    keys = get_all_subscription_keys()
    if not keys:
        bot.send_message(message.chat.id, "📭 No Keys Found")
        return
    
    keys_text = f"🗑️ **ACTIVE KEYS:**\n\n"
    for key in keys:
        status = "✅ Active" if key[8] == 1 else "❌ Inactive"
        keys_text += f"• `{key[0]}`\n  ├─ {key[6]} - {key[1]}d\n  ├─ {key[3]}/{key[2]} uses\n  ├─ {key[4]} files\n  └─ Status: {status}\n\n"
    
    keys_text += "\nEnter the key to revoke:"
    bot.send_message(message.chat.id, keys_text, parse_mode='Markdown')
    
    msg = bot.send_message(message.chat.id, "🔑 Key:")
    bot.register_next_step_handler(msg, process_delete_key)

def process_delete_key(message):
    """Process delete key"""
    key_value = message.text.strip().upper()
    
    keys = get_all_subscription_keys()
    key_exists = any(key[0] == key_value for key in keys)
    
    if not key_exists:
        bot.send_message(message.chat.id, f"❌ Key `{key_value}` not found", parse_mode='Markdown')
        return
    
    delete_subscription_key(key_value)
    bot.send_message(message.chat.id, f"✅ Key `{key_value}` revoked successfully", parse_mode='Markdown')

def handle_total_keys_text(message):
    """Handle total keys"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    keys = get_all_subscription_keys()
    key_stats = get_key_stats()
    
    if not keys:
        bot.send_message(message.chat.id, "📭 No Keys Found")
        return
    
    html_text = f"""
<b>🔢 ALL KEYS</b>

<b>📊 SUMMARY:</b>
├─ Total Keys: {key_stats['total_keys']}
├─ Active Keys: {key_stats['active_keys']}
├─ Used Keys: {key_stats['total_used']}
└─ Unique Users: {key_stats['unique_users']}

━━━━━━━━━━━━━━━━━━━━━
<b>🔑 KEY LIST:</b>
━━━━━━━━━━━━━━━━━━━━━
"""
    
    for key in keys[:20]:
        key_value, days, max_uses, used, files, created, key_type, price, is_active = key
        status = "✅" if is_active else "❌"
        html_text += f"""
{status} <code>{key_value}</code>
├─ Type: {key_type}
├─ Duration: {days} days
├─ Files: {files}
├─ Usage: {used}/{max_uses}
└─ Created: {created[:10]}
"""
    
    if len(keys) > 20:
        html_text += f"\n<b>... {len(keys) - 20} more keys</b>"
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_file_limit_text(message):
    """Handle file limit"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    current_limit = FREE_USER_LIMIT
    msg = bot.send_message(message.chat.id, f"📈 Current free user limit: {current_limit}\n\nEnter new limit (1-100):")
    bot.register_next_step_handler(msg, process_file_limit)

def process_file_limit(message):
    """Process file limit"""
    try:
        new_limit = int(message.text.strip())
        if 1 <= new_limit <= 100:
            update_file_limit(new_limit)
            bot.send_message(message.chat.id, f"✅ File limit updated to {new_limit}")
        else:
            bot.send_message(message.chat.id, "❌ Limit must be between 1 and 100")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid number")

def handle_bot_settings_text(message):
    """Handle bot settings"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if message.from_user.id == OWNER_ID:
        force_status = "🟢 Enabled" if force_join_enabled else "🔴 Disabled"
        markup.add(types.InlineKeyboardButton(f"🔐 Force Join: {force_status}", callback_data='toggle_force_join'))
    
    if message.from_user.id == OWNER_ID:
        lock_status = "🔓 Unlocked" if not bot_locked else "🔒 Locked"
        markup.add(types.InlineKeyboardButton(f"🔒 Bot Status: {lock_status}", callback_data='toggle_bot_lock'))
    
    markup.add(types.InlineKeyboardButton(f"📊 File Limit: {FREE_USER_LIMIT}", callback_data='change_file_limit'))
    
    if message.from_user.id == OWNER_ID:
        markup.add(types.InlineKeyboardButton("🛡️ Security Stats", callback_data='security_stats'))
    
    markup.add(types.InlineKeyboardButton("📢 Broadcast", callback_data='broadcast_settings'))
    markup.add(types.InlineKeyboardButton("ℹ️ System Info", callback_data='system_info'))
    markup.add(types.InlineKeyboardButton("💾 Backup Settings", callback_data='backup_settings'))
    markup.add(types.InlineKeyboardButton("🔐 Security Settings", callback_data='security_settings'))
    
    settings_text = f"""
⚙️ **BOT SETTINGS**

👤 **Admin:** {message.from_user.first_name}
🆔 **ID:** `{message.from_user.id}`
━━━━━━━━━━━━━━━━━━━━━
🔐 **Force Join:** {'Enabled' if force_join_enabled else 'Disabled'}
🔒 **Bot Lock:** {'Locked' if bot_locked else 'Unlocked'}
📊 **File Limit:** {FREE_USER_LIMIT}
🛡️ **Scans:** {security_scans['total_scans']}
━━━━━━━━━━━━━━━━━━━━━
    """
    
    bot.send_message(message.chat.id, settings_text, reply_markup=markup, parse_mode='Markdown')

def handle_add_admin_text(message):
    """Handle add admin"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    msg = bot.send_message(message.chat.id, "🆔 Enter user ID to promote to admin:")
    bot.register_next_step_handler(msg, process_add_admin)

def process_add_admin(message):
    """Process add admin"""
    try:
        admin_id = int(message.text.strip())
        
        if admin_id == OWNER_ID:
            bot.send_message(message.chat.id, "❌ Cannot add Owner")
            return
        
        if add_admin_to_db(admin_id, 'admin', OWNER_ID):
            admin_ids.add(admin_id)
            
            try:
                user_info = bot.get_chat(admin_id)
                username = f"@{user_info.username}" if user_info.username else "N/A"
                name = user_info.first_name
                
                bot.send_message(message.chat.id,
                                f"""
✅ **ADMIN ADDED**

👤 {name}
🆔 {admin_id}
👥 {username}
                                """,
                                parse_mode='Markdown')
                
                bot.send_message(admin_id,
                                f"""
🛡️ **YOU HAVE BEEN PROMOTED**

👑 By: {message.from_user.first_name}
🔑 Access: Full Admin Dashboard

Use /start to see your new menu.
                                """,
                                parse_mode='Markdown')
            except Exception as e:
                bot.send_message(message.chat.id, f"✅ Admin added (ID: {admin_id})")
                logger.error(f"❌ Failed to get user info: {e}")
        else:
            bot.send_message(message.chat.id, "❌ Failed to add admin")
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid ID")

def handle_remove_admin_text(message):
    """Handle remove admin"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    admins = get_all_admins()
    if not admins:
        bot.send_message(message.chat.id, "📭 No admins found")
        return
    
    admin_list = "🛡️ **CURRENT ADMINS:**\n\n"
    for admin_id, role in admins:
        if admin_id != OWNER_ID:
            try:
                user_info = bot.get_chat(admin_id)
                username = f"@{user_info.username}" if user_info.username else "N/A"
                admin_list += f"👤 {user_info.first_name} - `{admin_id}` {username} ({role})\n"
            except:
                admin_list += f"👤 Unknown - `{admin_id}` ({role})\n"
    
    admin_list += "\n🆔 Enter admin ID to remove:"
    msg = bot.send_message(message.chat.id, admin_list, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_remove_admin)

def process_remove_admin(message):
    """Process remove admin"""
    try:
        admin_id = int(message.text.strip())
        
        if admin_id == OWNER_ID:
            bot.send_message(message.chat.id, "❌ Cannot remove Owner")
            return
        
        if admin_id not in admin_ids:
            bot.send_message(message.chat.id, "❌ Not an admin")
            return
        
        if remove_admin_from_db(admin_id):
            admin_ids.discard(admin_id)
            
            try:
                user_info = bot.get_chat(admin_id)
                username = f"@{user_info.username}" if user_info.username else "N/A"
                name = user_info.first_name
                
                bot.send_message(message.chat.id,
                                f"""
❌ **ADMIN REMOVED**

👤 {name}
🆔 {admin_id}
👥 {username}
                                """,
                                parse_mode='Markdown')
                
                bot.send_message(admin_id,
                                f"""
⚠️ **YOU HAVE BEEN REMOVED**

👑 By: {message.from_user.first_name}
🔑 Access: Revoked
                                """,
                                parse_mode='Markdown')
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ Admin removed (ID: {admin_id})")
                logger.error(f"❌ Failed to get user info: {e}")
        else:
            bot.send_message(message.chat.id, "❌ Failed to remove admin")
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid ID")

def handle_ban_user_text(message):
    """Handle ban user"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    msg = bot.send_message(message.chat.id, "🆔 Enter user ID to ban:")
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    """Process ban user"""
    try:
        user_id = int(message.text.strip())
        
        if user_id == OWNER_ID:
            bot.send_message(message.chat.id, "❌ Cannot ban Owner")
            return
        
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "❌ Cannot ban Admin\nRemove admin first")
            return
        
        try:
            user_info = bot.get_chat(user_id)
            username = f"@{user_info.username}" if user_info.username else "N/A"
            name = user_info.first_name
        except:
            username = "N/A"
            name = "Unknown"
        
        success, result = ban_user(user_id, "Banned by owner")
        
        if success:
            bot.send_message(message.chat.id,
                           f"""
✅ **USER BANNED**

👤 {name}
🆔 `{user_id}`
👥 {username}
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 **Actions Taken:**
• Removed from active users
• Deleted all files
• Killed running processes
• Revoked subscription
                           """,
                           parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ {result}")
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid ID")

def handle_unban_user_text(message):
    """Handle unban user"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    banned_users = get_banned_users()
    if not banned_users:
        bot.send_message(message.chat.id, "📭 No banned users")
        return
    
    banned_text = "🚫 **BANNED USERS:**\n\n"
    for user in banned_users:
        user_id, ban_date, reason, ban_type, ban_expiry, username, first_name = user
        name = first_name or "Unknown"
        username_display = f"@{username}" if username else "N/A"
        banned_text += f"• `{user_id}` - {name} ({username_display})\n  ├─ Banned: {ban_date[:16]}\n  └─ Type: {ban_type}\n\n"
    
    banned_text += "\n🆔 Enter user ID to unban:"
    msg = bot.send_message(message.chat.id, banned_text, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    """Process unban user"""
    try:
        user_id = int(message.text.strip())
        
        success, result = unban_user(user_id)
        
        if success:
            bot.send_message(message.chat.id, f"✅ User `{user_id}` unbanned successfully", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ {result}")
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid ID")

def handle_view_banned_users_text(message):
    """Handle view banned users"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    banned_users = get_banned_users()
    if not banned_users:
        bot.send_message(message.chat.id, "📭 No banned users")
        return
    
    html_text = "<b>🚫 BANNED USERS</b>\n\n"
    
    for user in banned_users:
        user_id, ban_date, reason, ban_type, ban_expiry, username, first_name = user
        name = first_name or "Unknown"
        username_display = f"@{username}" if username else "N/A"
        time_ago = (datetime.now() - datetime.fromisoformat(ban_date)).days
        
        html_text += f"""
<b>👤 User:</b> {name}
<b>🆔 ID:</b> <code>{user_id}</code>
<b>📱 Username:</b> {username_display}
<b>📅 Banned:</b> {ban_date[:16]} ({time_ago} days ago)
<b>🔒 Type:</b> {ban_type}
"""
        if reason:
            html_text += f"<b>📝 Reason:</b> {reason}\n"
        if ban_type == 'temporary' and ban_expiry:
            html_text += f"<b>⏳ Expires:</b> {ban_expiry[:16]}\n"
        html_text += "─" * 30 + "\n"
    
    html_text += f"\n<b>📊 TOTAL:</b> {len(banned_users)} users"
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_force_stop_user_text(message):
    """Handle force stop user"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    msg = bot.send_message(message.chat.id, "🆔 Enter user ID to force stop all processes:")
    bot.register_next_step_handler(msg, process_force_stop_user)

def process_force_stop_user(message):
    """Process force stop user"""
    try:
        user_id = int(message.text.strip())
        
        stopped_count = cleanup_user_processes(user_id)
        
        bot.send_message(message.chat.id, f"✅ Force stopped {stopped_count} processes for user {user_id}")
        
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid ID")

def handle_admin_files_text(message):
    """Handle admin files"""
    user_id = message.from_user.id
    
    if user_id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    files = get_all_user_files_for_owner()
    
    if not files:
        bot.send_message(message.chat.id, "📭 No files found")
        return
    
    html_text = "<b>👑 ALL USER FILES</b>\n\n"
    
    current_user = None
    for file in files[:50]:
        file_user_id, username, first_name, file_name, file_type, file_size, upload_date, is_active, is_pending, downloads = file
        
        if current_user != file_user_id:
            current_user = file_user_id
            username_display = f"@{username}" if username else "N/A"
            html_text += f"\n<b>👤 {first_name}</b> ({username_display}) - <code>{file_user_id}</code>\n"
        
        status = "🟡 Pending" if is_pending else "🟢 Active" if is_active else "🔴 Inactive"
        html_text += f"├─ {status} <code>{file_name}</code> ({format_file_size(file_size)})\n"
        html_text += f"│  ├─ Uploaded: {upload_date[:16]}\n"
        html_text += f"│  └─ Downloads: {downloads}\n"
    
    if len(files) > 50:
        html_text += f"\n<b>... {len(files) - 50} more files</b>"
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_security_logs_text(message):
    """Handle security logs"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('''SELECT username, file_name, threat_count, risk_level, 
                            action_taken, log_date, details
                     FROM security_logs 
                     ORDER BY log_date DESC LIMIT 20''')
        logs = c.fetchall()
        
        if not logs:
            bot.send_message(message.chat.id, "📭 No security logs")
            return
        
        html_text = "<b>🛡️ SECURITY LOGS</b>\n\n"
        
        for log in logs:
            username, file_name, threat_count, risk_level, action_taken, log_date, details = log
            
            risk_emoji = "🔴" if risk_level == 'critical' else "🟠" if risk_level == 'high' else "🟡"
            
            html_text += f"""
{risk_emoji} <b>{risk_level.upper()}</b>
├─ <b>User:</b> @{username}
├─ <b>File:</b> <code>{file_name}</code>
├─ <b>Threats:</b> {threat_count}
├─ <b>Action:</b> {action_taken}
├─ <b>Time:</b> {log_date[:19]}
"""
            if details:
                html_text += f"└─ <b>Details:</b> {details[:100]}\n"
            html_text += "─" * 35 + "\n"
        
        c.execute('SELECT COUNT(*) FROM security_logs')
        total_logs = c.fetchone()[0]
        
        html_text += f"""
<b>📊 SUMMARY:</b>
├─ <b>Total Logs:</b> {total_logs}
├─ <b>Total Scans:</b> {security_scans['total_scans']}
├─ <b>Threats Found:</b> {security_scans['threats_found']}
└─ <b>Blocked Files:</b> {security_scans['blocked_files']}
        """
        
        bot.send_message(message.chat.id, html_text, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"❌ Error getting security logs: {e}")
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
    finally:
        conn.close()

# --- New Admin Handlers ---
def handle_analytics_text(message):
    """Handle analytics"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    stats = get_bot_statistics()
    
    # Create simple chart (you can enhance this with matplotlib)
    chart_data = f"""
📊 **ANALYTICS DASHBOARD**

━━━━━━━━━━━━━━━━━━━━━
📈 **DAILY STATISTICS**
━━━━━━━━━━━━━━━━━━━━━
Date: {datetime.now().strftime('%Y-%m-%d')}

Users: {'█' * min(stats['total_users'], 20)} {stats['total_users']}
Files: {'█' * min(stats['total_files'], 20)} {stats['total_files']}
Active: {'█' * min(stats['active_files'], 20)} {stats['active_files']}
Premium: {'█' * min(stats['premium_users'], 20)} {stats['premium_users']}

━━━━━━━━━━━━━━━━━━━━━
💾 **RESOURCE USAGE**
━━━━━━━━━━━━━━━━━━━━━
CPU: {'█' * int(stats['cpu_percent']/5)} {stats['cpu_percent']}%
Memory: {'█' * int(stats['memory_percent']/5)} {stats['memory_percent']}%
Disk: {'█' * int(stats['disk_percent']/5)} {stats['disk_percent']}%

━━━━━━━━━━━━━━━━━━━━━
🛡️ **SECURITY**
━━━━━━━━━━━━━━━━━━━━━
Scans: {security_scans['total_scans']}
Threats: {security_scans['threats_found']}
Blocked: {security_scans['blocked_files']}
    """
    
    bot.send_message(message.chat.id, chart_data, parse_mode='Markdown')

def handle_api_keys_text(message):
    """Handle API keys"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''SELECT api_key, user_id, created_date, expires_date, last_used, permissions, requests_count
                 FROM api_keys ORDER BY created_date DESC LIMIT 20''')
    keys = c.fetchall()
    conn.close()
    
    if not keys:
        bot.send_message(message.chat.id, "📭 No API keys found")
        return
    
    html_text = "<b>🔐 API KEYS</b>\n\n"
    
    for key in keys:
        api_key, user_id, created, expires, last_used, permissions, requests = key
        html_text += f"""
<b>Key:</b> <code>{api_key[:20]}...</code>
├─ <b>User:</b> <code>{user_id}</code>
├─ <b>Created:</b> {created[:16]}
├─ <b>Expires:</b> {expires[:16] if expires else 'Never'}
├─ <b>Last Used:</b> {last_used[:16] if last_used else 'Never'}
├─ <b>Permissions:</b> {permissions}
└─ <b>Requests:</b> {requests}
"""
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_webhooks_text(message):
    """Handle webhooks"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''SELECT webhook_id, user_id, url, events, is_active, created_date
                 FROM webhooks ORDER BY created_date DESC''')
    webhooks = c.fetchall()
    conn.close()
    
    if not webhooks:
        bot.send_message(message.chat.id, "🌐 No webhooks configured")
        return
    
    html_text = "<b>🌐 WEBHOOKS</b>\n\n"
    
    for webhook in webhooks:
        webhook_id, user_id, url, events, is_active, created = webhook
        status = "✅ Active" if is_active else "❌ Inactive"
        html_text += f"""
<b>ID:</b> {webhook_id}
├─ <b>User:</b> <code>{user_id}</code>
├─ <b>URL:</b> {url[:50]}...
├─ <b>Events:</b> {events}
├─ <b>Status:</b> {status}
└─ <b>Created:</b> {created[:16]}

"""
    
    bot.send_message(message.chat.id, html_text, parse_mode='HTML')

def handle_docker_text(message):
    """Handle Docker"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    if not docker_client:
        bot.send_message(message.chat.id, "❌ Docker not available")
        return
    
    try:
        containers = docker_client.containers.list(all=True)
        images = docker_client.images.list()
        
        html_text = f"""
<b>🐳 DOCKER STATUS</b>

━━━━━━━━━━━━━━━━━━━━━
<b>📊 OVERVIEW</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>Containers:</b> {len(containers)}
├─ <b>Images:</b> {len(images)}
└─ <b>Version:</b> {docker_client.version()['Version']}

━━━━━━━━━━━━━━━━━━━━━
<b>📦 CONTAINERS</b>
━━━━━━━━━━━━━━━━━━━━━
"""
        
        for container in containers[:10]:
            status = "🟢" if container.status == 'running' else "🔴"
            html_text += f"{status} <code>{container.name[:20]}</code> - {container.status}\n"
        
        if len(containers) > 10:
            html_text += f"... {len(containers) - 10} more\n"
        
        bot.send_message(message.chat.id, html_text, parse_mode='HTML')
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Docker error: {str(e)}")

def handle_email_text(message):
    """Handle email"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    msg = bot.send_message(message.chat.id, "📧 Enter email to send test message:")
    bot.register_next_step_handler(msg, process_test_email)

def process_test_email(message):
    """Process test email"""
    email = message.text.strip()
    send_email(email, "Test from KELVIN Cloud", "This is a test email from your bot.")
    bot.send_message(message.chat.id, f"✅ Test email sent to {email}")

def handle_reports_text(message):
    """Handle reports"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    stats = get_bot_statistics()
    key_stats = get_key_stats()
    
    report = f"""
<b>📊 SYSTEM REPORT</b>
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━
<b>1. USER STATISTICS</b>
━━━━━━━━━━━━━━━━━━━━━
• Total Users: {stats['total_users']}
• Premium Users: {stats['premium_users']} ({stats['premium_users']/stats['total_users']*100:.1f}% if stats['total_users'] > 0 else 0)
• Banned Users: {stats['banned_users']}

━━━━━━━━━━━━━━━━━━━━━
<b>2. FILE STATISTICS</b>
━━━━━━━━━━━━━━━━━━━━━
• Total Files: {stats['total_files']}
• Active Files: {stats['active_files']} ({stats['active_files']/stats['total_files']*100:.1f}% if stats['total_files'] > 0 else 0)
• Total Downloads: {stats['total_downloads']}
• Storage Used: {stats['total_storage']}

━━━━━━━━━━━━━━━━━━━━━
<b>3. KEY STATISTICS</b>
━━━━━━━━━━━━━━━━━━━━━
• Total Keys: {key_stats['total_keys']}
• Active Keys: {key_stats['active_keys']}
• Keys Used: {key_stats['total_used']}
• Unique Users: {key_stats['unique_users']}

━━━━━━━━━━━━━━━━━━━━━
<b>4. SYSTEM RESOURCES</b>
━━━━━━━━━━━━━━━━━━━━━
• CPU Usage: {stats['cpu_percent']}%
• Memory Usage: {stats['memory_percent']}% ({stats['memory_used']}/{stats['memory_total']})
• Disk Usage: {stats['disk_percent']}% ({stats['disk_used']}/{stats['disk_total']})
• Uptime: {stats['uptime']}

━━━━━━━━━━━━━━━━━━━━━
<b>5. SECURITY</b>
━━━━━━━━━━━━━━━━━━━━━
• Total Scans: {stats['security_scans']['total_scans']}
• Threats Found: {stats['security_scans']['threats_found']}
• High Risk Files: {stats['security_scans']['high_risk_files']}
• Blocked Files: {stats['security_scans']['blocked_files']}
• Security Alerts: {stats['security_alerts']}
    """
    
    # Save report to file
    report_file = os.path.join(LOGS_DIR, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_file, 'w') as f:
        f.write(report)
    
    with open(report_file, 'rb') as f:
        bot.send_document(
            message.chat.id,
            f,
            caption=f"📊 System Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    
    bot.send_message(message.chat.id, report, parse_mode='HTML')

def handle_system_text(message):
    """Handle system"""
    if message.from_user.id != OWNER_ID:
        bot.send_message(message.chat.id, "❌ Owner Only")
        return
    
    system_info = f"""
<b>🔧 SYSTEM INFORMATION</b>

━━━━━━━━━━━━━━━━━━━━━
<b>🖥️ PLATFORM</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>OS:</b> {platform.system()} {platform.release()}
├─ <b>Arch:</b> {platform.machine()}
├─ <b>Hostname:</b> {socket.gethostname()}
└─ <b>Python:</b> {platform.python_version()}

━━━━━━━━━━━━━━━━━━━━━
<b>🌐 NETWORK</b>
━━━━━━━━━━━━━━━━━━━━━
"""
    
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        system_info += f"├─ <b>Hostname:</b> {hostname}\n"
        system_info += f"├─ <b>IP Address:</b> {ip_address}\n"
        
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    system_info += f"├─ <b>Interface {interface}:</b> {addr['addr']}\n"
    except:
        pass
    
    system_info += f"""
━━━━━━━━━━━━━━━━━━━━━
<b>📦 STORAGE</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>Base Dir:</b> {BASE_DIR}
├─ <b>Uploads Dir:</b> {UPLOAD_BOTS_DIR}
├─ <b>Database:</b> {DATABASE_PATH}
├─ <b>Backup Dir:</b> {BACKUP_DIR}
└─ <b>Logs Dir:</b> {LOGS_DIR}

━━━━━━━━━━━━━━━━━━━━━
<b>⚙️ PROCESSES</b>
━━━━━━━━━━━━━━━━━━━━━
├─ <b>Running Scripts:</b> {len(bot_scripts)}
├─ <b>Active Users:</b> {len(active_users)}
└─ <b>Thread Pool:</b> {executor._max_workers}
    """
    
    bot.send_message(message.chat.id, system_info, parse_mode='HTML')

def handle_monitor_text(message):
    """Handle monitor"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    stats = get_bot_statistics()
    
    monitor_text = f"""
📡 **SYSTEM MONITOR**

━━━━━━━━━━━━━━━━━━━━━
🟢 **STATUS:** ONLINE
⏱️ **Uptime:** {stats['uptime']}

━━━━━━━━━━━━━━━━━━━━━
💻 **CPU**
━━━━━━━━━━━━━━━━━━━━━
Usage: {stats['cpu_percent']}%
{'█' * int(stats['cpu_percent']/5)}{'░' * (20 - int(stats['cpu_percent']/5))}

━━━━━━━━━━━━━━━━━━━━━
🧠 **MEMORY**
━━━━━━━━━━━━━━━━━━━━━
Usage: {stats['memory_percent']}%
Used: {stats['memory_used']}
Total: {stats['memory_total']}
{'█' * int(stats['memory_percent']/5)}{'░' * (20 - int(stats['memory_percent']/5))}

━━━━━━━━━━━━━━━━━━━━━
💾 **DISK**
━━━━━━━━━━━━━━━━━━━━━
Usage: {stats['disk_percent']}%
Used: {stats['disk_used']}
Total: {stats['disk_total']}
{'█' * int(stats['disk_percent']/5)}{'░' * (20 - int(stats['disk_percent']/5))}

━━━━━━━━━━━━━━━━━━━━━
📊 **ACTIVITY**
━━━━━━━━━━━━━━━━━━━━━
Users Online: {stats['total_users']}
Active Files: {stats['active_files']}
Running Scripts: {len(bot_scripts)}
Security Scans: {stats['security_scans']['total_scans']}
    """
    
    bot.send_message(message.chat.id, monitor_text, parse_mode='Markdown')

def handle_backup_text(message):
    """Handle backup"""
    if message.from_user.id not in admin_ids:
        bot.send_message(message.chat.id, "❌ Admin Only")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💾 Create Backup", callback_data='create_backup'),
        types.InlineKeyboardButton("📋 List Backups", callback_data='list_backups'),
        types.InlineKeyboardButton("⚙️ Backup Settings", callback_data='backup_settings'),
        types.InlineKeyboardButton("🔄 Restore", callback_data='restore_backup')
    )
    
    bot.send_message(
        message.chat.id,
        "💾 **BACKUP MANAGER**\n\nChoose an option:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

# --- User Text Handlers ---
def handle_back_to_main_text(message):
    """Handle back to main"""
    user_id = message.from_user.id
    markup = create_main_menu_keyboard(user_id)
    bot.send_message(message.chat.id, "⬅️ Back to Main Menu", reply_markup=markup)

def handle_upload_file_text(message):
    """Handle upload file"""
    user_id = message.from_user.id
    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)
    
    if current_files >= file_limit and not is_premium_user(user_id):
        bot.send_message(message.chat.id, f"❌ Storage limit reached ({FREE_USER_LIMIT} files)\n💎 Upgrade to Premium for more space.")
        return
    
    supported_files = ", ".join([ext for ext in SUPPORTED_EXTENSIONS.keys()])
    bot.send_message(message.chat.id,
                    f"""
📤 **UPLOAD FILE**

Supported extensions: `{supported_files}`
Max file size: 50MB

Upload your script or code file now.
Auto-deployment and dependency installation available.

⚠️ All files are scanned for security threats.
                    """,
                    parse_mode='Markdown')

def handle_manage_files_text(message):
    """Handle manage files"""
    user_id = message.from_user.id
    user_files_list = user_files.get(user_id, [])
    
    if not user_files_list:
        bot.send_message(message.chat.id, "📭 No files found. Upload a file to get started.")
        return
    
    files_text = f"📂 **MY FILES:**\n\n"
    
    for file_name, file_type, file_path in user_files_list:
        is_running = is_bot_running(user_id, file_name)
        status = "🟢 Running" if is_running else "🔴 Stopped"
        file_size = format_file_size(os.path.getsize(file_path)) if os.path.exists(file_path) else "Unknown"
        files_text += f"• `{file_name}`\n  ├─ {status}\n  └─ Size: {file_size}\n\n"
    
    files_text += "\nTap a file below to manage it."
    
    markup = create_manage_files_keyboard(user_id)
    bot.send_message(message.chat.id, files_text, reply_markup=markup, parse_mode='Markdown')

def handle_redeem_key_text(message):
    """Handle redeem key"""
    msg = bot.send_message(message.chat.id, "🔑 Enter your premium key (format: KELVIN-XXXX-XXXX-XXXX):")
    bot.register_next_step_handler(msg, process_redeem_key)

def process_redeem_key(message):
    """Process redeem key"""
    user_id = message.from_user.id
    
    if force_join_enabled and user_id not in admin_ids and not check_force_join(user_id):
        force_message = create_force_join_message()
        force_markup = create_force_join_keyboard()
        bot.send_message(message.chat.id, force_message, reply_markup=force_markup, parse_mode='Markdown')
        return
    
    key_value = message.text.strip().upper()
    
    if not key_value.startswith('KELVIN-') or len(key_value) < 16:
        bot.reply_to(message, f"❌ Invalid format. Use: KELVIN-XXXX-XXXX-XXXX\nExample: KELVIN-A1B2-C3D4-E5F6")
        return
    
    # Get client info for logging
    ip_address = get_client_ip(message)
    user_agent = f"Telegram/{message.from_user.language_code}"
    
    success, result_msg = redeem_subscription_key(key_value, user_id, ip_address, user_agent)
    bot.reply_to(message, result_msg, parse_mode='Markdown')

def handle_buy_subscription_text(message):
    """Handle buy subscription"""
    html_text = """
<b>💎 PREMIUM PLANS</b>

━━━━━━━━━━━━━━━━━━━━━
<b>♣️ WEEKLY</b>
━━━━━━━━━━━━━━━━━━━━━
│ <b>Price:</b> $0.50 / 2000 Ks
│ <b>Files:</b> 5 Files
│ <b>Support:</b> Basic
└─ <b>Best for:</b> Testing

━━━━━━━━━━━━━━━━━━━━━
<b>♦️ MONTHLY</b> (Popular)
━━━━━━━━━━━━━━━━━━━━━
│ <b>Price:</b> $2.00 / 8000 Ks
│ <b>Files:</b> 15 Files
│ <b>Support:</b> Standard
└─ <b>Best for:</b> Small projects

━━━━━━━━━━━━━━━━━━━━━
<b>♥️ 3 MONTHS</b>
━━━━━━━━━━━━━━━━━━━━━
│ <b>Price:</b> $5.50 / 23000 Ks
│ <b>Files:</b> Unlimited
│ <b>Support:</b> Priority
└─ <b>Best for:</b> Active developers

━━━━━━━━━━━━━━━━━━━━━
<b>♠️ 1 YEAR</b>
━━━━━━━━━━━━━━━━━━━━━
│ <b>Price:</b> $20.00 / 80000 Ks
│ <b>Files:</b> Unlimited
│ <b>Support:</b> Priority+
│ <b>Bonus:</b> Bot Admin
└─ <b>Best for:</b> Professional use

━━━━━━━━━━━━━━━━━━━━━
<b>⚡ LIFETIME</b>
━━━━━━━━━━━━━━━━━━━━━
│ <b>Price:</b> $50.00 / 200000 Ks
│ <b>Files:</b> Unlimited
│ <b>Support:</b> 24/7 VIP
│ <b>Bonus:</b> Bot Admin + Source
└─ <b>Best for:</b> Enterprise

━━━━━━━━━━━━━━━━━━━━━
<b>💳 Payment Methods:</b>
• Binance
• Bybit
• KPAY
• WAVE Pay
• Crypto (USDT)

<b>📲 Contact Support:</b> """ + YOUR_USERNAME + """

<i>All plans include auto-deployment, security scanning, and real-time monitoring.</i>
    """
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 Contact Support", url=f"https://t.me/{YOUR_USERNAME[1:]}"))
    markup.add(types.InlineKeyboardButton("🔑 Redeem Key", callback_data='redeem_key'))
    markup.add(types.InlineKeyboardButton("📋 Compare Plans", callback_data='compare_plans'))
    
    bot.send_message(message.chat.id, html_text, reply_markup=markup, parse_mode='HTML')

def handle_my_info_text(message):
    """Handle my info"""
    user_id = message.from_user.id
    user_status = get_user_status(user_id)
    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)
    user_stats = get_user_statistics(user_id)
    
    subscription_info = ""
    if is_premium_user(user_id):
        subscription_data = user_subscriptions.get(user_id, {})
        expiry = subscription_data.get('expiry', datetime.now())
        days_left = (expiry - datetime.now()).days
        hours_left = (expiry - datetime.now()).seconds // 3600
        subscription_info = f"📅 Expires: {expiry.strftime('%Y-%m-%d %H:%M')}\n⏳ Time Left: {days_left}d {hours_left}h"
    else:
        subscription_info = "⏳ No active subscription"
    
    limit_str = str(file_limit) if file_limit != float('inf') else "∞"
    
    my_info_text = f"""
👤 **USER PROFILE**

━━━━━━━━━━━━━━━━━━━━━
📋 **BASIC INFO**
━━━━━━━━━━━━━━━━━━━━━
├─ ID: `{user_id}`
├─ Name: {message.from_user.first_name}
├─ Username: @{message.from_user.username if message.from_user.username else '-'}
└─ Status: {user_status}

━━━━━━━━━━━━━━━━━━━━━
💎 **SUBSCRIPTION**
━━━━━━━━━━━━━━━━━━━━━
{subscription_info}
├─ Files Used: {current_files}/{limit_str}
└─ Storage Used: {user_stats['storage_used'] if user_stats else '0 B'}

━━━━━━━━━━━━━━━━━━━━━
📊 **ACTIVITY**
━━━━━━━━━━━━━━━━━━━━━
├─ Total Uploads: {user_stats['total_uploads'] if user_stats else 0}
├─ Total Downloads: {user_stats['total_downloads'] if user_stats else 0}
├─ Bandwidth Used: {user_stats['bandwidth_used'] if user_stats else '0 B'}
├─ Active Files: {sum(1 for fn, _, _ in user_files.get(user_id, []) if is_bot_running(user_id, fn))}
└─ Joined: {user_stats['join_date'] if user_stats else 'N/A'}

━━━━━━━━━━━━━━━━━━━━━
📁 **FILES**
━━━━━━━━━━━━━━━━━━━━━
├─ Total: {current_files}
├─ Running: {sum(1 for fn, _, _ in user_files.get(user_id, []) if is_bot_running(user_id, fn))}
└─ Stopped: {sum(1 for fn, _, _ in user_files.get(user_id, []) if not is_bot_running(user_id, fn))}
    """
    
    markup = types.InlineKeyboardMarkup()
    if not is_premium_user(user_id):
        markup.add(types.InlineKeyboardButton("💎 Upgrade Now", callback_data='buy_subscription'))
    markup.add(types.InlineKeyboardButton("📁 Manage Files", callback_data='manage_files'))
    markup.add(types.InlineKeyboardButton("🔑 Redeem Key", callback_data='redeem_key'))
    
    bot.send_message(message.chat.id, my_info_text, reply_markup=markup, parse_mode='Markdown')

def handle_status_text(message):
    """Handle status"""
    user_id = message.from_user.id
    user_status = get_user_status(user_id)
    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)
    stats = get_bot_statistics()
    
    status_text = f"""
📊 **SYSTEM STATUS**

━━━━━━━━━━━━━━━━━━━━━
👤 **YOUR STATUS**
━━━━━━━━━━━━━━━━━━━━━
├─ Plan: {user_status}
├─ Files: {current_files}/{file_limit if file_limit != float('inf') else '∞'}
├─ Running: {sum(1 for fn, _, _ in user_files.get(user_id, []) if is_bot_running(user_id, fn))}
└─ Stopped: {sum(1 for fn, _, _ in user_files.get(user_id, []) if not is_bot_running(user_id, fn))}

━━━━━━━━━━━━━━━━━━━━━
🌍 **GLOBAL STATUS**
━━━━━━━━━━━━━━━━━━━━━
├─ Total Users: {stats['total_users']}
├─ Premium Users: {stats['premium_users']}
├─ Total Files: {stats['total_files']}
├─ Active Files: {stats['active_files']}
└─ Total Downloads: {stats['total_downloads']}

━━━━━━━━━━━━━━━━━━━━━
⚙️ **BOT STATUS**
━━━━━━━━━━━━━━━━━━━━━
├─ Bot Lock: {'🔒 Locked' if bot_locked else '🔓 Open'}
├─ Force Join: {'✅ On' if force_join_enabled else '❌ Off'}
├─ Free Limit: {FREE_USER_LIMIT}
└─ Uptime: {stats['uptime']}

━━━━━━━━━━━━━━━━━━━━━
🛡️ **SECURITY**
━━━━━━━━━━━━━━━━━━━━━
├─ Total Scans: {security_scans['total_scans']}
├─ Threats Found: {security_scans['threats_found']}
└─ Blocked Files: {security_scans['blocked_files']}
    """
    
    bot.send_message(message.chat.id, status_text, parse_mode='Markdown')

def handle_tools_text(message):
    """Handle tools"""
    user_id = message.from_user.id
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Speed Test", callback_data='speed_test'),
        types.InlineKeyboardButton("🌐 IP Info", callback_data='ip_info'),
        types.InlineKeyboardButton("🔍 DNS Lookup", callback_data='dns_lookup'),
        types.InlineKeyboardButton("📧 WHOIS", callback_data='whois_lookup'),
        types.InlineKeyboardButton("🔐 SSL Check", callback_data='ssl_check'),
        types.InlineKeyboardButton("📡 Ping", callback_data='ping_test')
    )
    
    tools_text = """
🔧 **TOOLS & UTILITIES**

Select a tool to use:

• Speed Test - Test your connection speed
• IP Info - Get information about an IP
• DNS Lookup - Check DNS records
• WHOIS - Domain information lookup
• SSL Check - Check SSL certificate
• Ping Test - Test network latency
    """
    
    bot.send_message(message.chat.id, tools_text, reply_markup=markup, parse_mode='Markdown')

def handle_user_webhooks_text(message):
    """Handle user webhooks"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''SELECT webhook_id, url, events, is_active, created_date
                 FROM webhooks WHERE user_id = ? ORDER BY created_date DESC''', (user_id,))
    webhooks = c.fetchall()
    conn.close()
    
    if not webhooks:
        text = "🌐 **No webhooks configured**\n\nCreate a webhook to receive real-time notifications about your files."
    else:
        text = "🌐 **YOUR WEBHOOKS**\n\n"
        for webhook in webhooks:
            webhook_id, url, events, is_active, created = webhook
            status = "✅ Active" if is_active else "❌ Inactive"
            text += f"""
<b>ID:</b> {webhook_id}
├─ <b>URL:</b> {url[:50]}...
├─ <b>Events:</b> {events}
├─ <b>Status:</b> {status}
└─ <b>Created:</b> {created[:16]}

"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("➕ Create Webhook", callback_data='create_webhook'))
    if webhooks:
        markup.add(types.InlineKeyboardButton("🗑️ Delete Webhook", callback_data='delete_webhook'))
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')

def handle_user_backup_text(message):
    """Handle user backup"""
    user_id = message.from_user.id
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''SELECT backup_id, file_name, size, created_date
                 FROM backups WHERE user_id = ? ORDER BY created_date DESC LIMIT 10''', (user_id,))
    backups = c.fetchall()
    conn.close()
    
    if not backups:
        text = "💾 **No backups found**\n\nCreate a backup to save your files."
    else:
        text = "💾 **YOUR BACKUPS**\n\n"
        for backup in backups:
            backup_id, file_name, size, created = backup
            text += f"""
<b>ID:</b> {backup_id}
├─ <b>File:</b> {file_name}
├─ <b>Size:</b> {format_file_size(size)}
└─ <b>Created:</b> {created[:16]}

"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💾 Create Backup", callback_data='create_user_backup'))
    if backups:
        markup.add(types.InlineKeyboardButton("🔄 Restore", callback_data='restore_user_backup'))
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')

def handle_user_monitor_text(message):
    """Handle user monitor"""
    user_id = message.from_user.id
    stats = get_bot_statistics()
    user_stats = get_user_statistics(user_id)
    
    monitor_text = f"""
📡 **YOUR MONITOR**

━━━━━━━━━━━━━━━━━━━━━
📊 **USAGE**
━━━━━━━━━━━━━━━━━━━━━
├─ Files: {user_stats['current_files'] if user_stats else 0}
├─ Uploads: {user_stats['total_uploads'] if user_stats else 0}
├─ Downloads: {user_stats['total_downloads'] if user_stats else 0}
├─ Storage: {user_stats['storage_used'] if user_stats else '0 B'}
└─ Bandwidth: {user_stats['bandwidth_used'] if user_stats else '0 B'}

━━━━━━━━━━━━━━━━━━━━━
🟢 **ACTIVE PROCESSES**
━━━━━━━━━━━━━━━━━━━━━
"""
    
    running_count = 0
    for file_name, file_type, file_path in user_files.get(user_id, []):
        if is_bot_running(user_id, file_name):
            monitor_text += f"├─ 🟢 {file_name}\n"
            running_count += 1
    
    if running_count == 0:
        monitor_text += "├─ No active processes\n"
    
    monitor_text += f"""
└─ Total Running: {running_count}

━━━━━━━━━━━━━━━━━━━━━
🌍 **GLOBAL**
━━━━━━━━━━━━━━━━━━━━━
├─ Users Online: {stats['total_users']}
├─ System Load: {stats['cpu_percent']}%
└─ Uptime: {stats['uptime']}
    """
    
    bot.send_message(message.chat.id, monitor_text, parse_mode='Markdown')

# --- Security Alert Functions ---
def send_threat_alert_to_owner(report):
    """Send threat alert to owner"""
    if not report:
        return
    
    user_id = report['user_id']
    username = report['username'] or 'Unknown'
    file_name = report['file_name']
    threat_count = report['threat_count']
    risk_score = report['risk_score']
    critical_risk = report['critical_risk']
    high_risk = report['high_risk']
    
    username_clean = username.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    file_name_clean = file_name.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    
    risk_level = '🔴 CRITICAL' if critical_risk else '🟠 HIGH' if high_risk else '🟡 MEDIUM'
    
    alert_text = f"""
🚨 **SECURITY ALERT** 🚨

━━━━━━━━━━━━━━━━━━━━━
👤 **USER**
━━━━━━━━━━━━━━━━━━━━━
├─ ID: `{user_id}`
├─ Username: {username_clean}
└─ File: `{file_name_clean}`

━━━━━━━━━━━━━━━━━━━━━
⚠️ **THREAT ANALYSIS**
━━━━━━━━━━━━━━━━━━━━━
├─ Risk Level: {risk_level}
├─ Risk Score: {risk_score}/100
├─ Threats Found: {threat_count}
└─ Categories: {', '.join(report['threats_by_category'].keys())}

━━━━━━━━━━━━━━━━━━━━━
📋 **DETAILS**
━━━━━━━━━━━━━━━━━━━━━
"""
    
    for category, threats in list(report['threats_by_category'].items())[:3]:
        alert_text += f"├─ {category.upper()}: {len(threats)} threats\n"
        for threat in threats[:2]:
            content = threat['content'][:50].replace('`', "'")
            alert_text += f"│  └─ Line {threat['line']}: `{content}...`\n"
    
    alert_text += """
━━━━━━━━━━━━━━━━━━━━━
⚡ **ACTIONS**
━━━━━━━━━━━━━━━━━━━━━
"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if critical_risk:
        markup.add(
            types.InlineKeyboardButton("🚫 BAN USER", callback_data=f'security_ban_{user_id}_{file_name_clean}'),
            types.InlineKeyboardButton("🔒 BLOCK UPLOADS", callback_data=f'security_block_{user_id}_{file_name_clean}')
        )
        alert_text += "• CRITICAL: File auto-blocked\n"
    elif high_risk:
        markup.add(
            types.InlineKeyboardButton("🚫 BAN USER", callback_data=f'security_ban_{user_id}_{file_name_clean}'),
            types.InlineKeyboardButton("⚠️ WARN USER", callback_data=f'security_warn_{user_id}_{file_name_clean}')
        )
    else:
        markup.add(
            types.InlineKeyboardButton("⚠️ WARN USER", callback_data=f'security_warn_{user_id}_{file_name_clean}'),
            types.InlineKeyboardButton("👁️ IGNORE", callback_data=f'security_ignore_{user_id}_{file_name_clean}')
        )
    
    markup.add(
        types.InlineKeyboardButton("🗑️ DELETE FILE", callback_data=f'security_delete_{user_id}_{file_name_clean}'),
        types.InlineKeyboardButton("📋 FULL REPORT", callback_data=f'security_report_{user_id}_{file_name_clean}')
    )
    
    try:
        bot.send_message(OWNER_ID, alert_text, reply_markup=markup, parse_mode='Markdown')
        
        if not critical_risk:
            try:
                with open(report['file_path'], 'rb') as f:
                    bot.send_document(
                        OWNER_ID,
                        f,
                        caption=f"🚨 Suspicious file: {file_name_clean}\nUser: {username_clean} ({user_id})\nRisk: {risk_level}"
                    )
            except:
                pass
        
        log_security_event(user_id, username, file_name, threat_count,
                          'critical' if critical_risk else 'high' if high_risk else 'medium',
                          'alerted', f"Risk score: {risk_score}")
        
        logger.warning(f"⚠️ Security alert sent for user {user_id}, file {file_name}")
        
    except Exception as e:
        logger.error(f"❌ Failed to send security alert: {e}")
        try:
            simple_alert = f"""
🚨 SECURITY ALERT 🚨

User ID: {user_id}
Username: {username}
File: {file_name}
Risk: {risk_level}
Threats: {threat_count}

Action required.
            """
            bot.send_message(OWNER_ID, simple_alert, reply_markup=markup)
        except Exception as e2:
            logger.error(f"❌ Failed to send fallback alert: {e2}")

# --- Security Action Handlers ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('security_'))
def handle_security_actions(call):
    """Handle security actions"""
    try:
        parts = call.data.split('_')
        if len(parts) < 3:
            bot.answer_callback_query(call.id, "❌ Invalid action", show_alert=True)
            return
            
        action = parts[1]
        user_id_str = parts[2]
        file_name = '_'.join(parts[3:]) if len(parts) > 3 else "Unknown"
        
        user_id = int(user_id_str)
        
        if call.from_user.id != OWNER_ID:
            bot.answer_callback_query(call.id, "❌ Owner Only", show_alert=True)
            return
        
        if action == 'ban':
            success, result = ban_user(user_id, f"Banned for malicious file: {file_name}")
            if success:
                log_security_event(user_id, "Unknown", file_name, 0, 'critical', 'banned')
                bot.answer_callback_query(call.id, f"✅ Banned user {user_id}", show_alert=True)
                bot.edit_message_text(
                    f"✅ **USER BANNED**\n\n👤 User ID: `{user_id}`\n📁 File: `{file_name}`\n🕐 {datetime.now().strftime('%H:%M:%S')}",
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='Markdown'
                )
            else:
                bot.answer_callback_query(call.id, f"❌ {result}", show_alert=True)
        
        elif action == 'warn':
            if user_id not in user_warnings:
                user_warnings[user_id] = 0
            
            user_warnings[user_id] += 1
            warning_count = user_warnings[user_id]
            
            try:
                bot.send_message(user_id,
                    f"""⚠️ **SECURITY WARNING** ⚠️

Your uploaded file `{file_name}` has triggered security checks.
This is warning #{warning_count} of {MAX_WARNINGS}.

Repeated violations may result in account suspension.

Please review your code for security issues.
                    """,
                    parse_mode='Markdown'
                )
                
                if warning_count >= MAX_WARNINGS:
                    success, result = ban_user(user_id, f"Auto-banned after {MAX_WARNINGS} warnings")
                    if success:
                        bot.send_message(user_id,
                                       f"""
🚫 **ACCOUNT BANNED**

⚠️ You have exceeded the warning limit ({MAX_WARNINGS})
📁 All your files have been deleted

👑 **Contact:** {YOUR_USERNAME}
                                       """,
                                       parse_mode='Markdown')
                        bot.answer_callback_query(call.id, f"🚫 Auto-banned user (3/3)", show_alert=True)
                        bot.edit_message_text(
                            f"🚫 **AUTO-BANNED**\n\n👤 User ID: `{user_id}`\n📁 File: `{file_name}`\n⚠️ Warning #{warning_count}/{MAX_WARNINGS}",
                            call.message.chat.id,
                            call.message.message_id,
                            parse_mode='Markdown'
                        )
                    else:
                        bot.answer_callback_query(call.id, f"❌ {result}", show_alert=True)
                else:
                    bot.answer_callback_query(call.id, f"⚠️ Warned user ({warning_count}/{MAX_WARNINGS})", show_alert=True)
                    bot.edit_message_text(
                        f"⚠️ **USER WARNED**\n\n👤 User ID: `{user_id}`\n📁 File: `{file_name}`\n⚠️ Warning #{warning_count}/{MAX_WARNINGS}",
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown'
                    )
            except:
                bot.answer_callback_query(call.id, "❌ Cannot message user", show_alert=True)
        
        elif action == 'delete':
            remove_user_file_db(user_id, file_name)
            log_security_event(user_id, "Unknown", file_name, 0, 'medium', 'file_deleted')
            bot.answer_callback_query(call.id, f"🗑️ Deleted {file_name}", show_alert=True)
            bot.edit_message_text(
                f"🗑️ **FILE DELETED**\n\n📁 File: `{file_name}`\n👤 User ID: `{user_id}`",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
        
        elif action == 'ignore':
            approve_pending_file(user_id, file_name)
            
            log_security_event(user_id, "Unknown", file_name, 0, 'low', 'ignored', 'Manually approved by owner')
            bot.answer_callback_query(call.id, "👁️ Ignored", show_alert=True)
            bot.edit_message_text(
                f"👁️ **THREAT IGNORED**\n\n📁 File: `{file_name}`\n👤 User ID: `{user_id}`\n✅ Deployment allowed",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            
            try:
                user_info = bot.get_chat(user_id)
                
                deploy_msg = f"""
🚀 **DEPLOYMENT APPROVED** 🚀

Your file `{file_name}` has been manually approved for deployment by the owner.

🔧 **File Details:**
• Name: `{file_name}`
• Status: ✅ Approved

📊 **Your Usage:**
• Files: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}
• Status: {get_user_status(user_id)}

Tap the button below to deploy:
                """
                
                deploy_markup = types.InlineKeyboardMarkup()
                deploy_markup.add(types.InlineKeyboardButton("🚀 Deploy Now", callback_data=f'deploy_{user_id}_{file_name}'))
                
                bot.send_message(user_id, deploy_msg, reply_markup=deploy_markup, parse_mode='Markdown')
                
            except Exception as e:
                logger.error(f"❌ Error sending deploy message: {e}")
        
        elif action == 'block':
            success, result = ban_user(user_id, f"Uploads blocked for malicious file: {file_name}")
            if success:
                log_security_event(user_id, "Unknown", file_name, 0, 'high', 'blocked_uploads')
                bot.answer_callback_query(call.id, f"🔒 Blocked user uploads", show_alert=True)
                bot.edit_message_text(
                    f"🔒 **UPLOADS BLOCKED**\n\n👤 User ID: `{user_id}`\n📁 File: `{file_name}`\n🚫 Future uploads disabled",
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='Markdown'
                )
        
        elif action == 'report':
            bot.answer_callback_query(call.id, "📋 Full report sent", show_alert=False)
            
            # Send detailed report
            report_text = f"""
📋 **FULL SECURITY REPORT**

━━━━━━━━━━━━━━━━━━━━━
👤 **USER**
━━━━━━━━━━━━━━━━━━━━━
├─ ID: `{user_id}`
├─ Username: @{call.message.from_user.username}
└─ File: `{file_name}`

━━━━━━━━━━━━━━━━━━━━━
🔍 **DETAILED ANALYSIS**
━━━━━━━━━━━━━━━━━━━━━
"""
            
            # Get file info
            file_path = None
            for fn, ft, fp in user_files.get(user_id, []):
                if fn == file_name:
                    file_path = fp
                    break
            
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                report_text += f"\n📄 File size: {format_file_size(file_size)}\n"
                
                # Show first few lines
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[:20]
                
                report_text += "\n📝 First 20 lines:\n```\n"
                for i, line in enumerate(lines, 1):
                    report_text += f"{i:3d}: {line[:100]}\n"
                report_text += "```\n"
            
            bot.send_message(OWNER_ID, report_text, parse_mode='Markdown')
    
    except Exception as e:
        logger.error(f"❌ Error in security action: {e}")
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)

# --- Broadcast Handlers ---
def handle_confirm_broadcast(call):
    """Handle confirm broadcast"""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ Admin Only", show_alert=True)
        return
    
    try:
        message_id = int(call.data.split('_')[2])
        
        if message_id in broadcast_messages:
            broadcast_text = broadcast_messages[message_id]
        else:
            bot.answer_callback_query(call.id, "❌ Message not found", show_alert=True)
            return
        
        sent_count = 0
        failed_count = 0
        
        status_msg = bot.send_message(call.message.chat.id, "📢 Broadcasting... 0%")
        
        total_users = len(active_users)
        for i, user_id in enumerate(active_users):
            try:
                bot.send_message(user_id, broadcast_text)
                sent_count += 1
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Failed to send to {user_id}: {e}")
            
            if i % 10 == 0:
                try:
                    progress = int((i + 1) / total_users * 100)
                    bot.edit_message_text(f"📢 Broadcasting... {progress}%", 
                                        status_msg.chat.id, status_msg.message_id)
                except:
                    pass
        
        bot.answer_callback_query(call.id, f"✅ Sent: {sent_count}, Failed: {failed_count}")
        bot.edit_message_text(f"📢 Broadcast Complete\n✅ Success: {sent_count}\n❌ Failed: {failed_count}", 
                             call.message.chat.id, call.message.message_id)
        
        if message_id in broadcast_messages:
            del broadcast_messages[message_id]
        
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {str(e)}", show_alert=True)

def handle_cancel_broadcast(call):
    """Handle cancel broadcast"""
    try:
        parts = call.data.split('_')
        if len(parts) > 2:
            message_id = int(parts[2])
            if message_id in broadcast_messages:
                del broadcast_messages[message_id]
        
        bot.answer_callback_query(call.id, "❌ Cancelled")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        logger.error(f"❌ Error in cancel broadcast: {e}")

# --- Settings Handlers ---
def handle_toggle_force_join(call):
    """Handle toggle force join"""
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Owner Only", show_alert=True)
        return
    
    try:
        new_status = not force_join_enabled
        update_force_join_status(new_status)
        
        bot.answer_callback_query(call.id, f"✅ Force Join {'Enabled' if new_status else 'Disabled'}")
        
        # Refresh settings message
        handle_bot_settings_text(call.message)
        
    except Exception as e:
        logger.error(f"Error toggling force join: {e}")
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)

def handle_toggle_bot_lock(call):
    """Handle toggle bot lock"""
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Owner Only", show_alert=True)
        return
    
    try:
        global bot_locked
        bot_locked = not bot_locked
        
        bot.answer_callback_query(call.id, f"✅ Bot {'Locked' if bot_locked else 'Unlocked'}")
        
        # Refresh settings message
        handle_bot_settings_text(call.message)
        
    except Exception as e:
        logger.error(f"Error toggling bot lock: {e}")
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)

def handle_change_file_limit(call):
    """Handle change file limit"""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ Admin Only", show_alert=True)
        return
    
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    
    msg = bot.send_message(call.message.chat.id, "📊 Enter new file limit for free users (1-100):")
    bot.register_next_step_handler(msg, process_file_limit_change)

def process_file_limit_change(message):
    """Process file limit change"""
    try:
        new_limit = int(message.text.strip())
        if 1 <= new_limit <= 100:
            update_file_limit(new_limit)
            bot.send_message(message.chat.id, f"✅ File limit updated to {new_limit}")
        else:
            bot.send_message(message.chat.id, "❌ Limit must be between 1 and 100")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Invalid number")

def handle_security_stats(call):
    """Handle security stats"""
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Owner Only", show_alert=True)
        return
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM security_logs')
        total_logs = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM security_logs WHERE risk_level = 'critical'")
        critical_logs = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM security_logs WHERE risk_level = 'high'")
        high_logs = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT user_id) FROM security_logs")
        affected_users = c.fetchone()[0]
        
        c.execute("SELECT risk_level, COUNT(*) FROM security_logs GROUP BY risk_level")
        risk_counts = c.fetchall()
        
        conn.close()
        
        stats_text = f"""
🛡️ **SECURITY STATISTICS**

━━━━━━━━━━━━━━━━━━━━━
📊 **SCANNING OVERVIEW**
━━━━━━━━━━━━━━━━━━━━━
├─ Total Scans: {security_scans['total_scans']}
├─ Threats Found: {security_scans['threats_found']}
├─ High Risk Files: {security_scans['high_risk_files']}
└─ Blocked Files: {security_scans['blocked_files']}

━━━━━━━━━━━━━━━━━━━━━
📈 **LOGGED EVENTS**
━━━━━━━━━━━━━━━━━━━━━
├─ Total Logs: {total_logs}
├─ Critical Events: {critical_logs}
├─ High Risk Events: {high_logs}
└─ Affected Users: {affected_users}

━━━━━━━━━━━━━━━━━━━━━
📋 **RISK BREAKDOWN**
━━━━━━━━━━━━━━━━━━━━━
"""
        
        for risk, count in risk_counts:
            stats_text += f"├─ {risk.upper()}: {count}\n"
        
        stats_text += """
━━━━━━━━━━━━━━━━━━━━━
⚡ **SYSTEM STATUS**
━━━━━━━━━━━━━━━━━━━━━
├─ Security Scanner: 🟢 ACTIVE
├─ Real-time Monitoring: 🟢 ENABLED
└─ Owner Alerts: 🟢 ENABLED
        """
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📋 View Logs", callback_data='view_security_logs'))
        markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data='back_to_admin_settings'))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=stats_text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error getting security stats: {e}")
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)

def handle_broadcast_settings(call):
    """Handle broadcast settings"""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ Admin Only", show_alert=True)
        return
    
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    
    msg = bot.send_message(call.message.chat.id, "📢 Enter message to broadcast to all users:")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    """Process broadcast"""
    try:
        broadcast_text = message.text
        success_count = 0
        fail_count = 0
        
        status_msg = bot.send_message(message.chat.id, "📢 Broadcasting... 0%")
        
        total_users = len(active_users)
        for i, user_id in enumerate(active_users):
            try:
                bot.send_message(user_id, broadcast_text)
                success_count += 1
            except:
                fail_count += 1
            
            if i % 10 == 0:
                try:
                    progress = int((i + 1) / total_users * 100)
                    bot.edit_message_text(f"📢 Broadcasting... {progress}%", 
                                        status_msg.chat.id, status_msg.message_id)
                except:
                    pass
        
        bot.edit_message_text(
            f"📢 **Broadcast Complete**\n\n✅ Success: {success_count}\n❌ Failed: {fail_count}",
            status_msg.chat.id,
            status_msg.message_id,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

def handle_system_info(call):
    """Handle system info"""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ Admin Only", show_alert=True)
        return
    
    try:
        stats = get_bot_statistics()
        
        info_text = f"""
ℹ️ **SYSTEM INFORMATION**

━━━━━━━━━━━━━━━━━━━━━
💻 **HARDWARE**
━━━━━━━━━━━━━━━━━━━━━
├─ CPU: {stats['cpu_percent']}% ({psutil.cpu_count()} cores)
├─ Memory: {stats['memory_percent']}% ({stats['memory_used']}/{stats['memory_total']})
├─ Disk: {stats['disk_percent']}% ({stats['disk_used']}/{stats['disk_total']})
└─ Uptime: {stats['uptime']}

━━━━━━━━━━━━━━━━━━━━━
📊 **BOT STATS**
━━━━━━━━━━━━━━━━━━━━━
├─ Users: {stats['total_users']}
├─ Premium: {stats['premium_users']}
├─ Files: {stats['total_files']}
├─ Active: {stats['active_files']}
├─ API Keys: {stats['total_api_keys']}
└─ Webhooks: {stats['total_webhooks']}

━━━━━━━━━━━━━━━━━━━━━
⚙️ **SETTINGS**
━━━━━━━━━━━━━━━━━━━━━
├─ Force Join: {'✅' if force_join_enabled else '❌'}
├─ Bot Lock: {'🔒' if bot_locked else '🔓'}
├─ Free Limit: {FREE_USER_LIMIT}
├─ Rate Limit: {RATE_LIMIT}/{RATE_WINDOW}s
└─ Max File Size: {format_file_size(MAX_FILE_SIZE)}

━━━━━━━━━━━━━━━━━━━━━
🛡️ **SECURITY**
━━━━━━━━━━━━━━━━━━━━━
├─ Scans: {security_scans['total_scans']}
├─ Threats: {security_scans['threats_found']}
├─ Blocked: {security_scans['blocked_files']}
└─ Banned: {stats['banned_users']}

━━━━━━━━━━━━━━━━━━━━━
🔌 **INTEGRATIONS**
━━━━━━━━━━━━━━━━━━━━━
├─ Redis: {'✅' if redis_client else '❌'}
├─ MongoDB: {'✅' if mongodb_client else '❌'}
├─ Docker: {'✅' if docker_client else '❌'}
└─ Email: {'✅' if os.environ.get('SMTP_USERNAME') else '❌'}
        """
        
        bot.send_message(call.message.chat.id, info_text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        bot.answer_callback_query(call.id, "❌ Error", show_alert=True)

def handle_view_security_logs(call):
    """Handle view security logs"""
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Owner Only", show_alert=True)
        return
    
    handle_security_logs_text(call.message)

def handle_back_to_admin_settings(call):
    """Handle back to admin settings"""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ Admin Only", show_alert=True)
        return
    
    handle_bot_settings_text(call.message)

def handle_back_to_admin(call):
    """Handle back to admin"""
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, "❌ Admin Only", show_alert=True)
        return
    
    handle_admin_panel_text(call.message)

# --- Utility Functions ---
def check_force_join(user_id):
    """Check if user has joined required channels"""
    if user_id in admin_ids:
        return True
    
    if not force_join_enabled:
        return True
    
    if is_user_banned(user_id):
        return False
    
    try:
        group_member = bot.get_chat_member(FORCE_GROUP_ID, user_id)
        if group_member.status not in ['member', 'administrator', 'creator']:
            return False
        
        return True
    except Exception as e:
        logger.error(f"❌ Error checking membership for user {user_id}: {e}")
        return False

def is_user_banned(user_id):
    """Check if user is banned"""
    if user_id in admin_ids or user_id == OWNER_ID:
        return False
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT user_id FROM banned_users WHERE user_id = ?', (user_id,))
        return c.fetchone() is not None
    finally:
        conn.close()

def create_start_hosting_keyboard():
    """Create start hosting keyboard"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🚀 Deploy Now', callback_data='start_hosting'))
    return markup

# --- Cleanup Functions ---
def cleanup():
    """Cleanup on shutdown"""
    logger.warning("🛑 Shutting down...")
    
    # Stop all running processes
    for script_key in list(bot_scripts.keys()):
        if script_key in bot_scripts:
            force_cleanup_process(bot_scripts[script_key])
    
    # Close database connections
    # (handled by context managers)
    
    # Clean up temporary files
    try:
        for file in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except:
        pass
    
    logger.info("✅ Cleanup completed")

def schedule_cleanup():
    """Schedule regular cleanup"""
    while True:
        try:
            cleanup_zombie_processes()
            
            # Clean up old log files (older than 7 days)
            now = time.time()
            for file in os.listdir(LOGS_DIR):
                file_path = os.path.join(LOGS_DIR, file)
                if os.path.isfile(file_path) and os.path.getmtime(file_path) < now - 7 * 86400:
                    try:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old log: {file}")
                    except:
                        pass
            
            # Clean up old temp files
            for file in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, file)
                if os.path.isfile(file_path) and os.path.getmtime(file_path) < now - 86400:
                    try:
                        os.remove(file_path)
                    except:
                        pass
            
            # Clean up expired sessions
            for user_id in list(user_subscriptions.keys()):
                if user_subscriptions[user_id]['expiry'] < datetime.now():
                    del user_subscriptions[user_id]
            
            time.sleep(300)  # Run every 5 minutes
            
        except Exception as e:
            logger.error(f"Error in schedule_cleanup: {e}")
            time.sleep(60)

def monitor_system():
    """Monitor system resources"""
    while True:
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            if cpu_percent > 90:
                logger.warning(f"⚠️ High CPU usage: {cpu_percent}%")
                try:
                    bot.send_message(OWNER_ID, f"⚠️ **High CPU Usage Alert**\nCPU: {cpu_percent}%")
                except:
                    pass
            
            if memory.percent > 90:
                logger.warning(f"⚠️ High memory usage: {memory.percent}%")
                try:
                    bot.send_message(OWNER_ID, f"⚠️ **High Memory Usage Alert**\nMemory: {memory.percent}%")
                except:
                    pass
            
            if disk.percent > 90:
                logger.warning(f"⚠️ High disk usage: {disk.percent}%")
                try:
                    bot.send_message(OWNER_ID, f"⚠️ **High Disk Usage Alert**\nDisk: {disk.percent}%")
                except:
                    pass
            
            time.sleep(60)
        except Exception as e:
            logger.error(f"Error in system monitoring: {e}")
            time.sleep(60)

def schedule_backup():
    """Schedule automatic backups"""
    while True:
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            c.execute('SELECT setting_value FROM bot_settings WHERE setting_key = "backup_enabled"')
            result = c.fetchone()
            backup_enabled = result and result[0] == '1'
            
            if backup_enabled:
                c.execute('SELECT setting_value FROM bot_settings WHERE setting_key = "backup_interval"')
                result = c.fetchone()
                backup_interval = int(result[0]) if result else 24
                
                backup_file = create_backup()
                logger.info(f"✅ Automatic backup created: {backup_file}")
                
                # Clean up old backups (keep last 10)
                backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('full_backup_')])
                while len(backups) > 10:
                    old_backup = os.path.join(BACKUP_DIR, backups[0])
                    os.remove(old_backup)
                    backups.pop(0)
            
            conn.close()
            time.sleep(3600 * backup_interval)
        except Exception as e:
            logger.error(f"Error in scheduled backup: {e}")
            time.sleep(3600)

# --- Main ---
if __name__ == '__main__':
    # Register cleanup handler
    atexit.register(cleanup)
    
    # Start background threads
    cleanup_thread = threading.Thread(target=schedule_cleanup, daemon=True)
    cleanup_thread.start()
    
    monitor_thread = threading.Thread(target=monitor_system, daemon=True)
    monitor_thread.start()
    
    backup_thread = threading.Thread(target=schedule_backup, daemon=True)
    backup_thread.start()
    
    # Start Flask keep-alive
    keep_alive()
    
    logger.info("🚀 KELVIN Cloud Bot v3.0 starting...")
    logger.info(f"📊 Initial stats: {len(active_users)} users, {len(user_subscriptions)} subscriptions")
    
    # Start bot
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logger.error(f"❌ Bot polling error: {e}")
        time.sleep(5)
        # Restart bot
        bot.polling(none_stop=True, interval=0, timeout=20)