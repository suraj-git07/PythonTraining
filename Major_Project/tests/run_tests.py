"""
Test Runner for Customer and Restaurant Module System
"""

import unittest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.routes.test_routes import TestRoutes
from tests.services.test_services import TestServices


def run_all_tests():
    """Run all 11 essential customer tests"""
    
    print("="*60)
    print("RUNNING 11 ESSENTIAL CUSTOMER TESTS")
    print("="*60)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add UI tests (4 tests)
    suite.addTest(TestRoutes('test_1_view_restaurants_needs_auth'))
    suite.addTest(TestRoutes('test_2_view_restaurants_success'))
    suite.addTest(TestRoutes('test_3_add_to_cart'))
    suite.addTest(TestRoutes('test_4_place_order'))

    # Add new restaurant-related UI tests (3 tests)
    suite.addTest(TestRoutes('test_5_view_restaurant_detail'))
    suite.addTest(TestRoutes('test_6_view_order_history'))
    suite.addTest(TestRoutes('test_7_cancel_order'))

    # Add service tests (4 tests)  
    suite.addTest(TestServices('test_8_get_customer_id'))
    suite.addTest(TestServices('test_9_get_restaurant_list'))
    suite.addTest(TestServices('test_10_add_to_cart_service'))
    suite.addTest(TestServices('test_11_place_order_service'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Error:')[-1].strip()}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
