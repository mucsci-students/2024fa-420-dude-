import argparse
import subprocess
import sys

def run_gui():
    # Your GUI code goes here
    subprocess.run([sys.executable, 'GUI.py'])
def run_cli():
    # Your CLI code goes here
    subprocess.run([sys.executable, 'interface.py'])

def main():
    parser = argparse.ArgumentParser(description="Run the program in GUI or CLI mode.")
    parser.add_argument('--cli', action='store_true', help="Run the CLI version of the program.")

    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()

