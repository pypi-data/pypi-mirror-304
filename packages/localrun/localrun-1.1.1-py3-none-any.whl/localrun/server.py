# localrun/server.py
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer
import datetime

class LoggingHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.silent = kwargs.pop('silent', False)
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        if not self.silent:
            log_time = self.log_date_time_string()
            request_info = format % args
            print(f"localrun - - [{log_time}] {request_info}")

    def log_date_time_string(self):
        return datetime.datetime.now().strftime('%d/%b/%Y %H:%M:%S')

def run_server(host='127.0.0.1', port=8000, silent=False):
    server_address = (host, port)
    httpd = HTTPServer(server_address, 
                       lambda *args, **kwargs: LoggingHTTPRequestHandler(*args, silent=silent, **kwargs))

    if silent:
        subprocess.Popen(
            ['python', '-m', 'http.server', str(port), '--bind', host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return f'{host}:{port} (running in background)'

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

    return f'{host}:{port}'
