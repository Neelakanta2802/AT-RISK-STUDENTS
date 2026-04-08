#!/usr/bin/env python3
"""
Quick health check script for the Early Warning System backend.
Tests critical functionality to verify all fixes are working.
"""
import sys
import os
import requests
import json
from datetime import datetime

# Add backend to path if running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project', 'backend'))

def test_diagnostics_endpoint(base_url="http://localhost:8000"):
    """Test the diagnostics endpoint."""
    print("=" * 80)
    print("🔍 Testing Diagnostics Endpoint")
    print("=" * 80)
    
    try:
        response = requests.get(f"{base_url}/api/diagnostics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Diagnostics endpoint is accessible")
            print(f"\nCode Version: {data.get('code_version', 'unknown')}")
            
            # Database status
            db_status = data.get('database', {})
            print(f"\n📊 Database Status:")
            print(f"  Connected: {'✅' if db_status.get('connected') else '❌'}")
            print(f"  Can Read: {'✅' if db_status.get('can_read') else '❌'}")
            print(f"  Can Write: {'✅' if db_status.get('can_write') else '❌'}")
            print(f"  Student Count: {db_status.get('student_count', 0)}")
            print(f"  Risk Assessment Count: {db_status.get('risk_assessment_count', 0)}")
            print(f"  Students Without Assessments: {db_status.get('students_without_assessments', 0)}")
            
            # ML Model status
            ml_status = data.get('ml_models', {})
            print(f"\n🤖 ML Model Status:")
            print(f"  Model Loaded: {'✅' if ml_status.get('risk_engine_loaded') else '❌'}")
            print(f"  Model Trained: {'✅' if ml_status.get('model_trained') else '❌'}")
            print(f"  Model Type: {ml_status.get('model_type', 'unknown')}")
            
            # Configuration
            config = data.get('configuration', {})
            print(f"\n⚙️  Configuration:")
            print(f"  Supabase URL Set: {'✅' if config.get('supabase_url_set') else '❌'}")
            print(f"  Supabase Key Set: {'✅' if config.get('supabase_key_set') else '❌'}")
            key_length = config.get('supabase_key_length', 0)
            print(f"  Key Length: {key_length} characters {'✅' if key_length > 100 else '⚠️ (Service role keys are typically 200+ chars)'}")
            
            if db_status.get('error'):
                print(f"\n❌ Database Error: {db_status.get('error')}")
                return False
            
            return True
        else:
            print(f"❌ Diagnostics endpoint returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        print(f"   Tried: {base_url}")
        return False
    except Exception as e:
        print(f"❌ Error testing diagnostics: {e}")
        return False


def test_health_endpoint(base_url="http://localhost:8000"):
    """Test the basic health endpoint."""
    print("\n" + "=" * 80)
    print("💚 Testing Health Endpoint")
    print("=" * 80)
    
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint is accessible")
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health: {e}")
        return False


def check_backend_logs_for_rls_verification():
    """Instructions to check backend logs."""
    print("\n" + "=" * 80)
    print("📋 Check Backend Logs")
    print("=" * 80)
    print("Look for these messages in your backend startup logs:")
    print("  ✅ 'Database connection established and verified'")
    print("  ✅ 'RLS bypass verified - service role key is working correctly'")
    print("\nIf you see RLS errors, check your .env file:")
    print("  - SUPABASE_KEY must be the SERVICE ROLE KEY (200+ chars)")
    print("  - Not the anon key!")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🚀 Early Warning System - Health Check")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    base_url = os.environ.get("API_URL", "http://localhost:8000")
    print(f"Testing backend at: {base_url}\n")
    
    results = []
    
    # Test health endpoint
    results.append(("Health Endpoint", test_health_endpoint(base_url)))
    
    # Test diagnostics endpoint
    results.append(("Diagnostics Endpoint", test_diagnostics_endpoint(base_url)))
    
    # Check logs instructions
    check_backend_logs_for_rls_verification()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Test Summary")
    print("=" * 80)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 All tests passed! System appears to be healthy.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("\nNext steps:")
        print("  1. Verify backend is running")
        print("  2. Check .env file has correct SUPABASE_KEY (service role key)")
        print("  3. Check backend logs for RLS verification messages")
        print("  4. Verify Supabase connection is working")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
