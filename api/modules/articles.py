"""文章系统 API 蓝图"""
from datetime import datetime

from flask import Blueprint, request, jsonify

from db import get_db, query, cached, serialize_dates
from config import SITES, CACHE_TTL
from auth import require_admin

bp = Blueprint('articles', __name__, url_prefix='/api')


@bp.route('/articles/<site>')
@cached(ttl_seconds=CACHE_TTL['articles'])
def list_articles(site):
    """公开文章列表"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    total = query(
        "SELECT COUNT(*) as cnt FROM articles WHERE site=%s AND status=1",
        (site,), one=True, site=site
    )
    articles = query(
        """SELECT id, site, title, summary, cover_url, tags,
                  author, view_count, created_at, published_at
           FROM articles WHERE site=%s AND status=1
           ORDER BY published_at DESC LIMIT %s OFFSET %s""",
        (site, per_page, offset), site=site
    )

    return jsonify({
        "articles": serialize_dates(articles) if articles else [],
        "total": total['cnt'] if total else 0,
        "page": page,
        "per_page": per_page
    })


@bp.route('/article/<site>/<int:article_id>')
def get_article(site, article_id):
    """获取单篇文章（自动增加阅读数）"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    article = query(
        "SELECT * FROM articles WHERE site=%s AND id=%s",
        (site, article_id), one=True, site=site
    )
    if not article:
        return jsonify({"error": "文章不存在"}), 404

    # 增加阅读数
    db = get_db(site)
    cur = db.cursor()
    cur.execute("UPDATE articles SET view_count = view_count + 1 WHERE id=%s", (article_id,))
    db.commit()

    return jsonify(serialize_dates(article))


# ═══ 管理接口 ═══

@bp.route('/admin/article', methods=['POST'])
@require_admin
def create_article(username):
    """创建文章"""
    data = request.get_json() or {}
    site = data.get('site', 'jy')
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    db = get_db(site)
    cur = db.cursor()
    cur.execute(
        """INSERT INTO articles (site, title, content, summary, cover_url, tags, author, status, published_at)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())""",
        (
            site,
            data.get('title', '无标题'),
            data.get('content', ''),
            data.get('summary', ''),
            data.get('cover_url', ''),
            data.get('tags', ''),
            data.get('author', username),
            data.get('status', 1),
        )
    )
    db.commit()
    return jsonify({"success": True, "id": cur.lastrowid}), 201


@bp.route('/admin/article/<int:article_id>', methods=['PUT', 'DELETE'])
@require_admin
def manage_article(article_id, username):
    """更新/删除文章"""
    if request.method == 'DELETE':
        site = request.args.get('site', 'jy')
        if site not in SITES:
            return jsonify({"error": "无效站点"}), 400
        db = get_db(site)
        cur = db.cursor()
        cur.execute("DELETE FROM articles WHERE id=%s", (article_id,))
        db.commit()
        return jsonify({"success": True})

    # PUT: 更新
    data = request.get_json() or {}
    site = data.get('site', 'jy')
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    allowed = ['title', 'content', 'summary', 'cover_url', 'tags', 'status']
    updates = {k: v for k, v in data.items() if k in allowed}
    if not updates:
        return jsonify({"error": "没有可更新的字段"}), 400

    db = get_db(site)
    cur = db.cursor()
    set_clause = ", ".join(f"{k}=%s" for k in updates)
    values = list(updates.values()) + [article_id]
    cur.execute(f"UPDATE articles SET {set_clause}, updated_at=NOW() WHERE id=%s", values)
    db.commit()
    return jsonify({"success": True})
