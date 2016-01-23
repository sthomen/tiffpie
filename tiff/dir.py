# vim:ts=4:sw=4:

from exceptions import TiffDirectoryEntryException
from tags import TiffTags

class TiffDirectory(object):
	def __init__(self, br, offset):
		self.entries=[]

		self.br=br
		self.offset=offset
		self.length=None
		self.next=None

		if self.br:
			self.read(offset)

	def __iter__(self):
		for entry in self.entries:
			yield entry

		raise StopIteration

	def __str__(self):
		return '\n'.join([str(e) for e in self.entries + [ 'Next index: {}'.format(self.next) ]])

	def append(self, entry):
		self.entries.append(entry)

	def read(self, offset):
		self.br.seek(offset)
		self.length=self.br.read()

		for i in range(0, self.length):
			de=TiffDirectoryEntry(self, self.br)

			if de.tag == 0x14a:				# Sub IFD
				position=self.br.tell()

				for offset in de.read():
					de.directory=TiffDirectory(self.br, offset)

				self.br.seek(position)

			self.entries.append(de)

		self.next=self.br.read(4, 'I')

	def find(self, tag):
		results=()

		for entry in self.entries:
			if entry.directory:
				res=entry.directory.find(tag)
				if res:
					results+=res

			if entry.tag == tag:
				results+=(entry, )

		return results

class TiffDirectoryEntry(object):
	# XXX Tiff 3.0 types, 6.0 has more, but I don't need them yet
	BYTE=1
	ASCII=2
	SHORT=3
	LONG=4
	RATIONAL=5

	types={
		BYTE:		'byte',
		ASCII:		'ascii',
		SHORT:		'short',
		LONG:		'long',
		RATIONAL:	'rational'
	}

	def __init__(self, parent, br):
		self.parent=parent
		self.br=br
		self.tags=TiffTags()

		self.tag=self.br.read()
		self.type=self.br.read()
		self.count=self.br.read(4, 'I')
		self.offset=self.br.read(4, 'I')
		self.directory=None

	def __repr__(self):
		return 'TiffDirectoryEntry(parent={}, tag={}, type={}, count={}, offset={})'.format(self.parent.offset,  self._tagstr(self.tag), self._typestr(self.type), self.count, self.offset)

	def __str__(self):
		return self.__repr__()

	def _typestr(self, type):
		if type in self.types:
			return self.types[type]

		return 'unknown'

	def _tagstr(self, tag):
		name=self.tags.getTagName(tag)
		if name:
			return name

		return hex(tag)

	def read(self):
		self.br.seek(self.offset)

		if self.type==TiffDirectoryEntry.BYTE:
			return self.br.read(1, 'H', self.count)

		if self.type==TiffDirectoryEntry.SHORT:
			return self.br.read(2, 'H', self.count, True)

		elif self.type==TiffDirectoryEntry.LONG:
			return self.br.read(4, 'L', self.count, True)

		elif self.type==TiffDirectoryEntry.ASCII:
			return self.br.read(1, 's', self.count)

		elif self.type==TiffDirectoryEntry.RATIONAL:
			values=()
			for i in range(0, self.count):
				numerator,denominator=self.br.read(8, 'LL', 1, True)

				values+=((numerator, denominator), )

			return values
