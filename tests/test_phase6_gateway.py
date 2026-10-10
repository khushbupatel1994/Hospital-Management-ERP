import tempfile, sqlite3
from pathlib import Path
from server.module_gateway import list_records, create_record, update_record, delete_record

def setup_db():
    p=Path(tempfile.mkdtemp())/"t.db"
    with sqlite3.connect(p) as c:
        c.execute("CREATE TABLE patients (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, registration_no TEXT, patient_name TEXT, name TEXT, gender TEXT, dob TEXT, age INTEGER, blood_group TEXT, mobile TEXT, email TEXT, address TEXT, city TEXT, state TEXT, patient_type TEXT, assigned_doctor INTEGER, registration_date TEXT, status TEXT, created_at TEXT)")
        c.execute("INSERT INTO patients(patient_name,status) VALUES('Test Patient','Active')")
        c.commit()
    return p

def test_list_search_and_update():
    p=setup_db(); out=list_records(p,'patients','Admin',search='Test'); assert out['total']==1
    rid=out['items'][0]['id']; assert update_record(p,'patients','Admin',rid,{'status':'Inactive'})

def test_delete_protected():
    p=setup_db()
    try: delete_record(p,'patients','Admin',1)
    except PermissionError: return
    assert False
