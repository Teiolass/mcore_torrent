from tracker import Tracker
from peer import Peer


class Torrent_Downloader:
    def __init__(self, torrent):
        self.torrent = torrent
        self.tracker = Tracker(self.torrent.announce, self.torrent.get_params())
        self.peers = self.create_peers()

    def create_peers(self):
        peers = []
        for p in self.tracker.peer_list:
            if p[0] == self.torrent.ip:
                continue
            peers.append(Peer(p[0], p[1], self))
        return peers
