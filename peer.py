class Peer:
    def __init__(self, ip, port, torrent_downloader):
        self.IP = ip
        self.port = port
        self.torrent_downloader = torrent_downloader
        self.torrent = torrent_downloader.torrent
