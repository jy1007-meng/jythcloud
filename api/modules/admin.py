"""管理后台 API 蓝图"""
from datetime import datetime

from flask import Blueprint, request, jsonify

from db import get_db, query, serialize_dates
from config import SITES
from auth import require_admin, login_user, verify_token

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


# ═══ 认证 ═══

@bp.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json() or {}
    token = login_user(data.get('username', ''), data.get('password', ''))
    if token:
        return jsonify({"token": token, "username": data.get('username'), "role": "admin"})
    return jsonify({"error": "用户名或密码错误"}), 401


@bp.route('/auth/verify', methods=['POST'])
def verify():
    """验证 token 是否有效"""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({"valid": False}), 401
    username = verify_token(auth[7:])
    return jsonify({"valid": bool(username), "username": username})


# ═══ 仪表盘 ═══

@bp.route('/dashboard/<site>')
@require_admin
def dashboard(site, username):
    """站点仪表盘数据"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    total_v = query(
        "SELECT visitor_count FROM site_config WHERE site=%s", (site,), one=True, site=site
    )
    total_m = query(
        "SELECT COUNT(*) as cnt FROM messages WHERE site=%s", (site,), one=True, site=site
    )
    unread_m = query(
        "SELECT COUNT(*) as cnt FROM messages WHERE site=%s AND is_read=0", (site,), one=True, site=site
    )
    total_a = query(
        "SELECT COUNT(*) as cnt FROM articles WHERE site=%s", (site,), one=True, site=site
    )
    pub_a = query(
        "SELECT COUNT(*) as cnt FROM articles WHERE site=%s AND status=1", (site,), one=True, site=site
    )
    today = datetime.now().strftime('%Y-%m-%d')
    today_s = query(
        "SELECT pv, uv FROM daily_stats WHERE site=%s AND date=%s",
        (site, today), one=True, site=site
    )
    trend = query(
        """SELECT date, pv, uv FROM daily_stats
           WHERE site=%s ORDER BY date DESC LIMIT 7""",
        (site,), site=site
    )
    recent = query(
        """SELECT name, content, created_at FROM messages
           WHERE site=%s ORDER BY created_at DESC LIMIT 5""",
        (site,), site=site
    )

    if trend:
        trend = list(reversed(trend))

    return jsonify({
        "visitors": {"total": total_v['visitor_count'] if total_v else 0},
        "messages": {
            "total": total_m['cnt'] if total_m else 0,
            "unread": unread_m['cnt'] if unread_m else 0
        },
        "articles": {
            "total": total_a['cnt'] if total_a else 0,
            "published": pub_a['cnt'] if pub_a else 0
        },
        "today": {
            "pv": today_s['pv'] if today_s else 0,
            "uv": today_s['uv'] if today_s else 0
        },
        "trend": serialize_dates(trend) if trend else [],
        "recent_messages": serialize_dates(recent) if recent else []
    })


# ═══ 文章管理 ═══

@bp.route('/articles/<site>')
@require_admin
def admin_articles(site, username):
    """后台文章列表"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    total = query(
        "SELECT COUNT(*) as cnt FROM articles WHERE site=%s", (site,), one=True, site=site
    )
    articles = query(
        "SELECT * FROM articles WHERE site=%s ORDER BY created_at DESC LIMIT %s OFFSET %s",
        (site, per_page, offset), site=site
    )
    return jsonify({
        "articles": serialize_dates(articles) if articles else [],
        "total": total['cnt'] if total else 0
    })


# ═══ 留言管理 ═══

@bp.route('/messages/<site>')
@require_admin
def admin_messages(site, username):
    """后台留言列表"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400
    msgs = query(
        "SELECT * FROM messages WHERE site=%s ORDER BY created_at DESC",
        (site,), site=site
    )
    return jsonify(serialize_dates(msgs) if msgs else [])


@bp.route('/message/<int:msg_id>/read', methods=['POST'])
@require_admin
def mark_read(msg_id, username):
    """标记留言为已读"""
    data = request.get_json() or {}
    site = data.get('site', 'jy')
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400
    db = get_db(site)
    cur = db.cursor()
    cur.execute("UPDATE messages SET is_read=1 WHERE id=%s", (msg_id,))
    db.commit()
    return jsonify({"success": True})


@bp.route('/message/<int:msg_id>/reply', methods=['POST'])
@require_admin
def reply_message(msg_id, username):
    """回复留言"""
    data = request.get_json() or {}
    site = data.get('site', 'jy')
    reply = data.get('reply', '')
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400
    db = get_db(site)
    cur = db.cursor()
    cur.execute(
        "UPDATE messages SET reply_content=%s, replied_at=NOW(), is_read=1 WHERE id=%s",
        (reply, msg_id)
    )
    db.commit()
    return jsonify({"success": True})


@bp.route('/message/<int:msg_id>', methods=['DELETE'])
@require_admin
def delete_message(msg_id, username):
    """删除留言"""
    site = request.args.get('site', 'jy')
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400
    db = get_db(site)
    cur = db.cursor()
    cur.execute("DELETE FROM messages WHERE id=%s", (msg_id,))
    db.commit()
    return jsonify({"success": True})


# ═══ 站点配置 ═══

@bp.route('/site-config/<site>', methods=['GET', 'PUT'])
@require_admin
def site_config(site, username):
    """获取/更新站点配置"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    if request.method == 'PUT':
        data = request.get_json() or {}
        allowed = ['site_name', 'site_subtitle', 'avatar_text', 'theme_color', 'about_text']
        updates = {k: v for k, v in data.items() if k in allowed}
        if updates:
            db = get_db(site)
            cur = db.cursor()
            set_clause = ", ".join(f"{k}=%s" for k in updates)
            values = list(updates.values()) + [site]
            cur.execute(f"UPDATE site_config SET {set_clause}, updated_at=NOW() WHERE site=%s", values)
            db.commit()
        return jsonify({"success": True})

    cfg = query(
        "SELECT * FROM site_config WHERE site=%s", (site,), one=True, site=site
    )
    return jsonify(serialize_dates(cfg) if cfg else {})


# ═══ 用户管理 ═══

@bp.route('/users')
@require_admin
def admin_users(username):
    """获取用户列表"""
    users = query("SELECT id, username, role, site, created_at FROM users", site='jy')
    return jsonify(serialize_dates(users) if users else [])


@bp.route('/user', methods=['POST'])
@require_admin
def create_user(username):
    """创建用户"""
    data = request.get_json() or {}
    u = data.get('username', '')
    p = data.get('password', '')
    if not u or not p:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    from werkzeug.security import generate_password_hash
    for site_key in SITES:
        db = get_db(site_key)
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (u, generate_password_hash(p), data.get('role', 'admin'))
            )
            db.commit()
        except Exception as e:
            if 'Duplicate' in str(e):
                return jsonify({"error": "用户名已存在"}), 400
    return jsonify({"success": True}), 201


@bp.route('/user/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id, username):
    """删除用户"""
    for site_key in SITES:
        db = get_db(site_key)
        cur = db.cursor()
        cur.execute("DELETE FROM users WHERE id=%s AND username!='admin'", (user_id,))
        db.commit()
    return jsonify({"success": True})


@bp.route('/change-password', methods=['POST'])
@require_admin
def change_password(username):
    """修改密码"""
    data = request.get_json() or {}
    old_pw = data.get('old_password', '')
    new_pw = data.get('new_password', '')
    if not old_pw or not new_pw:
        return jsonify({"error": "请提供旧密码和新密码"}), 400

    from werkzeug.security import check_password_hash, generate_password_hash
    user = query(
        "SELECT * FROM users WHERE username=%s", (username,), one=True, site='jy'
    )
    if not user or not check_password_hash(user['password_hash'], old_pw):
        return jsonify({"error": "旧密码错误"}), 401

    new_hash = generate_password_hash(new_pw)
    for site_key in SITES:
        db = get_db(site_key)
        cur = db.cursor()
        cur.execute("UPDATE users SET password_hash=%s WHERE username=%s", (new_hash, username))
        db.commit()
    return jsonify({"success": True})


@bp.route('/clear-visits/<site>', methods=['DELETE'])
@require_admin
def clear_visits(site, username):
    """清除访问记录"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400
    db = get_db(site)
    cur = db.cursor()
    cur.execute("DELETE FROM page_views WHERE site=%s", (site,))
    cur.execute("DELETE FROM daily_stats WHERE site=%s", (site,))
    cur.execute("UPDATE site_config SET visitor_count=0 WHERE site=%s", (site,))
    db.commit()
    return jsonify({"success": True})
