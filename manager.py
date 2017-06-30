from torrent import Torrent
from torrent_downloader import Torrent_Downloader

class Manager:
    def __init__(self, torrent_file):
        self.torrent = Torrent(torrent_file)
        self.torrent_downloader = Torrent_Downloader(self.torrent)

m = Manager('deb/ubuntu.torrent')
print(m.torrent_downloader.peers)
