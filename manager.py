from torrent import Torrent
from torrent_downloader import Torrent_Downloader
from asyncio import get_event_loop, coroutine
from traceback import print_exc


class Manager:
    def __init__(self, torrent_file):
        self.torrent = Torrent(torrent_file)
        self.torrent_downloader = Torrent_Downloader(self.torrent)
        self.loop = get_event_loop()
        self.start_loop = self.start_loop()

    def start_loop(self):
        self.loop.create_task(self.connect_peers())
        self.loop.run_forever()

    @coroutine
    def connect_peers(self):
        for peer in self.torrent_downloader.peers:
            peer.visualize('CONNECTING')
            self.loop.create_task(peer.connect(self.torrent_downloader.message_handler.handshake))
