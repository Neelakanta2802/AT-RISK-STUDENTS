-- ===================================================================
-- COMPLETE RLS POLICY FIX FOR EARLY WARNING SYSTEM
-- ===================================================================
-- This script FIXES ONLY the RLS policies that block backend operations
-- It does NOT create tables or duplicate existing policies
-- Safe to run - all DROP statements use IF EXISTS
-- ===================================================================

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
DROP POLICY IF EXISTS "Authenticated users can acknowledge alerts" ON alerts;
CREATE POLICY "Allow all operations on alerts"
  ON alerts FOR ALL
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
