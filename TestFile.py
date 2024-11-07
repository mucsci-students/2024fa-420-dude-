import argparse
import subprocess
import sys
import os

def run_tests():
    # Define paths to the test files
    model_test_path = os.path.join('Model', 'DBFunctionsTestFile.py')
    control_test_path = os.path.join('Control', 'UtilFunctionsTestFile.py')
    
    # Run each test file with pytest
    print("Running DBFunctions tests...")
    #subprocess.run([sys.executable, '-m', 'pytest', model_test_path])
    #pytest --cov=Model.DBFunctions --cov-report=term-missing DBFunctionsTestFile.py
    subprocess.run([sys.executable, '-m', 'pytest',
        '--cov=Model.DBFunctions', 
        '--cov-report=term-missing', 
        model_test_path,
        control_test_path
    ])

    
    print("Running Utility Functions tests...")
    subprocess.run([sys.executable, '-m', 'pytest', control_test_path])

def main():
    parser = argparse.ArgumentParser(description="Run tests for Model and Control folders.")
    parser.add_argument('--test', action='store_true', help="Run tests for DBFunctions and Utility Functions.")
    
    args = parser.parse_args()

    if args.test:
        run_tests()
    else:
        print("No action specified. Use --test to run tests.")

if __name__ == "__main__":
    main()
