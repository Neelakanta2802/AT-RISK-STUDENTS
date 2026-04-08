#!/usr/bin/env python3
"""
Test script to diagnose why risk assessments aren't being created.
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "project" / "backend"
sys.path.insert(0, str(backend_path))

from database import db
from monitoring import monitoring_engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("=" * 80)
    print("Testing Risk Assessment Creation")
    print("=" * 80)
    
    # Check database connection
    if db.client is None:
        print("❌ Database client not initialized!")
        return
    
    print("✅ Database client initialized")
    
    # Get first student
    students = db.get_students(limit=1)
    if not students:
        print("❌ No students found in database!")
        return
    
    student = students[0]
    student_id = student['id']
    print(f"✅ Found student: {student.get('full_name')} (ID: {student_id})")
    
    # Try to evaluate this student
    print(f"\n📊 Attempting to create risk assessment for student {student_id}...")
    try:
        result = monitoring_engine.evaluate_student(student_id, force_reassessment=True)
        
        if result:
            print(f"✅ Risk assessment result returned!")
            print(f"   Assessment: {result.get('assessment') is not None}")
            print(f"   Alerts created: {result.get('alerts_created', 0)}")
            
            # Check if assessment was actually saved
            assessments = db.get_risk_assessments(student_id=student_id, limit=1)
            if assessments:
                print(f"✅ Risk assessment saved to database!")
                print(f"   Risk Level: {assessments[0].get('risk_level')}")
                print(f"   Risk Score: {assessments[0].get('risk_score')}")
            else:
                print("❌ Risk assessment NOT saved to database (result returned but not persisted)")
        else:
            print("❌ evaluate_student returned None - check logs above for errors")
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("Test Complete")
    print("=" * 80)

if __name__ == "__main__":
    main()
