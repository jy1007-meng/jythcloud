"""数据库连接和工具函数"""
import time, threading
from datetime import datetime
from functools import wraps

import pymysql
from pymysql.cursors import DictCursor
from flask import g, jsonify
from werkzeug.security import generate_password_hash

from config import MYSQL_CONFIG, SITES, CACHE_TTL

# ═══ 内存缓存 ═══
_cache = {}
_cache_lock = threading.Lock()

def cached(ttl_seconds=30):
    """TTL 缓存装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = f"{f.__name__}:{args}:{kwargs}"
            now = time.time()
            with _cache_lock:
                if key in _cache:
                    data, expiry = _cache[key]
                    if now < expiry:
                        return data
            result = f(*args, **kwargs)
            with _cache_lock:
                _cache[key] = (result, now + ttl_seconds)
            return result
        return wrapper
    return decorator

def _cache_cleaner():
    while True:
        time.sleep(300)
        now = time.time()
        with _cache_lock:
            expired = [k for k, (_, t) in _cache.items() if now >= t]
            for k in expired:
                del _cache[k]

_cleaner_thread = threading.Thread(target=_cache_cleaner, daemon=True)
_cleaner_thread.start()

def clear_cache():
    """手动清除缓存"""
    with _cache_lock:
        _cache.clear()


# ═══ 数据库连接 ═══
def get_db(site='jy'):
    """获取站点数据库连接（带连接池）"""
    db_name = SITES.get(site, SITES['jy'])['db']
    key = f'db_{db_name}'
    if not hasattr(g, '_dbs'):
        g._dbs = {}
    if key not in g._dbs:
        conn = pymysql.connect(
            database=db_name,
            cursorclass=DictCursor,
            autocommit=False,
            **MYSQL_CONFIG
        )
        g._dbs[key] = conn
    return g._dbs[key]

def close_db(e=None):
    """关闭所有数据库连接"""
    dbs = getattr(g, '_dbs', {})
    for key, conn in dbs.items():
        try:
            conn.close()
        except:
            pass
    g._dbs = {}

def query(sql, args=(), one=False, site='jy'):
    """便捷查询"""
    db = get_db(site)
    cur = db.cursor()
    cur.execute(sql, args)
    rows = cur.fetchall()
    db.commit()
    return rows[0] if one and rows else rows


# ═══ 日期序列化 ═══
def serialize_dates(obj):
    """递归处理 datetime 字段"""
    if isinstance(obj, list):
        for item in obj:
            serialize_dates(item)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(v, str) and hasattr(v, 'strftime'):
                obj[k] = v.strftime('%Y-%m-%d %H:%M:%S')
    return obj


# ═══ 数据库初始化 ═══
def init_db():
    """初始化所有站点的数据库表"""
    for site_key, info in SITES.items():
        conn = pymysql.connect(
            database=info['db'],
            cursorclass=DictCursor,
            **MYSQL_CONFIG
        )
        cur = conn.cursor()

        # 页面访问
        cur.execute("""
            CREATE TABLE IF NOT EXISTS page_views (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site VARCHAR(20) NOT NULL,
                page VARCHAR(255) DEFAULT '/',
                user_agent TEXT,
                ip VARCHAR(64) DEFAULT '',
                referer TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_pv_site (site),
                INDEX idx_pv_created (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 留言
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site VARCHAR(20) NOT NULL,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(200) DEFAULT '',
                content TEXT NOT NULL,
                is_read TINYINT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                replied_at DATETIME NULL,
                reply_content TEXT,
                INDEX idx_msg_site (site)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 文章
        cur.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site VARCHAR(20) NOT NULL,
                title VARCHAR(255) NOT NULL,
                content LONGTEXT NOT NULL,
                summary TEXT,
                cover_url VARCHAR(500) DEFAULT '',
                tags VARCHAR(255) DEFAULT '',
                author VARCHAR(100) DEFAULT 'admin',
                status TINYINT DEFAULT 1,
                view_count INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                published_at DATETIME NULL,
                INDEX idx_art_site (site)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 用户
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'admin',
                site VARCHAR(20) DEFAULT 'all',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 站点配置
        cur.execute("""
            CREATE TABLE IF NOT EXISTS site_config (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site VARCHAR(20) UNIQUE NOT NULL,
                site_name VARCHAR(100) DEFAULT '',
                site_subtitle VARCHAR(200) DEFAULT '',
                avatar_text VARCHAR(20) DEFAULT '',
                theme_color VARCHAR(20) DEFAULT '#6366f1',
                about_text TEXT,
                visitor_count INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 每日统计
        cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                site VARCHAR(20) NOT NULL,
                date DATE NOT NULL,
                pv INT DEFAULT 0,
                uv INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY uk_site_date (site, date),
                INDEX idx_ds_site_date (site, date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 默认管理员
        from config import ADMIN_USERNAME, ADMIN_PASSWORD
        cur.execute("SELECT id FROM users WHERE username=%s", (ADMIN_USERNAME,))
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'admin')",
                (ADMIN_USERNAME, generate_password_hash(ADMIN_PASSWORD))
            )

        # 默认站点配置
        sites_data = [
            ('jy', '吉天宇', '全栈工程师', 'JT', '#6366f1',
             '热爱技术，专注全栈开发。拥有丰富的Web应用开发经验，擅长前后端分离架构和云原生部署。'),
            ('tan', '谭海涛', '数据科学家', 'TH', '#10b981',
             '数据驱动的决策者，精通机器学习与数据分析。善于从海量数据中提取洞察，用数据讲故事。'),
            ('hu', '胡子雄', '产品设计师', 'HZ', '#ec4899',
             '用户体验至上，用设计思维创造有温度的产品。擅长交互设计、视觉设计和设计系统构建。'),
        ]
        for sid, name, subtitle, avatar, color, about in sites_data:
            if sid == site_key:
                cur.execute("SELECT id FROM site_config WHERE site=%s", (sid,))
                if not cur.fetchone():
                    cur.execute(
                        "INSERT INTO site_config (site, site_name, site_subtitle, avatar_text, theme_color, about_text) VALUES (%s,%s,%s,%s,%s,%s)",
                        (sid, name, subtitle, avatar, color, about)
                    )

        conn.commit()
        conn.close()
        print(f"  ✓ {info['name']} ({site_key}) 初始化完成")
