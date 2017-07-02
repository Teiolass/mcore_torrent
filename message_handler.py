class MessageHandler():
  def __init__(self, torrent, torrent_downloader):
    self.torrent = torrent
    self.torrent_downloader = torrent_downloader
    self.handshake = self.handshake()

  def handshake(self):
    ''' construct handshake bytestring in form:
      <19><'BitTorrent protocol'><00000000><ID>
      Spec here: https://wiki.theory.org/BitTorrentSpecification#Handshake
    '''
    pstrlen = b'\x13'
    pstr = b'BitTorrent protocol'
    reserved = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    parts = [pstrlen, pstr, reserved, self.torrent.info_hash, self.torrent.peer_id.encode()]
    handshake_string = b''.join(parts)
    return handshake_string
