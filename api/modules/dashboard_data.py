"""数据大屏 API 蓝图"""
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify

from db import get_db, query, cached, serialize_dates
from config import SITES, CACHE_TTL

bp = Blueprint('dashboard', __name__, url_prefix='/api')


@bp.route('/dashboard/<site>')
def data_dashboard(site):
    """数据大屏接口"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    five_min_ago = (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')

    # 在线人数
    online = query(
        """SELECT COUNT(DISTINCT ip) as cnt FROM page_views
           WHERE site=%s AND ip!='' AND ip!='auto' AND created_at>=%s""",
        (site, five_min_ago), one=True, site=site
    )

    # 30天趋势
    pv_trend = query(
        """SELECT date, pv, uv FROM daily_stats
           WHERE site=%s AND date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
           ORDER BY date""",
        (site,), site=site
    )

    # 热门页面
    top_pages = query(
        """SELECT page, COUNT(*) as cnt FROM page_views
           WHERE site=%s GROUP BY page ORDER BY cnt DESC LIMIT 10""",
        (site,), site=site
    )

    # 城市分布（基于IP哈希模拟）
    cities = [
        {"city": "北京", "count": 0},
        {"city": "上海", "count": 0},
        {"city": "广州", "count": 0},
        {"city": "深圳", "count": 0},
        {"city": "杭州", "count": 0},
        {"city": "成都", "count": 0},
        {"city": "南京", "count": 0},
        {"city": "武汉", "count": 0},
        {"city": "西安", "count": 0},
        {"city": "其他", "count": 0},
    ]
    ips = query(
        "SELECT DISTINCT ip FROM page_views WHERE site=%s AND ip!='' AND ip!='auto' LIMIT 100",
        (site,), site=site
    )
    for row in ips:
        idx = abs(hash(row['ip'])) % len(cities)
        cities[idx]['count'] += 1

    # 热门文章
    art_stats = query(
        """SELECT title, view_count, created_at FROM articles
           WHERE site=%s AND status=1 ORDER BY view_count DESC LIMIT 10""",
        (site,), site=site
    )

    # 留言趋势
    msg_trend = query(
        """SELECT DATE(created_at) as date, COUNT(*) as cnt FROM messages
           WHERE site=%s AND created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
           GROUP BY DATE(created_at) ORDER BY date""",
        (site,), site=site
    )

    # 站点配置
    config = query(
        "SELECT * FROM site_config WHERE site=%s", (site,), one=True, site=site
    )

    return jsonify({
        "online": online['cnt'] if online else 0,
        "pv_trend": serialize_dates(pv_trend) if pv_trend else [],
        "top_pages": top_pages or [],
        "cities": cities,
        "articles": serialize_dates(art_stats) if art_stats else [],
        "msg_trend": serialize_dates(msg_trend) if msg_trend else [],
        "config": serialize_dates(config) if config else {}
    })
