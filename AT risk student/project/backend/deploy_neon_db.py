#!/usr/bin/env python3
"""
Neon Database Schema Deployer for Early Warning System.
Connects to Neon PostgreSQL and runs the database migrations to set up the EWS schema.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
backend_dir = Path(__file__).resolve().parent
project_dir = backend_dir.parent
load_dotenv(backend_dir / ".env")
load_dotenv(project_dir / ".env")

# Try to import psycopg2
try:
    import psycopg2
except ImportError:
    print("[ERROR] psycopg2 is not installed. Please install it using 'pip install psycopg2-binary'")
    sys.exit(1)

# Get database connection string
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("[ERROR] DATABASE_URL environment variable is missing!")
    print("Please set it in your environment or in a .env file.")
    sys.exit(1)

# Render/Neon postgres standard compatibility
if db_url.startswith("postgres://"):
    db_url = "postgresql://" + db_url[len("postgres://"):]

print("=" * 80)
print("             EWS NEON DATABASE SCHEMA DEPLOYER")
print("=" * 80)
print(f"Target DB: {db_url.split('@')[-1] if '@' in db_url else 'Neon DB'}")
print()

# Migration SQL files list
migration_files = [
    # 1. Base EWS schema
    project_dir / "supabase" / "migrations" / "20251225151810_create_ews_schema.sql",
    # 2. Upload history table
    project_dir / "supabase" / "migrations" / "20260112_create_upload_history.sql",
    # 3. Enhanced RLS fixes (skip policy edits since direct connection bypasses RLS, but we'll apply them for schema completeness)
    project_dir / "supabase" / "migrations" / "20251225151811_fix_rls_for_service_role.sql",
    # 4. Behavioral indicators, metadata, views, and functions
    backend_dir / "database_migrations.sql"
]

# Check migration files exist
missing_files = [f for f in migration_files if not f.exists()]
if missing_files:
    print("[ERROR] The following migration files are missing:")
    for f in missing_files:
        print(f"  - {f}")
    sys.exit(1)

compatibility_sql = """
-- 1. Create mock Auth schema for Supabase compatibility
CREATE SCHEMA IF NOT EXISTS auth;
CREATE TABLE IF NOT EXISTS auth.users (
    id uuid PRIMARY KEY,
    email text UNIQUE
);

-- 2. Create mock roles if they do not exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN
    CREATE ROLE authenticated;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
    CREATE ROLE anon;
  END IF;
END
$$;

-- 3. Create mock auth.uid() function
CREATE OR REPLACE FUNCTION auth.uid()
RETURNS uuid
LANGUAGE sql STABLE
AS $$
  SELECT '00000000-0000-0000-0000-000000000000'::uuid;
$$;
"""

try:
    print("Connecting to database...")
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    print("[OK] Connected successfully.")
    
    # Run compatibility setup
    print("\nRunning Supabase compatibility setup...")
    cur.execute(compatibility_sql)
    print("[OK] Compatibility schema and roles configured.")
    
    # Run migration files
    for file_path in migration_files:
        print(f"\nApplying migration: {file_path.name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        try:
            cur.execute(sql_content)
            print(f"[OK] Successfully applied {file_path.name}")
        except Exception as file_err:
            print(f"[ERROR] Failed to apply {file_path.name}")
            print(f"Reason: {file_err}")
            # Ask if we should continue or exit
            choice = input("Would you like to skip this file and continue? (y/N): ").strip().lower()
            if choice != 'y':
                sys.exit(1)
                
    print("\n" + "=" * 80)
    print("DATABASE SCHEMA DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] Migration failed: {e}")
    sys.exit(1)
finally:
    if 'cur' in locals() and cur:
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()
