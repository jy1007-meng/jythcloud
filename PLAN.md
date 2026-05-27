# jythcloud.cn 三站项目 — 实施规划

> 最后更新: 2026-05-27

## 📋 项目概况

三站合一 Flask 后端 + 三个独立前端静态页面，部署于腾讯云服务器。

| 站点 | 角色 | URL | 主题色 |
|------|------|-----|--------|
| 吉天宇 | 数据科学 & AI 创业 | jy.jythcloud.cn | 🟣 紫色 #6366f1 |
| 谭海涛 | 项目管理 & 执行负责人 | tan.jythcloud.cn | 🟢 绿色 #10b981 |
| 胡子雄 | 商务拓展 & 客户对接 | hu.jythcloud.cn | 🩷 粉色 #ec4899 |

## 🗂 文件结构

```
/www/wwwroot/
├── jythcloud/                    # 项目根目录
│   ├── api/                      # Flask 后端
│   │   ├── app.py                # 主应用 (MySQL版)
│   │   ├── config.py             # 数据库配置
│   │   ├── static/               # 静态资源
│   │   └── templates/            # 后台模板
│   │       ├── admin.html        # 管理后台
│   │       └── dashboard.html    # 数据大屏
│   ├── index.html                # 主站首页 (Hermes Agent)
│   ├── 404.html                  # 404页面
│   └── api.py                    # 服务器状态API
├── jy.jythcloud.cn/              # 吉天宇站点
│   ├── index.html                # 主页 (完整版)
│   ├── wechat-qr.jpg             # 微信二维码
│   └── campus-*.jpg              # 校园图片(6张)
├── tan.jythcloud.cn/             # 谭海涛站点
│   ├── index.html                # 主页
│   └── campus-*.jpg              # 校园图片
├── hu.jythcloud.cn/              # 胡子雄站点
│   ├── index.html                # 主页
│   └── campus-*.jpg              # 校园图片
├── backups/                      # 备份目录
│   └── YYYYMMDD_HHMMSS/          # 每次修改前的备份
└── hermes-site/                  # Hermes静态站点
```

## 🎯 已完成功能

### 前端 (三个站点)
- [x] 暗色主题风格（统一 CSS 变量体系）
- [x] Hero 主页（姓名、标题、学校、CTA按钮）
- [x] 关于我（3段个人自述）
- [x] 教育背景（湖北工程学院 + 校园图片 + 技能卡片）
- [x] 专业技能（4个技能卡片）
- [x] 项目/实践经历（时间线）
- [x] 角色定位（jy: AI创业 / tan: 管理 / hu: 商务）
- [x] 留言板（提交 + 展示）
- [x] 博客文章（列表 + 弹窗阅读）
- [x] 联系方式（邮箱复制 + GitHub链接 + 微信二维码）
- [x] 统计计数（总访问量 + 今日访问）
- [x] 移动端适配（hamburger菜单 + 响应式grid）
- [x] SEO（meta description + OG标签 + favicon）

### 后端 (Flask API)
- [x] MySQL 数据库（每站独立库）
- [x] 访问统计（page_views + daily_stats）
- [x] 留言管理（提交/回复/删除/已读标记）
- [x] 博客系统（CRUD + 浏览量统计）
- [x] 后台认证（JWT + admin/admin123）
- [x] 数据大屏（趋势/热力图/城市分布）
- [x] 站点配置（名称/副标题/主题色/简介）
- [x] 宝塔面板集成

## 📋 待办事项

### P0 — 必要功能
- [ ] tan 和 hu 的微信/邮箱真实信息（当前为示例）
- [ ] jy 的微信二维码已上传，tan/hu 等待上传
- [ ] GitHub 链接改为真实账号

### P1 — 体验优化
- [ ] 页面加载动画优化（骨架屏或进度条）
- [ ] 文章内容 XSS 防护（当前用 innerHTML）
- [ ] 留言板审核流（管理员审核后显示）
- [ ] 邮箱真实地址替换

### P2 — 内容完善
- [ ] 每人真实邮箱
- [ ] 每人真实微信二维码
- [ ] 每人真实 GitHub
- [ ] 每人真实项目/作品链接

### P3 — 代码质量
- [ ] 提取公共 CSS/JS 为外部文件（三站高度重复）
- [ ] 添加自动备份脚本
- [ ] 添加部署脚本
- [ ] 考虑使用 git 版本控制

## 🔧 常见操作

### 备份方法
```bash
# 手动备份
cp -r /www/wwwroot/jythcloud /www/wwwroot/jythcloud_backup_$(date +%Y%m%d)
cp /www/wwwroot/jy.jythcloud.cn/index.html /www/wwwroot/backups/jy_$(date +%Y%m%d_%H%M%S).html

# 自动备份脚本
python3 /www/wwwroot/jythcloud/scripts/backup.py
```

### 修改站点内容
1. 修改 `/www/wwwroot/[site].jythcloud.cn/index.html`
2. 测试 `curl https://[site].jythcloud.cn/`
3. 刷新浏览器验证

### 修改后端API
1. 修改 `/www/wwwroot/jythcloud/api/app.py`
2. 重启 uwsgi 或 Flask
3. 测试 API `curl http://127.0.0.1:5002/api/status`

## ⚡ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | 纯 HTML + CSS + JS (无框架) |
| 后端 | Flask (Python 3.11) |
| 数据库 | MySQL 5.7 (宝塔管理) |
| 服务器 | Nginx (反向代理) |
| 部署 | 腾讯云轻量服务器 (OpenCloudOS 9.4) |
| SSL | Let's Encrypt ECC 泛域名 |
| CDN | Google Fonts + Font Awesome + Chart.js |
