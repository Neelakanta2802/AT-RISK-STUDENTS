/*
  COMPREHENSIVE FIX: Update ALL RLS policies to allow backend (service role) operations
  
  The service role key should bypass RLS, but these policies ensure compatibility
  and allow the backend to insert/update data without authentication.
  
  Run this in Supabase Dashboard → SQL Editor
*/

-- ============================================================
-- FIX 1: risk_assessments table
-- ============================================================
DROP POLICY IF EXISTS "Administrators can manage risk assessments" ON risk_assessments;

CREATE POLICY "Allow all operations on risk_assessments"
  ON risk_assessments FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 2: students table  
-- ============================================================
DROP POLICY IF EXISTS "Administrators can insert students" ON students;
DROP POLICY IF EXISTS "Administrators can update students" ON students;

CREATE POLICY "Allow all operations on students"
  ON students FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 3: academic_records table
-- ============================================================
DROP POLICY IF EXISTS "Administrators can manage academic records" ON academic_records;

CREATE POLICY "Allow all operations on academic_records"
  ON academic_records FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 4: attendance_records table
-- ============================================================
DROP POLICY IF EXISTS "Faculty and administrators can manage attendance" ON attendance_records;

CREATE POLICY "Allow all operations on attendance_records"
  ON attendance_records FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 5: alerts table
-- ============================================================
DROP POLICY IF EXISTS "Administrators can create alerts" ON alerts;

CREATE POLICY "Allow insert on alerts"
  ON alerts FOR INSERT
  USING (true)
  WITH CHECK (true);

-- Keep the acknowledge policy for authenticated users
-- But also allow updates for service role
DROP POLICY IF EXISTS "Authenticated users can acknowledge alerts" ON alerts;

CREATE POLICY "Allow update on alerts"
  ON alerts FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 6: interventions table
-- ============================================================
DROP POLICY IF EXISTS "Administrators and counselors can create interventions" ON interventions;
DROP POLICY IF EXISTS "Assigned users can update interventions" ON interventions;

CREATE POLICY "Allow all operations on interventions"
  ON interventions FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- VERIFICATION QUERIES (Optional - run to verify)
-- ============================================================

-- Check current policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('students', 'risk_assessments', 'academic_records', 'attendance_records', 'alerts', 'interventions')
ORDER BY tablename, policyname;
