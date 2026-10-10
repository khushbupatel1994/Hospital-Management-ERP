Cloud Secure Hospital ERP - FINAL FIXED BUILD

This package fixes the startup circular-import error:
LoginApp -> AdminDashboard -> LoginApp

Fix:
- AdminDashboard is imported locally only when login succeeds.
- LoginApp is imported locally only during logout.
- Hospital login image remains bundled through the existing PyInstaller spec.
- The original hospital.db is included and is used as the first-run seed in LOCALAPPDATA.
- Logout history remains enabled.
- Build script uses `python` instead of requiring the Windows `py` launcher.

BUILD:
1. Extract this ZIP completely.
2. Open the final_erp_source folder.
3. Double-click BUILD-FINAL-FIXED-WINDOWS.bat.
4. Wait for BUILD SUCCESSFUL.
5. Open:
   dist\Cloud Secure Hospital ERP\Cloud Secure Hospital ERP.exe

IMPORTANT:
- Do not delete database/hospital.db.
- Do not manually replace the database after first run.
- If SmartScreen appears for this self-built unsigned EXE, use More info -> Run anyway only if you trust this build.

Included original database record counts:
- doctors: 3
- patients: 4
- appointments: 2
- billing: 3
- inventory: 1
- accounts: 1
- OPD: 2
- IPD: 2
- medicines: 2
- laboratory: 1
- users: 5
