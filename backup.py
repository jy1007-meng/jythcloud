#!/usr/bin/env python3
"""jythcloud.cn 自动备份脚本 - 每次修改前执行"""
import shutil, datetime, os, sys
from pathlib import Path

BACKUP_ROOT = Path("/www/wwwroot/jythcloud/backups")
MAX_BACKUPS = 20  # 最多保留20份

FILES_TO_BACKUP = [
    "/www/wwwroot/jy.jythcloud.cn/index.html",
    "/www/wwwroot/tan.jythcloud.cn/index.html",
    "/www/wwwroot/hu.jythcloud.cn/index.html",
    "/www/wwwroot/jythcloud/api/app.py",
]

IMAGES_DIRS = [
    "/www/wwwroot/jy.jythcloud.cn/",
    "/www/wwwroot/tan.jythcloud.cn/",
    "/www/wwwroot/hu.jythcloud.cn/",
]

def backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_ROOT / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Backup files
    for f in FILES_TO_BACKUP:
        src = Path(f)
        if src.exists():
            shutil.copy2(str(src), str(backup_dir / src.name))
            print(f"  ✅ {src.name}")
    
    # Backup images
    img_dir = backup_dir / "images"
    img_dir.mkdir(exist_ok=True)
    for d in IMAGES_DIRS:
        for img in Path(d).glob("*.jpg"):
            shutil.copy2(str(img), str(img_dir / img.name))
        for img in Path(d).glob("*.png"):
            shutil.copy2(str(img), str(img_dir / img.name))
    
    # Clean old backups
    all_backups = sorted(BACKUP_ROOT.iterdir())
    while len(all_backups) > MAX_BACKUPS:
        oldest = all_backups.pop(0)
        shutil.rmtree(str(oldest))
        print(f"  🗑️ Removed old backup: {oldest.name}")
    
    print(f"\n📁 Backup saved: {backup_dir}")
    print(f"📦 Size: {sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file()) / 1024:.1f}KB")
    return str(backup_dir)

if __name__ == "__main__":
    print(f"=== jythcloud.cn Backup ({datetime.datetime.now():%Y-%m-%d %H:%M}) ===")
    backup()
