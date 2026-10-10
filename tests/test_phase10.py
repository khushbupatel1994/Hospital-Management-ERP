import tempfile
import sqlite3
from pathlib import Path

from production_readiness import sqlite_backup, verify_sqlite, sha256_file


def test_backup_and_verify():
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "db.sqlite3"

        con = sqlite3.connect(src)
        cur = con.cursor()

        try:
            cur.execute(
                "create table t(id integer primary key, name text)"
            )
            cur.execute(
                "insert into t(name) values (?)",
                ("demo",)
            )
            con.commit()
        finally:
            cur.close()
            con.close()

        b = sqlite_backup(str(src), d)

        assert verify_sqlite(str(b))["ok"]
        assert len(sha256_file(str(b))) == 64


def test_phase10_files():
    root = Path(__file__).parents[1]

    assert (root / "deploy/docker-compose.production.yml").exists()
    assert (root / "deploy/nginx.conf").exists()
    assert (root / "DOCKERFILE").exists()