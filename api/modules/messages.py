"""留言板 API 蓝图"""
from datetime import datetime

from flask import Blueprint, request, jsonify

from db import get_db, query, cached, serialize_dates
from config import SITES, CACHE_TTL
from auth import require_admin, verify_token

bp = Blueprint('messages', __name__, url_prefix='/api')


@bp.route('/message', methods=['POST'])
def submit_message():
    """提交留言"""
    data = request.get_json() or {}
    site = data.get('site', 'jy')
    name = data.get('name', '匿名')
    email = data.get('email', '')
    content = data.get('content', '')

    if not content:
        return jsonify({"error": "内容不能为空"}), 400
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    db = get_db(site)
    cur = db.cursor()
    cur.execute(
        "INSERT INTO messages (site, name, email, content) VALUES (%s,%s,%s,%s)",
        (site, name, email, content)
    )
    db.commit()
    return jsonify({"success": True, "message": "留言成功！"})


@bp.route('/messages/<site>')
def get_messages(site):
    """获取留言列表"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    auth = request.headers.get('Authorization', '')
    is_admin = bool(auth.startswith('Bearer ') and verify_token(auth[7:]))

    if is_admin:
        msgs = query(
            "SELECT * FROM messages WHERE site=%s ORDER BY created_at DESC",
            (site,), site=site
        )
    else:
        msgs = _get_messages_cached(site)

    return jsonify(serialize_dates(msgs) if msgs else [])


@cached(ttl_seconds=CACHE_TTL['messages'])
def _get_messages_cached(site):
    """公开留言缓存（只显示已审核的）"""
    return query(
        """SELECT id, site, name, content, created_at
           FROM messages WHERE site=%s AND is_read=1
           ORDER BY created_at DESC""",
        (site,), site=site
    )
