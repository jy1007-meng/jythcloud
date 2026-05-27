#! /usr/bin/env python3
"""服务器状态API - v2.0 完整版"""
import json, os, time, subprocess, socket, sys
from pathlib import Path

def get_uptime():
    try:
        with open('/proc/uptime') as f:
            seconds = float(f.read().split()[0])
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{days}d {hours}h {mins}m"
    except:
        return "--"

def get_cpu_info():
    try:
        load = os.getloadavg()
        # 获取CPU核心数
        cores = os.cpu_count() or 1
        # 过去1分钟负载百分比
        pct = min(round(load[0] / cores * 100, 1), 100)
        return {
            "load": f"{load[0]:.1f} {load[1]:.1f} {load[2]:.1f}",
            "percent": pct,
            "cores": cores
        }
    except:
        return {"load": "--", "percent": 0, "cores": 1}

def get_mem_info():
    try:
        with open('/proc/meminfo') as f:
            lines = [l.strip() for l in f.readlines()]
        total_kb = int([l for l in lines if l.startswith('MemTotal:')][0].split()[1])
        avail_kb = int([l for l in lines if l.startswith('MemAvailable:')][0].split()[1])
        total = round(total_kb / 1024**2, 2)
        avail = round(avail_kb / 1024**2, 2)
        used = round(total - avail, 2)
        pct = round(used / total * 100, 1)
        return {
            "total": f"{total:.2f}GB",
            "used": f"{used:.2f}GB",
            "free": f"{avail:.2f}GB",
            "percent": pct
        }
    except:
        return {"total": "--", "used": "--", "free": "--", "percent": 0}

def get_disk_info():
    try:
        st = os.statvfs('/')
        total = st.f_frsize * st.f_blocks / (1024**3)
        free = st.f_frsize * st.f_bfree / (1024**3)
        used = total - free
        pct = round(used / total * 100, 1)
        return {
            "total": f"{total:.1f}GB",
            "used": f"{used:.1f}GB",
            "free": f"{free:.1f}GB",
            "percent": pct
        }
    except:
        return {"total": "--", "used": "--", "free": "--", "percent": 0}

def get_network_info():
    """获取网络接口流量"""
    try:
        net_dev = Path('/proc/net/dev').read_text()
        lines = net_dev.strip().split('\n')[2:]  # 跳过表头
        rx_total = tx_total = 0
        interfaces = []
        for line in lines:
            parts = line.split()
            iface = parts[0].rstrip(':')
            if iface in ('lo',): 
                continue
            rx_bytes = int(parts[1])
            tx_bytes = int(parts[9])
            rx_total += rx_bytes
            tx_total += tx_bytes
            interfaces.append({
                "name": iface,
                "rx": round(rx_bytes / 1024**3, 2),
                "tx": round(tx_bytes / 1024**3, 2)
            })
        return {
            "interfaces": interfaces,
            "rx_total": f"{round(rx_total / 1024**3, 2)}GB",
            "tx_total": f"{round(tx_total / 1024**3, 2)}GB"
        }
    except:
        return {"interfaces": [], "rx_total": "--", "tx_total": "--"}

def get_process_count():
    try:
        result = subprocess.run(['ps', 'aux', '--no-headers'], 
                               capture_output=True, text=True, timeout=3)
        total = len(result.stdout.strip().split('\n'))
        # 统计各用户进程数
        users = {}
        for line in result.stdout.strip().split('\n'):
            if line:
                user = line.split()[0]
                users[user] = users.get(user, 0) + 1
        return {"total": total, "users": dict(sorted(users.items(), key=lambda x: -x[1])[:5])}
    except:
        return {"total": "--", "users": {}}

def get_nginx_connections():
    """获取Nginx活跃连接数"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'http://127.0.0.1/nginx_status'],
            capture_output=True, text=True, timeout=3
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 3:
            active = lines[0].split(':')[1].strip() if ':' in lines[0] else "--"
            # 第二行解释
            parts = lines[2].split()
            if len(parts) >= 8:
                return {
                    "active": active,
                    "accepted": parts[0],
                    "handled": parts[1],
                    "requests": parts[2],
                    "reading": parts[4] if len(parts) > 4 else "--",
                    "writing": parts[6] if len(parts) > 6 else "--",
                    "waiting": parts[8] if len(parts) > 8 else "--"
                }
        return {"active": "--"}
    except:
        return {"active": "--"}

def get_docker_status():
    try:
        result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}|{{.Status}}|{{.Image}}'],
                               capture_output=True, text=True, timeout=3)
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                containers.append({
                    "name": parts[0],
                    "status": parts[1] if len(parts) > 1 else "",
                    "image": parts[2] if len(parts) > 2 else ""
                })
        return {"count": len(containers), "containers": containers}
    except:
        return {"count": 0, "containers": []}

def get_quant_status():
    """获取量化交易状态（如果有策略文件）"""
    quant_dir = Path(os.path.expanduser('~/.hermes/knowledge/quant'))
    state_dir = quant_dir / 'trades' / 'state'
    try:
        # 查找最新的状态文件
        state_files = sorted(state_dir.glob('*.json')) if state_dir.exists() else []
        latest_state = {}
        if state_files:
            latest_state = json.loads(state_files[-1].read_text())
        
        # 检查数据文件
        data_dir = quant_dir / 'data' / 'stock_kline'
        stock_count = len(list(data_dir.glob('*.csv'))) if data_dir.exists() else 0
        
        return {
            "active": True,
            "stock_count": stock_count,
            "state_file": state_files[-1].name if state_files else None,
            "latest_snapshot": latest_state.get('portfolio_total', '--'),
            "positions": latest_state.get('holdings_count', 0)
        }
    except:
        return {"active": False, "stock_count": 0}

# 组装完整状态
status = {
    "server": "Hermes Agent",
    "ip": "81.71.27.84",
    "hostname": socket.gethostname(),
    "os": "OpenCloudOS 9.4",
    "uptime": get_uptime(),
    "cpu": get_cpu_info(),
    "memory": get_mem_info(),
    "disk": get_disk_info(),
    "network": get_network_info(),
    "processes": get_process_count(),
    "nginx": get_nginx_connections(),
    "docker": get_docker_status(),
    "quant": get_quant_status(),
    "timestamp": int(time.time())
}

# 支持 jsonp 或直接输出
callback = os.environ.get('HTTP_JSONP')
output = json.dumps(status, ensure_ascii=False)
if callback:
    print(f"{callback}({output})")
else:
    print(output)
