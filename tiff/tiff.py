# vim:ts=4:sw=4:

from binaryreader import BinaryReader
from exceptions import TiffException
from dir import TiffRootDirectory, TiffDirectory, TiffDirectoryEntry

class Tiff(object):
	BYTEORDER={
		'<':	'little-endian',
		'>':	'big-endian'
	}

	def __init__(self, fp):
		self.fp=fp
		self.byteorder=None
		self.magic=None
		self.offset=None
		self.br=None
		self.directory=TiffRootDirectory()

		self.readHeader()			# sets self.offset
		self.readIFDs(self.offset)

	def readHeader(self):
		last=None
		for byte in self.fp.read(2):
			if last != None and byte != last:
				raise TiffException('Inconsistent TIFF byte order mark')

			if ord(byte)==0b1001101:	# MM, motorola, or big-endian
				bo='>'
			elif ord(byte)==0b1001001:	# II, intel, or little-endian
				bo='<'
			else:
				raise TiffException('Unknown byte order in file')

			self.byteorder=self.BYTEORDER[bo]

			last=byte

		self.br=BinaryReader(self.fp, bo)

		self.magic=self.br.read()

		if int(self.magic) != 42:
			raise TiffException('Invalid magic number')

		self.offset=self.br.read(4, 'I')

	def readIFDs(self, start):
		done=False

		while not done:
			td=TiffDirectory(self.br, start)

			self.directory.append(td)

			if not td.next:
				done=True

			start=td.next
