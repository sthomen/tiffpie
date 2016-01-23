# vim:ts=4:sw=4:

from exceptions import TiffDirectoryEntryException
from tags import TiffTags

class TiffRootDirectory(object):
	"""
	Models the IFD:s of the TIFF File. Also base class for the TiffDirectory class,
	this class generates dummy directory entries with linked subdirectories (entry.directory)
	for any append()ed directory.
	"""
	def __init__(self):
		self.entries=[]
		self.offset=0
		self.next=0

	def __iter__(self):
		for entry in self.entries:
			yield entry

		raise StopIteration

	def __str__(self):
		return '\n'.join([ str(e.directory) for e in self.entries ])

	def __len__(self):
		return len(self.entries)

	def append(self, directory):
		"""
		Append a TiffDirectory to the root entries, this method creates dummy TiffDirectoryEntry objects
		to hold the directory references.
		"""
		entry=TiffDirectoryEntry(self)
		entry.tag=0
		entry.directory=directory

		self.entries.append(entry)

	def find(self, tag):
		"""
		Recursively find a tag in discovered IFDs and subIFDs. Returns a tuple with all matches.
		"""
		results=()

		for entry in self.entries:
			if entry.directory:
				results+=entry.directory.find(tag)

			if entry.tag == tag:
				results+=(entry, )

		return results

class TiffDirectory(TiffRootDirectory):
	"""
	A direct model of the TIFF directory, requires an open BinaryReader file pointing to the same
	file as the parent Tiff object.
	"""
	def __init__(self, br, offset):
		super(TiffRootDirectory, self).__init__()

		self.entries=[]
		self.br=br
		self.offset=offset
		self.length=None

		self.read(offset)

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

class TiffDirectoryEntry(object):
	# XXX Tiff 3.0 types, 6.0 has more, but I don't need them yet
	BYTE=1
	ASCII=2
	SHORT=3
	LONG=4
	RATIONAL=5

	STRING=0
	LENGTH=1
	FORMAT=2

	types={
		BYTE:		('byte',	1, 's'),
		ASCII:		('ascii',	1, 's'),
		SHORT:		('short',	2, 'H'),
		LONG:		('long',	4, 'L'),
		RATIONAL:	('rational',8, 'LL')
	}

	def __init__(self, parent, br=None):
		self.parent=parent
		self.br=br
		self.tags=TiffTags()

		self.tag=None
		self.type=None
		self.count=None
		self.offset=None
		self.directory=None

		if br:
			self._load()

	def __repr__(self):
		return 'TiffDirectoryEntry(parent={}, tag={}, type={}, count={}, offset={})'.format(self.parent.offset,  self._tagstr(self.tag), self._typestr(self.type), self.count, self.offset)

	def __str__(self):
		return self.__repr__()

	def _typestr(self, type):
		if type in self.types:
			return self.types[type][self.STRING]

		return 'unknown'

	def _tagstr(self, tag):
		name=self.tags.getTagName(tag)
		if name:
			return name

		return hex(tag)

	def _load(self):
		self.tag=self.br.read()
		self.type=self.br.read()
		self.count=self.br.read(4, 'I')
		self.offset=self.br.read(4, 'I')

	def read(self):
		if not self.br:
			return None

# To save time and space the Value Offset contains the Value instead of pointing to
# the Value if and only if the Value fits into 4 bytes. If the Value is shorter than 4
# bytes, it is left-justified within the 4-byte Value Offset, i.e., stored in the lowernumbered
# bytes. Whether the Value fits within 4 bytes is determined by the Type
# and Count of the field.

		if self.types[self.type][self.LENGTH] * self.count <= 4:
			return self.offset

		self.br.seek(self.offset)

		if self.type in (TiffDirectoryEntry.BYTE, TiffDirectoryEntry.ASCII):
			return self.br.read(self.types[self.type][self.LENGTH], self.types[self.type][self.FORMAT], self.count)

		if self.type in (TiffDirectoryEntry.SHORT, TiffDirectoryEntry.LONG):
			return self.br.read(self.types[self.type][self.LENGTH], self.types[self.type][self.FORMAT], self.count, True)

		elif self.type==TiffDirectoryEntry.RATIONAL:
			values=()
			for i in range(0, self.count):
				numerator,denominator=self.br.read(self, 'LL', 1, True)

				values+=((numerator, denominator), )

			return values
