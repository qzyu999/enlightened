"""Simple test runner using unittest (no pytest required)."""
import sys
import unittest

# Add src to path
sys.path.insert(0, '.')

# Import test modules
from tests.test_card import TestSuit, TestRank, TestCard
from tests.test_deck import TestDeck
from tests.test_hand import TestHand


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSuit))
    suite.addTests(loader.loadTestsFromTestCase(TestRank))
    suite.addTests(loader.loadTestsFromTestCase(TestCard))
    suite.addTests(loader.loadTestsFromTestCase(TestDeck))
    suite.addTests(loader.loadTestsFromTestCase(TestHand))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("="*50)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
