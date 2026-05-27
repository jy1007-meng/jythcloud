"""JYTHCloud API 配置"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

# 安全配置（生产环境请用环境变量覆盖）
SECRET_KEY = os.environ.get('JYTH_SECRET', '***')
ADMIN_USERNAME = os.environ.get('JYTH_ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.environ.get('JYTH_ADMIN_PASS', '***')

# MySQL 配置
MYSQL_CONFIG = {
    'host': os.environ.get('JYTH_DB_HOST', '127.0.0.1'),
    'port': int(os.environ.get('JYTH_DB_PORT', '3306')),
    'user': os.environ.get('JYTH_DB_USER', 'jythcloud'),
    'password': os.environ.get('JYTH_DB_PASS', 'W5tCMxXDTpPk'),
    'charset': 'utf8mb4',
}

# 站点配置
SITES = {
    'jy': {'db': 'jy_site', 'name': '吉天宇', 'color': '#6366f1'},
    'tan': {'db': 'tan_site', 'name': '谭海涛', 'color': '#10b981'},
    'hu': {'db': 'hu_site', 'name': '胡子雄', 'color': '#ec4899'},
}

# 缓存配置
CACHE_TTL = {
    'stats': 15,
    'articles': 15,
    'messages': 10,
    'status': 10,
    'dashboard': 30,
}
