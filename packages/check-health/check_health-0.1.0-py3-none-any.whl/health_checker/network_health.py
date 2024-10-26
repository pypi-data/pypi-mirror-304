import socket

from .health_checker import BaseHealthChecker


class NetworkHealth(BaseHealthChecker):
    def __init__(self, host: str, port: int, timeout: int = 5):
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout

    def ping(self):
        """Attempts to connect to the specified host and port to check availability."""
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout):
                return True
        except (socket.timeout, ConnectionRefusedError, socket.gaierror):
            return False

    def health_check_report(self):
        """Returns a dictionary with the host, port, and ping status."""
        return {
            "host": self.host,
            "port": self.port,
            "status": "reachable" if self.ping() else "unreachable"
        }
