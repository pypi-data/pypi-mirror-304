# localrun/cli.py
import time

def print_startup_message(host, port):
    print(f'Serving HTTP on {host}:{port}...')
    time.sleep(1)  

def print_server_stopped_message():
    print("Server stopped.")

def print_running_address(running_address):
    print(f"Running port is: {running_address}")

def print_log_message(log_time, request_info):
    print(f"localrun - - [{log_time}] {request_info}")
