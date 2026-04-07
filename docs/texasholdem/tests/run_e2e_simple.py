"""Simple E2E test runner without pytest dependency."""

import sys
import traceback
from types import FunctionType

sys.path.insert(0, '/workspace')

def run_test(test_func):
    """Run a single test function."""
    try:
        test_func()
        return True, None
    except AssertionError as e:
        return False, str(e)
    except Exception as e:
        return False, f"{type(e).__name__}: {e}\n{traceback.format_exc()}"

def run_tests_from_module(module, class_name):
    """Run all test methods from a test class."""
    test_class = getattr(module, class_name)
    instance = test_class()
    
    results = []
    for name in dir(instance):
        if name.startswith('test_'):
            method = getattr(instance, name)
            if callable(method):
                success, error = run_test(method)
                results.append((name, success, error))
    
    return results

def main():
    print("=" * 60)
    print("Texas Hold'em E2E Test Suite (Simple Runner)")
    print("=" * 60)
    print()
    
    # Import test modules
    from tests.e2e import test_complete_games
    
    all_results = []
    
    # Run TestCompleteGameFlow
    print("Running TestCompleteGameFlow...")
    results = run_tests_from_module(test_complete_games, 'TestCompleteGameFlow')
    all_results.extend(results)
    for name, success, error in results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")
        if error:
            print(f"    Error: {error[:100]}...")
    print()
    
    # Run TestHandScenarios
    print("Running TestHandScenarios...")
    results = run_tests_from_module(test_complete_games, 'TestHandScenarios')
    all_results.extend(results)
    for name, success, error in results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")
        if error:
            print(f"    Error: {error[:100]}...")
    print()
    
    # Run TestEdgeCases
    print("Running TestEdgeCases...")
    results = run_tests_from_module(test_complete_games, 'TestEdgeCases')
    all_results.extend(results)
    for name, success, error in results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")
        if error:
            print(f"    Error: {error[:100]}...")
    print()
    
    # Summary
    passed = sum(1 for _, success, _ in all_results if success)
    failed = len(all_results) - passed
    
    print("=" * 60)
    print(f"Results: {passed}/{len(all_results)} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
