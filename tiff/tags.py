# vim:ts=4:sw=4:

class TiffTags(object):
	tags={
# Tags from the TIFF 6.0 standards document
# http://partners.adobe.com/public/developer/en/tiff/TIFF6.pdf
		0x00FE: ('NewSubfileType', ),
		0x00FF: ('SubfileType', ),
		0x0100: ('ImageWidth', ),
		0x0101: ('ImageLength', ),
		0x0102: ('BitsPerSample', 'SamplesPerPixel'),
		0x0103: ('Compression', 'Uncompressed = 1 CCITT 1D = 2 Group = 3 = Fax = 3 Group = 4 = Fax = 4 LZW = 5 JPEG = 6 PackBits = 3277'),
		0x0106: ('PhotometricInterpretation', 'WhiteIsZero = 0 BlackIsZero = 1 RGB = 2 RGB Palette = 3 Transparency mask = 4 CMYK = 5 YCbCr = 6 CIELab = 8'),
		0x0107: ('Threshholding', ),
		0x0108: ('CellWidth', ),
		0x0109: ('CellLength', ),
		0x010A: ('FillOrder', ),
		0x010D: ('DocumentName', ),
		0x010E: ('ImageDescription', ),
		0x010F: ('Make', ),
		0x0110: ('Model', ),
		0x0111: ('StripOffsets', 'StripsPerImage'),
		0x0112: ('Orientation', ),
		0x0115: ('SamplesPerPixel', ),
		0x0116: ('RowsPerStrip', ),
		0x0117: ('StripByteCounts', 'StripsPerImage'),
		0x0118: ('MinSampleValue', 'SamplesPerPixel'),
		0x0119: ('MaxSampleValue', 'SamplesPerPixel'),
		0x011A: ('XResolution', ),
		0x011B: ('YResolution', ),
		0x011C: ('PlanarConfiguration', ),
		0x011D: ('PageName', ),
		0x011E: ('XPosition', ),
		0x011F: ('YPosition', ),
		0x0120: ('FreeOffsets', ),
		0x0121: ('FreeByteCounts', ),
		0x0122: ('GrayResponseUnit', ),
		0x0123: ('GrayResponseCurve', '2**BitsPerSample'),
		0x0124: ('T4Options', ),
		0x0125: ('T6Options', ),
		0x0128: ('ResolutionUnit', ),
		0x0129: ('PageNumber', ),
		0x012D: ('TransferFunction', '{1 or SamplesPerPixel}*2**BitsPerSample'),
		0x0131: ('Software', ),
		0x0132: ('DateTime', ),
		0x013B: ('Artist', ),
		0x013C: ('HostComputer', ),
		0x013D: ('Predictor', ),
		0x013E: ('WhitePoint', ),
		0x013F: ('PrimaryChromaticities', ),
		0x0140: ('ColorMap', '3*(2**BitsPerSample)'),
		0x0141: ('HalftoneHints', ),
		0x0142: ('TileWidth', ),
		0x0143: ('TileLength', ),
		0x0144: ('TileOffsets', 'TilesPerImage'),
		0x0145: ('TileByteCounts', 'TilesPerImage'),
		0x014C: ('InkSet', ),
		0x014D: ('InkNames', 'Total number of characters in all ink name strings, including zeros'),
		0x014E: ('NumberOfInks', ),
		0x0150: ('DotRange', '2 or 2*NumberOfInks'),
		0x0151: ('TargetPrinter', ),
		0x0152: ('ExtraSamples', 'Number of extra components per pixel'),
		0x0153: ('SampleFormat', 'SamplesPerPixel'),
		0x0154: ('SMinSampleValue', 'SamplesPerPixel'),
		0x0155: ('SMaxSampleValue', 'SamplesPerPixel'),
		0x0156: ('TransferRange', ),
		0x0200: ('JPEGProc', ),
		0x0201: ('JPEGInterchangeFormat', ),
		0x0202: ('JPEGInterchangeFormatLngth', ),
		0x0203: ('JPEGRestartInterval', ),
		0x0205: ('JPEGLosslessPredictors', 'SamplesPerPixel'),
		0x0206: ('JPEGPointTransforms', 'SamplesPerPixel'),
		0x0207: ('JPEGQTables', 'SamplesPerPixel'),
		0x0208: ('JPEGDCTables', 'SamplesPerPixel'),
		0x0209: ('JPEGACTables', 'SamplesPerPixel'),
		0x0211: ('YCbCrCoefficients', ),
		0x0212: ('YCbCrSubSampling', ),
		0x0213: ('YCbCrPositioning', ),
		0x0214: ('ReferenceBlackWhite', '2*SamplesPerPixel'),
		0x8298: ('Copyright', ),

# These are for the nikon electronic file format
# taken from http://lclevy.free.fr/nef/index.html

		0x9003: ('DateTimeOriginal', 'The date and time when the original image data was generated'),
		0x21465: ('ReferenceBlackWhite', ),
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
