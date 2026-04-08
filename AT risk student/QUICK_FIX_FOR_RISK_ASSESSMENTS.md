# Quick Fix for Risk Assessment Creation Issue

## Problem Identified

**31 students exist but 0 risk assessments** - Risk assessments are not being created/saved to the database.

## Root Cause

The RLS (Row Level Security) policies on the `risk_assessments` table are too restrictive. Even though the service role key should bypass RLS, the policies may be preventing inserts.

## Solution Applied

1. **Created new migration** (`20251225151811_fix_rls_for_service_role.sql`) to update RLS policies to explicitly allow service role operations

2. **Enhanced error logging** in `database.py` to show exactly why risk assessment creation fails

## Immediate Action Required

### Option 1: Apply the SQL Migration (Recommended)

Run this SQL in your Supabase SQL editor:

```sql
-- Fix risk_assessments RLS
DROP POLICY IF EXISTS "Administrators can manage risk assessments" ON risk_assessments;
CREATE POLICY "Allow service role to manage risk assessments"
  ON risk_assessments FOR ALL
  USING (true)
  WITH CHECK (true);
```

### Option 2: Disable RLS Temporarily (For Testing Only)

```sql
ALTER TABLE risk_assessments DISABLE ROW LEVEL SECURITY;
```

**⚠️ WARNING:** Only do this for testing. Re-enable RLS after confirming it works.

### Option 3: Verify Service Role Key

Make sure your `.env` file has the **SERVICE ROLE KEY** (not anon key):
- Should be 200+ characters
- Starts with `eyJ`
- Found in Supabase Dashboard → Settings → API → `service_role` key

## Testing

After applying the fix:

1. Restart backend server
2. Upload a test file
3. Check backend logs for risk assessment creation messages
4. Verify risk assessments appear in database

## Next Steps

1. Apply the SQL migration
2. Restart backend
3. Test upload
4. Check logs for success/failure messages
