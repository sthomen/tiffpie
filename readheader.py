#!/usr/bin/env python2.7
# vim:ts=4:sw=4:

import sys
from argparse import ArgumentParser

from tiff.tiff import Tiff

if __name__ == "__main__":
	parser = ArgumentParser(description='Read TIFF header fields from a file')
	parser.add_argument('filename', type=str, help='File to parse')
	parser.add_argument('tags', metavar='tag', nargs='*', help='Find a specific tag')

	args = parser.parse_args()

	with open(args.filename, 'rb') as fp:
		tiff=Tiff(fp)

		if args.tags:
			for tag in args.tags:
				for entry in tiff.directory.find(int(tag, 0)):
					print entry
					print entry.read()
		else:
			print tiff.directory
