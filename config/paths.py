import os
import sys

APP_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Cloud Secure Hospital ERP")
DATABASE_DIR = os.path.join(APP_DATA_DIR, "database")
CONFIG_DIR = os.path.join(APP_DATA_DIR, "config")


def resource_path(*parts):
    """Return a path to a bundled/read-only application resource."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


def ensure_app_dirs():
    os.makedirs(DATABASE_DIR, exist_ok=True)
    os.makedirs(CONFIG_DIR, exist_ok=True)
    return APP_DATA_DIR
