import configparser
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

import psycopg2


url = urlsplit(os.environ["DATABASE_URL"])
db_name = unquote(url.path.lstrip("/"))
db = {
    "host": url.hostname,
    "port": url.port or 5432,
    "user": unquote(url.username or ""),
    "password": unquote(url.password or ""),
    "dbname": db_name,
    "sslmode": "require",
    "connect_timeout": 30,
}

data_dir = Path(os.environ.get("ODOO_DATA_DIR", "/var/lib/odoo"))
data_dir.mkdir(parents=True, exist_ok=True)
config_path = data_dir / "tarea4.conf"
config = configparser.ConfigParser(interpolation=None)
config["options"] = {
    "admin_passwd": os.environ["ODOO_MASTER_PASSWORD"],
    "db_host": db["host"],
    "db_port": str(db["port"]),
    "db_user": db["user"],
    "db_password": db["password"],
    "db_name": db_name,
    "dbfilter": "^" + re.escape(db_name) + "$",
    "db_sslmode": "require",
    "db_maxconn": "8",
    "list_db": "False",
    "proxy_mode": "True",
    "http_interface": "0.0.0.0",
    "http_port": os.environ.get("PORT", "8069"),
    "workers": "0",
    "max_cron_threads": "0",
    "data_dir": str(data_dir),
    "addons_path": "/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons",
    "log_level": "info",
    "limit_time_real": "180",
}
with config_path.open("w", encoding="utf-8") as stream:
    config.write(stream)
config_path.chmod(0o600)

with psycopg2.connect(**db) as conn:
    with conn.cursor() as cr:
        cr.execute("SELECT to_regclass('public.ir_config_parameter')")
        initialized = False
        if cr.fetchone()[0]:
            cr.execute("SELECT value FROM ir_config_parameter WHERE key = %s",
                       ("tarea4.cloud.initialized",))
            initialized = cr.fetchone() == ("1",)

command = [sys.executable, "/usr/bin/odoo", "-c", str(config_path)]
if not initialized:
    print("Installing Ventas UNICAH and cloud storage on the new database.", flush=True)
    subprocess.run(command + [
        "-i", "ventas_unicah,unicah_cloud_storage",
        "--without-demo", "--load-language=es_ES",
        "--stop-after-init", "--no-http",
    ], check=True)
    bootstrap = Path(__file__).with_name("bootstrap.py").read_text(encoding="utf-8")
    subprocess.run(command[:2] + ["shell"] + command[2:] + ["--no-http"],
                   input=bootstrap, text=True, check=True)

os.execv(command[0], command)
