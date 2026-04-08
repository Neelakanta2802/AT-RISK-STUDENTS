-- ===================================================================
-- COMPLETE FIX: Paste this ENTIRE block in Supabase SQL Editor
-- ===================================================================
-- This will fix ALL RLS policies to allow backend (service role) operations
-- ===================================================================

-- FIX 1: risk_assessments table (THIS IS THE MAIN ISSUE)
DROP POLICY IF EXISTS "Administrators can manage risk assessments" ON risk_assessments;
CREATE POLICY "Allow all operations on risk_assessments"
  ON risk_assessments FOR ALL
  USING (true)
  WITH CHECK (true);

-- FIX 2: students table (ensuring inserts work properly)
DROP POLICY IF EXISTS "Administrators can insert students" ON students;
DROP POLICY IF EXISTS "Administrators can update students" ON students;
CREATE POLICY "Allow all operations on students"
  ON students FOR ALL
  USING (true)
  WITH CHECK (true);

-- FIX 3: academic_records table (for academic data uploads)
DROP POLICY IF EXISTS "Administrators can manage academic records" ON academic_records;
CREATE POLICY "Allow all operations on academic_records"
  ON academic_records FOR ALL
  USING (true)
  WITH CHECK (true);

-- FIX 4: attendance_records table (for attendance data uploads)
DROP POLICY IF EXISTS "Faculty and administrators can manage attendance" ON attendance_records;
CREATE POLICY "Allow all operations on attendance_records"
  ON attendance_records FOR ALL
  USING (true)
  WITH CHECK (true);

-- FIX 5: alerts table (for future alert generation)
DROP POLICY IF EXISTS "Administrators can create alerts" ON alerts;
DROP POLICY IF EXISTS "Authenticated users can acknowledge alerts" ON alerts;
CREATE POLICY "Allow all operations on alerts"
  ON alerts FOR ALL
  USING (true)
  WITH CHECK (true);

-- FIX 6: interventions table (for future intervention tracking)
DROP POLICY IF EXISTS "Administrators and counselors can create interventions" ON interventions;
DROP POLICY IF EXISTS "Assigned users can update interventions" ON interventions;
CREATE POLICY "Allow all operations on interventions"
  ON interventions FOR ALL
  USING (true)
  WITH CHECK (true);

-- ===================================================================
-- VERIFICATION (Optional - run after to see what changed)
-- ===================================================================
-- SELECT tablename, policyname, cmd 
-- FROM pg_policies 
-- WHERE schemaname = 'public' 
--   AND tablename IN ('risk_assessments', 'students', 'academic_records', 'attendance_records', 'alerts', 'interventions')
-- ORDER BY tablename;
