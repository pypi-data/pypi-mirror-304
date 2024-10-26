import argparse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from localrun.cli import print_startup_message, print_server_stopped_message, print_running_address, print_log_message
import time

class LoggingHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.silent = kwargs.pop('silent', False)
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        log_time = self.log_date_time_string()
        request_info = format % args
        print_log_message(log_time, request_info)

def run_server(host='127.0.0.1', port=8000, silent=False):
    server_address = (host, port)
    httpd = HTTPServer(server_address, 
                       lambda *args, **kwargs: LoggingHTTPRequestHandler(*args, silent=silent, **kwargs))
    
    if not silent:
        print_startup_message(host, port)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        if not silent:
            print_server_stopped_message()
    
    return f'{host}:{port}'

def main():
    parser = argparse.ArgumentParser(description='Run a simple local server.')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host address to bind (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000,
                        help='Port number to bind (default: 8000)')
    parser.add_argument('--silent', action='store_true',
                        help='Run the server in silent mode (no output)')
    
    args = parser.parse_args()
    
    running_address = run_server(args.host, args.port, args.silent)
    if not args.silent:
        print_running_address(running_address)

if __name__ == '__main__':
    main()
