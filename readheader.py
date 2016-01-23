#!/usr/bin/env python2.7
# vim:ts=4:sw=4:

import sys

from tiff.tiff import Tiff
from tiff.dir import TiffDirectory

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: {} <filename> [ <tag> ]".format(sys.argv[0])
		quit()

	with open(sys.argv[1], "rb") as fp:
		tiff=Tiff(fp)

		if len(sys.argv) > 2:
			for entry in tiff.find(int(sys.argv[2], 0)):
				print entry
				print entry.read()
		else:
			for directory in tiff.directory:
				print directory
