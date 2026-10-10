import tempfile, sqlite3
from pathlib import Path
from enterprise_phase8.backup import backup_sqlite
from enterprise_phase8.health import database_health
from enterprise_phase8.security import TokenRevocationStore

def test_revocation():
    s=TokenRevocationStore(); s.revoke('x', 4102444800); assert s.is_revoked('x')

def test_health_and_backup():
    with tempfile.TemporaryDirectory() as d:
        db=Path(d)/'hospital.db'; con=sqlite3.connect(db); con.execute('create table t(id integer)'); con.commit(); con.close()
        assert database_health(db)['ok']
        out=backup_sqlite(db, Path(d)/'backups'); assert out.exists()
