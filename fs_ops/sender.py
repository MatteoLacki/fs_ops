from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import socket


def get_current_ip():
    return socket.gethostbyname(socket.gethostname())


class Sender(object):
    """A class used to simplify connections with the server."""
    def __init__(self,
                 ip_port, 
                 encoding="cp1251"):
        self.url = f"http://{ip_port}/"
        self.encoding = encoding
        self.connected = self.greet()

    def greet(self):
        request = Request(self.url)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        try:
            urlopen(request)
            return True
        except URLError as e:
            return False

    def __sock(self, route, message=None):
        request = Request(f"{self.url}/{route}")
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        if message is None:
            message = json.dumps(self.name).encode(self.encoding)
        return urlopen(request, message)

    def get_check_sum(self, path):
        """Get the check sum for the file on the server.

        Args:
            relative_file_path (str): relative file path, w.r.t. the folder things are copied into.
        Returns:
            str: requested check sum.
        """
        message = json.dumps(str(path)).encode(self.encoding)
        with self.__sock('check', message) as s:
            check_sum = json.loads(s.read())
        return check_sum
