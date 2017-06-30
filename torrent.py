from bencoding import decode as bdecode
from hashlib import sha1
from json import loads
from random import randrange
from requests import get
from math import ceil


class Torrent():
	''' Contains all torrent meta info.

	'''
	def __init__(self, torrent_file):
		with open(torrent_file, 'rb') as f:
			self.torrent_file = f.read()
		self.meta_info_dict = bdecode(self.torrent_file)
		self.announce = self.meta_info_dict[b'announce'].decode('utf-8')
		self.info_dict = self.meta_info_dict[b'info']
		self.bencoded_info_dict = self.info_dict['ben_string']
		self.filename = self.info_dict[b'name'].decode('utf-8')
		self.path = 'torrents_in_progress'
		self.info_hash = sha1(self.bencoded_info_dict).digest()
		self.peer_id = '-'.join(['','TZ', '0000', str(randrange(10000000000,99999999999))])
		self.ip = self.get_IP_address()
		self.port =  '6881' #TODO: Try ports in range (6881,6889)
		self.length = int(self.info_dict[b'length']) if b'length' in self.info_dict \
				else sum([int((f[b'length'])) for f in self.info_dict[b'files']])
		self.piece_length = int(self.info_dict[b'piece length'])
		self.pieces = self.info_dict[b'pieces']
		self.piece_hashes = [self.pieces[i:i+20] for i in range(0, len(self.pieces), 20)]
		self.number_of_pieces = ceil(self.length/self.piece_length)
		self.downloaded = 0
		self.uploaded = 0
		self.have = [False] * self.number_of_pieces #TODO: pass torrent class a bitfield and handle restarting torrents
		self.complete = False #TODO: Update when self.pieces_needed is empty
		self.pieces_needed = []

	def get_IP_address(self):
		response = get('http://api.ipify.org?format=json')
		ip_object = loads(response.text)
		return ip_object["ip"]

t = Torrent('deb/ubuntu.torrent')
print(t.announce)
print(t.filename)
