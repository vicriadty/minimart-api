#!/usr/bin/env python3
"""Backup minimart.db ke ~/backups/, simpan 7 terakhir."""

import shutil
from datetime import datetime
from pathlib import Path

SRC = Path("/home/deploy/minimart-api/minimart.db")
DST_DIR = Path.home() / "backups"
DST_DIR.mkdir(exist_ok=True)

name = f"minimart-{datetime.now():%Y%m%d-%H%M%S}.db"
shutil.copy2(SRC, DST_DIR / name)

for old in sorted(DST_DIR.glob("minimart-*.db"))[:-7]:
    old.unlink()
print(f"Backup OK: {name}")
