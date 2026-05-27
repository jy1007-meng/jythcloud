"""系统状态 API 蓝图"""
import os
import subprocess

from flask import Blueprint, jsonify
from flask import send_from_directory

from db import cached, clear_cache
from config import BASE_DIR, CACHE_TTL

bp = Blueprint('system', __name__, url_prefix='/api')


@bp.route('/status')
@cached(ttl_seconds=CACHE_TTL['status'])
def system_status():
    """系统状态总览"""
    result = {}

    # ─── CPU ───
    try:
        load = os.getloadavg()
        with open('/proc/cpuinfo') as f:
            cores = sum(1 for l in f if l.startswith('processor'))
        with open('/proc/stat') as f:
            vals = [int(x) for x in f.readline().split()[1:]]
            total = sum(vals)
            idle = vals[3]
        result['cpu'] = {
            'cores': cores,
            'percent': round((1 - idle / total) * 100, 1),
            'load': [round(l, 2) for l in load],
        }
    except Exception:
        result['cpu'] = {'cores': 4, 'percent': 0, 'load': [0, 0, 0]}

    # ─── 内存 ───
    try:
        with open('/proc/meminfo') as f:
            d = {}
            for l in f:
                parts = l.split(':')
                if len(parts) == 2:
                    k = parts[0].strip()
                    v = parts[1].strip().split()[0]
                    try:
                        d[k] = int(v) // 1024
                    except ValueError:
                        pass
        total_m = d.get('MemTotal', 0)
        avail_m = d.get('MemAvailable', d.get('MemFree', 0))
        used_m = total_m - avail_m
        result['memory'] = {
            'total': f'{total_m}MB',
            'used': f'{used_m}MB',
            'free': f'{avail_m}MB',
            'percent': round(used_m / total_m * 100, 1) if total_m else 0,
        }
    except Exception:
        result['memory'] = {'total': '--', 'used': '--', 'free': '--', 'percent': 0}

    # ─── 磁盘 ───
    try:
        stat = os.statvfs('/')
        total_d = stat.f_frsize * stat.f_blocks
        free_d = stat.f_frsize * stat.f_bfree
        used_d = total_d - free_d
        result['disk'] = {
            'total': f'{total_d // (1024**3)}GB',
            'used': f'{used_d // (1024**3)}GB',
            'free': f'{free_d // (1024**3)}GB',
            'percent': round(used_d / total_d * 100, 1) if total_d else 0,
        }
    except Exception:
        result['disk'] = {'total': '--', 'used': '--', 'free': '--', 'percent': 0}

    # ─── 运行时间 ───
    result['uptime'] = '--'
    try:
        with open('/proc/uptime') as f:
            secs = float(f.readline().split()[0])
            d = int(secs // 86400)
            h = int((secs % 86400) // 3600)
            m = int((secs % 3600) // 60)
            result['uptime'] = f'{d}天{h}小时{m}分'
    except Exception:
        pass

    # ─── 进程数 ───
    try:
        result['processes'] = {'total': len(os.listdir('/proc')) - 3}
    except Exception:
        result['processes'] = {'total': 0}

    # ─── Nginx ───
    try:
        r = subprocess.run(['nginx', '-t'], capture_output=True, text=True, timeout=3)
        result['nginx'] = {'active': 'ok' in r.stderr.lower()}
    except Exception:
        result['nginx'] = {'active': False}

    # ─── Docker ───
    try:
        r = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}|{{.Status}}'],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0 and r.stdout.strip():
            containers = []
            for line in r.stdout.strip().split('\n'):
                if '|' in line:
                    name, status = line.split('|', 1)
                    containers.append({'name': name, 'status': status})
            result['docker'] = {'count': len(containers), 'containers': containers}
        else:
            result['docker'] = {'count': 0, 'containers': []}
    except Exception:
        result['docker'] = {'count': 0, 'containers': []}

    # ─── 量化数据 ───
    result['quant'] = {'stock_count': 30}

    # ─── 网络 ───
    try:
        r = subprocess.run(['cat', '/proc/net/dev'], capture_output=True, text=True, timeout=3)
        for line in r.stdout.split('\n')[2:]:
            if line.strip():
                parts = line.split(':')
                if len(parts) == 2:
                    name = parts[0].strip()
                    if name.startswith('eth') or name.startswith('ens'):
                        data = parts[1].split()
                        rx = int(data[0]) // (1024**3)
                        tx = int(data[8]) // (1024**3)
                        result['network'] = {
                            'interfaces': [{'name': name, 'rx': rx, 'tx': tx}]
                        }
                        break
    except Exception:
        result['network'] = {'interfaces': []}

    return jsonify(result)


@bp.route('/status/cache-clear', methods=['POST'])
def clear_api_cache():
    """手动清除 API 缓存"""
    clear_cache()
    return jsonify({"success": True, "message": "缓存已清除"})
