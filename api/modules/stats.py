"""访问统计 API 蓝图"""
from datetime import datetime

from flask import Blueprint, request, jsonify

from db import get_db, query, cached, serialize_dates
from config import SITES, CACHE_TTL

bp = Blueprint('stats', __name__, url_prefix='/api')


@bp.route('/visit', methods=['POST'])
def record_visit():
    """记录页面访问"""
    data = request.get_json() or {}
    site = data.get('site', 'jy')
    page = data.get('page', '/')
    ua = data.get('user_agent', request.headers.get('User-Agent', ''))
    ip = data.get('ip', request.remote_addr or '')
    referer = data.get('referer', request.headers.get('Referer', ''))

    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    db = get_db(site)
    cur = db.cursor()

    # 记录访问
    cur.execute(
        "INSERT INTO page_views (site, page, user_agent, ip, referer) VALUES (%s,%s,%s,%s,%s)",
        (site, page, ua, ip, referer)
    )

    # 更新访问总数
    cur.execute(
        "UPDATE site_config SET visitor_count = visitor_count + 1, updated_at = NOW() WHERE site=%s",
        (site,)
    )

    # 更新每日统计
    today = datetime.now().strftime('%Y-%m-%d')
    uv_inc = 1 if ip and ip != 'auto' else 0
    cur.execute(
        """INSERT INTO daily_stats (site, date, pv, uv)
           VALUES (%s,%s,1,%s)
           ON DUPLICATE KEY UPDATE pv = pv + 1, uv = GREATEST(uv, %s)""",
        (site, today, uv_inc, uv_inc if uv_inc else 1)
    )

    db.commit()
    return jsonify({"success": True})


@bp.route('/stats/<site>')
@cached(ttl_seconds=CACHE_TTL['stats'])
def get_stats(site):
    """获取站点统计数据"""
    if site not in SITES:
        return jsonify({"error": "无效站点"}), 400

    total = query(
        "SELECT visitor_count FROM site_config WHERE site=%s",
        (site,), one=True, site=site
    )
    today = datetime.now().strftime('%Y-%m-%d')
    today_stat = query(
        "SELECT pv, uv FROM daily_stats WHERE site=%s AND date=%s",
        (site, today), one=True, site=site
    )
    week = query(
        """SELECT date, pv, uv FROM daily_stats
           WHERE site=%s AND date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
           ORDER BY date""",
        (site,), site=site
    )

    return jsonify({
        "total": total['visitor_count'] if total else 0,
        "today": {
            "pv": today_stat['pv'] if today_stat else 0,
            "uv": today_stat['uv'] if today_stat else 0
        },
        "week": serialize_dates(week) if week else []
    })
