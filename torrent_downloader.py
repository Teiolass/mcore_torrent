from tracker import Tracker
from peer import Peer
from message_handler import MessageHandler
from asyncio import get_event_loop, coroutine


class Torrent_Downloader:
    def __init__(self, torrent):
        self.torrent = torrent
        self.tracker = Tracker(self.torrent.announce, self.torrent.get_params())
        self.peers = self.create_peers()
        self.message_handler = MessageHandler(self.torrent, self)
        self.io_loop = get_event_loop()


    def create_peers(self):
        peers = []
        for p in self.tracker.peer_list:
            if p[0] == self.torrent.ip:
                continue
            peers.append(Peer(p[0], p[1], self))
        return peers

    def pieces_changed_callback(self, peer):
        '''	Check if connected peer has pieces I need. Send interested message.
            Call choose_piece.
            If peer has no pieces I need, disconnect and remove from peers list.
        '''
        self.torrent.update_pieces_needed()
        for i in self.torrent.pieces_needed:
            if peer.has_pieces[i]:
                self.io_loop.create_task(self.message_handler.send_message(peer=peer, message_id=2))
                self.choose_piece(peer=peer)
                break
            else:
                self.peers.remove(peer)
