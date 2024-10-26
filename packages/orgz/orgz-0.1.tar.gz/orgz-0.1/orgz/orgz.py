import argparse
import subprocess

def orgz():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Execute backend commands")
    parser.add_argument('command', choices=['start', 'stop', 'restart'], help="Command to execute")

    # Parse arguments from the command line
    args = parser.parse_args()

    # Map user commands to backend commands
    command_map = {
        'start': 'gs_om -t start',
        'stop': 'gs_om -t stop',
        'restart': 'gs_om -t restart'
    }

    # Execute the mapped command
    backend_command = command_map[args.command]
    try:
        subprocess.run(backend_command, shell=True, check=True)
        print(f"Successfully executed: {backend_command}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")

def main():
    orgz()

