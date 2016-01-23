# vim:ts=4:sw=4:

import os
from struct import unpack

class BinaryReader(object):
	"""
	Perform binary reads at a given byte order
	Note: while this object is like a file, it is not File Like(tm)
	"""
	def __init__(self, fp, bo='@'):
		if type(fp) == file:
			self.fp=fp
		else:
			self.fp=open(fp, 'rb')

		self._byteorder=bo

	def tell(self):
		return self.fp.tell()

	def seek(self, position, offset=os.SEEK_SET):
		return self.fp.seek(position, offset)

	def close(self):
		self.fp.close()

	def byteorder(self, new=None):
		bo=self._byteorder

		if new:
			self._byteorder=new

		return bo

	def read(self, bc=2, fmt='H', count=1, all=False):
		data=self.fp.read(bc * count)
		if not data:
			return None

		unpacked=self.unpack(fmt, count, data)

		if all:
			return unpacked

		return unpacked[0]

	def unpack(self, fmt, count, data):
		return unpack("{}{}{}".format(self.byteorder(), count, fmt), data)
