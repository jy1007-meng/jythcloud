"""JWT 认证工具"""
import json, time, hashlib, hmac, base64
from functools import wraps

from flask import request, jsonify
from werkzeug.security import check_password_hash

from config import SECRET_KEY
from db import query


def create_token(username):
    """生成JWT token（7天有效期）"""
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    ).rstrip(b'=').decode()

    payload_data = {"username": username, "exp": int(time.time()) + 86400 * 7}
    payload = base64.urlsafe_b64encode(
        json.dumps(payload_data).encode()
    ).rstrip(b'=').decode()

    signature = hmac.new(
        SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256
    ).digest()
    sig = base64.urlsafe_b64encode(signature).rstrip(b'=').decode()

    return f"{header}.{payload}.{sig}"


def verify_token(token):
    """验证JWT token"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header, payload, sig = parts
        expected = base64.urlsafe_b64encode(
            hmac.new(
                SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256
            ).digest()
        ).rstrip(b'=').decode()
        if sig != expected:
            return None
        data = json.loads(base64.urlsafe_b64decode(payload + '=='))
        if data.get('exp', 0) < time.time():
            return None
        return data.get('username')
    except Exception:
        return None


def require_admin(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({"error": "未登录"}), 401
        username = verify_token(auth[7:])
        if not username:
            return jsonify({"error": "登录已过期"}), 401
        return f(*args, username=username, **kwargs)
    return decorated


def login_user(username, password):
    """验证用户登录（遍历三个数据库）"""
    from config import SITES
    for site_key in SITES:
        user = query(
            "SELECT * FROM users WHERE username=%s",
            (username,), one=True, site=site_key
        )
        if user and check_password_hash(user['password_hash'], password):
            return create_token(username)
    return None
