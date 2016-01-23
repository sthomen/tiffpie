# vim:ts=4:sw=4:
# These are mostly for the nikon electronic file format, because that was what I was interested in
# taken from http://lclevy.free.fr/nef/index.html

class TiffTags(object):
	tags={
		0x0000fe: ('NewSubfileType', 'Bit field: Bit 0 = reduced-resolution, Bit 1 = single page of multi-page image, Bit 2 = transparency mask for another image'),
		0x000100: ('ImageWidth', ),
		0x000101: ('ImageHeight', ),
		0x000101: ('ImageHeight', ),
		0x000102: ('BitsPerSample', '[ 8, 8, 8 ]'),
		0x000103: ('Compression', '1=uncompressed,  6=old/jpeg, 34713=NEF Compressed'),
		0x000106: ('PhotometricInterpretation', '32803=Color Filter Array'),
		0x00010e: ('ImageDescription', ),
		0x00010f: ('Make', ),
		0x000110: ('Model', ),
		0x000111: ('JpgFromRawStart', 'offset to the image data'),
		0x000115: ('SamplesPerPixel', ),
		0x000116: ('RowsPerStrip', ),
		0x000117: ('JpgFromRawLength', 'image data lenght'),
		0x00011a: ('XResolution', ),
		0x00011b: ('YResolution', ),
		0x00011c: ('PlanarConfiguration', '1 = Chunky'),
		0x000128: ('ResolutionUnit', '2=pixel_per_inch'),
		0x000132: ('DateTime', 'Date and time of image creation'),
		0x00013b: ('Artist', ),
		0x00014a: ('SubIFD', '[ JpegImageOffset, RawOffset ] : offsets to the 2 child IFDs'),
		0x000201: ('JpgFromRawStart', 'Offset to image data'),
		0x000202: ('JpgFromRawLength', 'Image data length'),
		0x000213: ('YCbCrPositioning', '2=co_sited'),

# private tags below, higher than 0x8000

		0x008298: ('Copyright', 'Copyright notice'),
		0x009003: ('DateTimeOriginal', 'The date and time when the original image data was generated'),

# these have suspiciously large tag numbers

		0x021465: ('ReferenceBlackWhite', ),
		0x828d21: ('CFARepeatPatternDim', '(2, 2) = 2x2'),
		0x828e22: ('CFAPattern2', '(1, 2, 0, 1) = (G, B, R, G) for the D60'),
		0x876965: ('EXIF', 'Offset to the EXIF IFD'),
		0x921799: ('SensingMethod', '2 = One-chip color area (D60)'),
		0x928610: ('UserComment', )
	}

	def getTag(self, tag):
		if tag in self.tags:
			return self.tags[tag]
		
		return None

	def getTagName(self, tag):
		if tag in self.tags:
			return self.tags[tag][0]

		return None

	def getTagDescription(self, tag):
		if len(self.tags[tag]) == 2:
			return self.tags[tag][1]

		return None
