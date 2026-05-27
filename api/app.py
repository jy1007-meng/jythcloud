"""
JYTHCloud API — 模块化 Flask 应用

路由结构：
  /api/visit           POST   — 记录访问
  /api/stats/<site>     GET   — 获取统计
  /api/message         POST   — 提交留言
  /api/messages/<site>  GET   — 获取留言
  /api/articles/<site>  GET   — 文章列表
  /api/article/<site>/<id> GET — 文章详情
  /api/dashboard/<site> GET   — 数据大屏
  /api/status           GET   — 系统状态

管理后台（需 Bearer token）：
  /api/admin/dashboard/<site>   GET — 仪表盘
  /api/admin/articles/<site>    GET — 文章管理
  /api/admin/article            POST — 创建文章
  /api/admin/article/<id>    PUT/DEL — 编辑/删除
  /api/admin/messages/<site>    GET — 留言管理
  /api/admin/message/<id>/read  POST — 标记已读
  /api/admin/site-config/<site> GET/PUT — 站点配置
  /api/admin/users              GET — 用户列表
  /api/admin/user               POST — 创建用户
  /api/admin/change-password    POST — 改密码
  /api/status/cache-clear       POST — 清除缓存

页面路由：
  /admin/<site>   — 管理后台页
  /dashboard/<site> — 数据大屏页
"""
from flask import Flask, send_from_directory
from flask_cors import CORS

from config import BASE_DIR
from db import init_db, close_db

app = Flask(__name__, static_folder='static')
CORS(app)

# ─── 注册蓝图 ───
from modules.stats import bp as stats_bp
from modules.messages import bp as messages_bp
from modules.articles import bp as articles_bp
from modules.admin import bp as admin_bp
from modules.dashboard_data import bp as dashboard_bp
from modules.status import bp as status_bp

app.register_blueprint(stats_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(articles_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(status_bp)

# ─── 请求生命周期 ───
app.teardown_appcontext(close_db)


# ─── 页面路由 ───
@app.route('/admin/<site>')
def admin_page(site):
    return send_from_directory(str(BASE_DIR / 'templates'), 'admin.html')


@app.route('/dashboard/<site>')
def dashboard_page(site):
    return send_from_directory(str(BASE_DIR / 'templates'), 'dashboard.html')


# ─── 启动 ───
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    print(f"\n🚀 JYTHCloud API 启动 (端口 {port}, debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
