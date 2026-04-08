-- ===================================================================
-- FIX RLS POLICIES - Only Updates Policies, Doesn't Create Tables
-- ===================================================================
-- This script fixes ONLY the policies that block backend operations
-- It keeps existing SELECT policies intact
-- Safe to run multiple times - uses IF EXISTS
-- ===================================================================

-- ============================================================
-- FIX 1: risk_assessments table
-- Drop the restrictive policy and create permissive one
-- ============================================================
DROP POLICY IF EXISTS "Administrators can manage risk assessments" ON risk_assessments;
CREATE POLICY "Allow all operations on risk_assessments"
  ON risk_assessments FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 2: students table
-- Drop restrictive INSERT/UPDATE policies and create permissive one
-- ============================================================
DROP POLICY IF EXISTS "Administrators can insert students" ON students;
DROP POLICY IF EXISTS "Administrators can update students" ON students;
CREATE POLICY "Allow all operations on students"
  ON students FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 3: academic_records table
-- Drop restrictive policy and create permissive one
-- ============================================================
DROP POLICY IF EXISTS "Administrators can manage academic records" ON academic_records;
CREATE POLICY "Allow all operations on academic_records"
  ON academic_records FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 4: attendance_records table
-- Drop restrictive policy and create permissive one
-- ============================================================
DROP POLICY IF EXISTS "Faculty and administrators can manage attendance" ON attendance_records;
CREATE POLICY "Allow all operations on attendance_records"
  ON attendance_records FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 5: alerts table
-- Drop restrictive policies and create permissive one
-- ============================================================
DROP POLICY IF EXISTS "Administrators can create alerts" ON alerts;
DROP POLICY IF EXISTS "Authenticated users can acknowledge alerts" ON alerts;
CREATE POLICY "Allow all operations on alerts"
  ON alerts FOR ALL
  USING (true)
  WITH CHECK (true);

-- ============================================================
-- FIX 6: interventions table
-- Drop restrictive policies and create permissive one
-- ============================================================
DROP POLICY IF EXISTS "Administrators and counselors can create interventions" ON interventions;
DROP POLICY IF EXISTS "Assigned users can update interventions" ON interventions;
CREATE POLICY "Allow all operations on interventions"
  ON interventions FOR ALL
  USING (true)
  WITH CHECK (true);

-- ===================================================================
-- VERIFICATION: Check policies (optional - uncomment to run)
-- ===================================================================
-- SELECT 
--     tablename,
--     policyname,
--     cmd,
--     roles,
--     qual,
--     with_check
-- FROM pg_policies
-- WHERE schemaname = 'public'
--   AND tablename IN ('students', 'risk_assessments', 'academic_records', 'attendance_records', 'alerts', 'interventions')
-- ORDER BY tablename, policyname;
