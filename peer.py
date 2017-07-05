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
        self.connected = False
        self.state = {
				'am_choking' : True,
				'am_interested' : False,
				'peer_choking' : True,
				'peer_interested' : False,
		}

    @coroutine
    def connect(self, message):
        self.message = message
        self.sock.setblocking(0)
        try:
            yield from self.io_loop.sock_connect(self.sock, (self.IP, self.port))
        except:
            print('Error while connecting to peer ', self.IP)
            return
        yield from self.io_loop.sock_sendall(self.sock, message)
        while len(self.buffer) < 68:
            try:
                message_bytes = yield from self.io_loop.sock_recv(self.sock, 4096)
            except:
                print('Error while receiving data from peer ', self.IP)
            if not message_bytes:
                raise Exception("Socket closed unexpectedly while receiving hanshake")
            self.buffer += message_bytes
        self.torrent_downloader.message_handler.check_handshake(self, self.buffer[:68])

    @coroutine
    def listen(self):
        ''' Listen for messages from socket
        '''
        while self.connected:
            self.dispatch_messages_from_buffer()
            message_bytes = yield from self.io_loop.sock_recv(self.sock, 4096)
            if not message_bytes:
                raise Exception("Socket closed unexpectedly while receiving message")
                # @warning close without brackets
                self.sock.close
                self.connected = False
                self.buffer += message_bytes

    def dispatch_messages_from_buffer(self):
        ''' First four bytes of each message are an indication of length.
            Wait until full message has been recieved and then send relevent
            bytes to dispatch_message. If length is 0000, message is "keep alive"
        '''
        while True:
            if len(self.buffer) >= 4:
                message_length = int.from_bytes(self.buffer[:4], byteorder='big')
                if message_length == 0:
                    print("{} - KEEP ALIVE".format(self.IP))
                    self.buffer = self.buffer[4:]
                elif len(self.buffer[4:]) >= message_length:
                    message = self.buffer[4:message_length+4]
                    self.torrent_downloader.message_handler.dispatch_message(self, message)
                    self.buffer = self.buffer[message_length+4:]
                else:
                    return self.buffer
            else:
                return self.buffer
