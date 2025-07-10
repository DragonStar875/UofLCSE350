import threading
import time
import socket
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pywebio import start_server
import smartShelf


def is_port_open(host, port):
    """Check if the port is open (i.e., server is running)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def test_pantry_main_server_starts():
    # Use lambda to wrap start_server call to prevent argument unpacking issues
    server_thread = threading.Thread(
        target=lambda: start_server(smartShelf.pantry_main, port=8080, open_browser=False),
        daemon=True
    )
    server_thread.start()

    time.sleep(5.0)

    assert is_port_open("localhost", 8080), "Server failed to start on port 8080"
