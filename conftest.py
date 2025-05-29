import pytest
import time
 

def pytest_addoption(parser):
    parser.addoption(
        "--correct", action="store_true", help="run tests on the correct version"
    )
    parser.addoption("--runslow", action="store_true", help="run slow tests")
    parser.addoption(
        "--fixed", action="store_true", help="run tests on the fixed version"
    )

def pytest_configure(config):
    pytest.use_correct = config.getoption("--correct")
    pytest.use_fixed = config.getoption("--fixed")
    pytest.run_slow = config.getoption("--runslow")
    pytest.fixed = config.getoption("--fixed")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    test_results = {}

    test_results['Passed'] = len(terminalreporter.stats.get('passed', []))
    test_results['Failed'] = len(terminalreporter.stats.get('failed', []))
    test_results['Skipped'] = len(terminalreporter.stats.get('skipped', []))
    test_results['Total'] = test_results['Passed'] + test_results['Failed'] + test_results['Skipped']

    print("Test Result:")
    for key in test_results:
        if key!= "Total":
            print(f"{key}: {test_results[key]}/{test_results["Total"]}")


