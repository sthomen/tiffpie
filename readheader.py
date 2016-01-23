#!/usr/bin/env python2.7
# vim:ts=4:sw=4:

import sys
from argparse import ArgumentParser

from tiff.tiff import Tiff
from tiff.tags import TiffTags

if __name__ == "__main__":
	parser = ArgumentParser(description='Read TIFF header fields from a file')
	parser.add_argument('filename', nargs='?', type=str, help='File to parse')
	parser.add_argument('-i', dest='info', action='store_true', help='Show file info')
	parser.add_argument('-l', dest='list', action='store_true', help='List known tags')
	parser.add_argument('tags', metavar='tag', nargs='*', help='Find a specific tag')

	args = parser.parse_args()

	if args.list:
		tags=TiffTags.tags

		for tag in tags.keys():
			info=dict(zip(('tag', 'name'), (tag,) + tags[tag]))
			print "{tag:#10x}: {name}".format(**info)

		quit()

	if args.filename:
		with open(args.filename, 'rb') as fp:
			tiff=Tiff(fp)

			if args.info:
				print "Byte order: {}".format(tiff.byteorder)
				print "Magic number: {}".format(tiff.magic)
				print "First IFD offset: {}".format(tiff.offset)
				print "Linked IFD:s: {}".format(len(tiff.directory))

				quit()

			if args.tags:
				for tag in args.tags:
					for entry in tiff.directory.find(int(tag, 0)):
						print entry
						print entry.read()
			else:
				print tiff.directory
