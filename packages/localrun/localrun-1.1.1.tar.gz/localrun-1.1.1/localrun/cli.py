# localrun/cli.py
import argparse
from localrun.server import run_server

def main():
    parser = argparse.ArgumentParser(description='Run a simple local server.')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host address to bind (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000,
                        help='Port number to bind (default: 8000)')
    parser.add_argument('--silent', action='store_true',
                        help='Run the server in silent mode (no output) and in background')
    
    args = parser.parse_args()
    
    running_address = run_server(args.host, args.port, args.silent)

    if not args.silent:
        print(f"Running port is: {running_address}")

if __name__ == '__main__':
    main()
