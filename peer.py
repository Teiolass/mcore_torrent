import socket
from asyncio import get_event_loop, coroutine

class Peer:
    def __init__(self, ip, port, torrent_downloader):
        self.IP = ip
        self.port = port
        self.torrent_downloader = torrent_downloader
        self.torrent = torrent_downloader.torrent
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = b''
        self.io_loop = get_event_loop()

    @coroutine
    def connect(self, message):
        self.message = message
        self.sock.setblocking(0)
        yield from self.io_loop.sock_connect(self.sock, (self.IP, self.port))
        yield from self.io_loop.sock_sendall(self.sock, message)
        while len(self.buffer) < 68:
            message_bytes = yield from self.io_loop.sock_recv(self.sock, 4096)
            if not message_bytes:
                raise Exception("Socket closed unexpectedly while receiving hanshake")
            self.buffer += message_bytes
        # self.torrent_downloader.message_handler.check_handshake(self, self.buffer[:68])
        print(self.buffer)
