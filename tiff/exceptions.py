# vim:ts=4:sw=4:

class TiffException(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return "TiffDirectoryEntryException({})".format(self.message)
		
class TiffDirectoryEntryException(TiffException):
	def __init__(self, message):
		super(TiffDirectoryEntryException, self).__init__(message)
