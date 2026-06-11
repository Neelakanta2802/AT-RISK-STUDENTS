#!/usr/bin/env python3
"""
Validation script for Neon/PostgreSQL Query Builder integration.
Tests query translation logic (offline) and live database connection (if DATABASE_URL is set).
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env variables
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))
load_dotenv(backend_dir / ".env")

from database import PostgresQueryBuilder, PostgresResponse

# Mock connection pool for unit testing query output
class MockConnection:
    def __init__(self):
        self.executed_queries = []
        
    def cursor(self):
        return MockCursor(self)
        
    def close(self):
        pass

class MockCursor:
    def __init__(self, conn):
        self.conn = conn
        
    def execute(self, query, params=None):
        self.conn.executed_queries.append((query, params or []))
        
    def fetchall(self):
        return [] # Return empty result for mocking
        
    def close(self):
        pass

class MockConnectionPool:
    def __init__(self):
        self.conn = MockConnection()
        
    def get_connection(self):
        return self.conn

print("=" * 80)
print("             POSTGRES / NEON INTEGRATION VALIDATOR")
print("=" * 80)

# ----------------------------------------------------------------------------
# PART 1: Unit Tests for PostgresQueryBuilder SQL Generation
# ----------------------------------------------------------------------------
print("\n--- PART 1: Testing SQL Query Generation (Offline) ---")

pool = MockConnectionPool()

def run_test(name, builder_func, expected_sql_substring, expected_params):
    pool.conn.executed_queries.clear()
    builder = PostgresQueryBuilder("students", pool)
    builder_func(builder).execute()
    
    assert len(pool.conn.executed_queries) == 1, f"Expected 1 query to be executed, got {len(pool.conn.executed_queries)}"
    query, params = pool.conn.executed_queries[0]
    
    # Check substring
    sql_ok = expected_sql_substring.lower() in query.lower()
    params_ok = params == expected_params
    
    if sql_ok and params_ok:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}")
        print(f"  Generated SQL: {query}")
        print(f"  Expected query to contain: {expected_sql_substring}")
        print(f"  Generated params: {params}")
        print(f"  Expected params: {expected_params}")
        sys.exit(1)

# Test 1: Simple Select
run_test(
    "Simple Select with Filter",
    lambda b: b.select("*").eq("status", "active"),
    "SELECT * FROM students WHERE status = %s",
    ["active"]
)

# Test 2: Order, Limit, and Offset
run_test(
    "Select with Order, Limit, Offset",
    lambda b: b.select("id, name").order("created_at", desc=True).limit(5).offset(10),
    "SELECT id, name FROM students ORDER BY created_at DESC LIMIT %s OFFSET %s",
    [5, 10]
)

# Test 3: IN filter
run_test(
    "Select with IN Filter",
    lambda b: b.select("*").in_("id", ["uuid1", "uuid2"]),
    "SELECT * FROM students WHERE id IN (%s, %s)",
    ["uuid1", "uuid2"]
)

# Test 4: Delete with Filter
run_test(
    "Delete with Filter",
    lambda b: b.delete().eq("id", "uuid-to-delete"),
    "DELETE FROM students WHERE id = %s RETURNING *",
    ["uuid-to-delete"]
)

# Test 5: Insert (dict)
run_test(
    "Insert Single Record",
    lambda b: b.insert({"name": "Test User", "status": "active"}),
    "INSERT INTO students (name, status) VALUES (%s, %s) RETURNING *",
    ["Test User", "active"]
)

# Test 6: Update with Filter
run_test(
    "Update Record",
    lambda b: b.update({"status": "inactive"}).eq("id", "uuid-to-update"),
    "UPDATE students SET status = %s WHERE id = %s RETURNING *",
    ["inactive", "uuid-to-update"]
)

print("[OK] All offline query generation tests passed.")

# ----------------------------------------------------------------------------
# PART 2: Live Integration Test (Only if DATABASE_URL is set)
# ----------------------------------------------------------------------------
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("\n--- PART 2: Live Database Test (Skipped) ---")
    print("Set DATABASE_URL environment variable to run live integration tests.")
    print("Example:")
    print("  $env:DATABASE_URL=\"postgresql://user:pass@host/dbname?sslmode=require\"")
else:
    print(f"\n--- PART 2: Live Database Test (Target: {db_url.split('@')[-1] if '@' in db_url else 'Neon DB'}) ---")
    
    # Import main Database class to trigger live connection
    from database import db
    
    if db.client is None:
        print("[FAIL] Database client failed to initialize.")
        sys.exit(1)
        
    try:
        print("Testing select query on live database...")
        # Check if table exists by selecting 1 record
        res = db.client.table("students").select("id").limit(1).execute()
        print(f"[OK] Live query succeeded. Fetched {len(res.data)} rows.")
        print("\n[OK] Live database integration verified successfully!")
    except Exception as live_err:
        print(f"[FAIL] Live query failed: {live_err}")
        print("Please verify your Neon database is active and deploy_neon_db.py has been run.")
        sys.exit(1)

print("\n" + "=" * 80)
print("INTEGRATION VALIDATION SUCCESSFULLY PASSED!")
print("=" * 80)
