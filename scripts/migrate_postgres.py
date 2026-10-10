"""Guarded PostgreSQL migration entry point.
This intentionally does not auto-copy unknown hospital schemas. Run after mapping and backup review.
"""
import os
print('DATABASE_URL:', os.getenv('DATABASE_URL', '<not set>'))
print('Migration guard: schema mapping + backup confirmation required before data migration.')
