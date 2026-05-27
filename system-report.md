# jythcloud.cn 系统生态分析报告
生成时间: 2026-05-27 00:41

## 一、网站全貌

### 主站
- **jythcloud.cn (HTTPS)** — 公司官网，Flask后端（Port 5002），有API层、管理后台
- Nginx 由宝塔面板托管，监听 80/443/888

### 三个简历子站（静态HTML + MySQL后端）
| 子域名 | 人物 | 说明 |
|--------|------|------|
| jy.jythcloud.cn | 吉天宇 | 数据科学 & AI 创业者 |
| tan.jythcloud.cn | 谭海涛 | 项目管理 & 执行负责人 |
| hu.jythcloud.cn | 胡子雄 | 商务拓展 & 客户成功 |
- 每个站点有独立的MySQL数据库（jy_site/tan_site/hu_site）
- Flask API (5002) 提供动态简历数据 + 浏览量统计 + 管理后台/api/templates/admin.html

### WordPress 站点
- **wordpress.jythcloud.cn** — 学习 WordPress，Docker 部署
- 当前只有1篇文章 + 1个页面
- 主题: Twenty Twenty-Five (FSE全站编辑)
- 0个激活的插件，0个评论
- 已配置独立 SSL 证书

### 其他服务
- NewAPI 服务（A3R5）— 含 MySQL(375MB) + Redis(7MB) + API(55MB)，很吃内存
- Workbuddy MCP — 12MB，很轻
- 宝塔面板 — 默认已装，Nginx由宝塔管理

## 二、系统资源 (3.6GB RAM)

### 内存占用 TOP5
| 进程 | 内存 | 说明 |
|------|------|------|
| NewAPI MySQL | 375MB 🔴 | 最重，可优化 |
| 主机 MySQL (宝塔) | 214MB | 双MySQL浪费 |
| Hermes Agent | 206MB | 我自己 |
| Docker daemon | 60MB | OK |
| WordPress PHP | 59MB | OK |

### 问题发现 🔍
1. **双MySQL运行** — 主机MySQL（宝塔/用于简历站）+ Docker内MySQL（用于WordPress/NewAPI），两个实例共占用~600MB
2. **NewAPI 资源偏高** — MySQL 375MB + API 55MB + Redis 7MB，只为你一个人服务的话可以精简
3. **系统可用内存仅1.8GB** — 余量紧张，如果再跑大任务可能交换swap
4. **无自动备份机制** — 仅有手动 backup.py，但没配cron
5. **WordPress 零插件、零内容** — 纯学习用，未配置缓存/SEO/安全插件

### 已做优化
- ✅ delegate_task 超时从600→180秒，重试3次
- ✅ quant-agent 已卸载（释放317MB Docker镜像）
- ✅ 已备份全部站点 + 数据库 (4.9MB)
- ✅ 系统配置优化：container_cpu=1, container_memory=5120, timeout=180

### 推荐优化（低token成本）
1. 主机MySQL与Docker MySQL合并 → 省200MB+
2. NewAPI MySQL使用独立轻量实例或SQLite → 省300MB
3. 添加 nginx 缓存层到简历站 → 省后端算力
4. 配置每日自动备份cron
5. WordPress 加个缓存插件（WP Super Cache）