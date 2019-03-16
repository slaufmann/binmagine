#!/usr/bin/env python3.7

# Copyright (C) 2018 Stefan Laufmann
#
# This file is part of binmagine.
#
# binmagine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# binmagine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with binmagine.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
from PIL import Image
from enum import Enum


# enum class for supported file types
class Filetype(Enum):
	BMP = "bmp"
	PNG = "png"
	JPEG = "jpeg"


class Options:
	"""
	Options that are read from the command line interface and control the behaviour of the program
	Attributes:
			input_file:		path to file that should be analysed
			output_file:	path to output file
			filetype:		type of the output file
			height:			height of the resulting image
			width:			width of the resulting image
			samples:		number of samples that should be analysed from input file
	"""
	def __init__(self, input_file, output_file, height, width, samples):
		self.input_file = input_file
		self.output_file = output_file
		self.filetype = self.type_from_filename(output_file)
		self.height = height
		self.width = width
		self.samples = samples

	# derive type of file from file extension
	@staticmethod
	def type_from_filename(filename):
		extensions = {
			"bmp": Filetype.BMP,
			"png": Filetype.PNG,
			"jpg": Filetype.JPEG,
			"jpeg": Filetype.JPEG
		}
		_, file_extension = os.path.splitext(filename)
		file_extension = file_extension.strip('.')  # remove leading '.'
		try:
			filetype = extensions[file_extension]
		except KeyError:
			print("Error: Name of output file has no supported file extension, exiting.")
			exit()
		else:
			return filetype


# parse command line arguments
def parse_cli_args():
	"""
	parse_cli_args parses command line arguments and returns Options object containing the given or default values.

	NOTE:	In this function no sanity checks are performed on the argument values. See process_options for that.
	"""
	# create parser and add arguments
	parser = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("file",
							help="path to the file that should be analysed (file is read as binary data)")
	parser.add_argument("--width", type=int, default=512,
							help="width of the resulting image")
	parser.add_argument("--height", type=int, default=0,
							help="height of the resulting image (this may lead to not reading all samples)")
	parser.add_argument("-s", "--samples", type=int, default=0,
							help="number of samples that should be taken from the file (takes precedence over dimension parameters)")
	parser.add_argument("-o", "--output", default="out.png",
							help="path to output file (file ending determines file type, supported: bmp, jpg, png)")
	# parse the arguments and create Options object
	args = parser.parse_args()
	options = Options(args.file, args.output, int(args.height), int(args.width), int(args.samples))

	return options


# process options and identify conflicts
def process_options(options):
	"""
	process_options checks the values that were parsed from the command line interface
	to identify conflicts or calculate missing values.

	NOTE:	Since the number of samples to process and the requested dimensions of the resulting image
			can be conflicting the minimum of both values is chosen.
	"""
	# get size of the file
	file_size = os.stat(options.input_file).st_size
	# if no height given, calculate from file size and width
	if not options.height:
		options.height = int(file_size/options.width)
	# if number of samples not given, calculate from requested output image dimensions
	if not options.samples:
		options.samples = options.height * options.width
	else:
		options.height = int(min(options.height, (options.samples/options.width)))

	# exit if not enough data for one line inside the image
	if options.height == 0:
		print("Error: File contains not enough samples for at least one line of chosen width, exiting.")
		exit()


# read file data and build result image
def process_image(input_file, options):
	"""
	process_image creates an image with the dimensions given by the options object. It then
	reads data from the given input file as binary values and build an grayscale image from
	this data.

	NOTE:	The maximum number of bytes read is specified by the samples attribute of the
			options object OR if smaller by the image dimensions.
	"""
	result_image = Image.new("RGB", (options.width, options.height), "black")
	pixels = result_image.load()  # load the pixels to be able to change their values

	# read lines from the file and set color of pixels
	total_bytes_read = 0
	x = y = 0 	# pixel coordinates
	for line in input_file:
		bin_data = bytearray(line)
		for byte in bin_data:
			pixels[x, y] = byte_to_grayvalue(byte)
			total_bytes_read += 1
			x += 1
			if x == options.width:  # if we reached maximum of x (width of image) increment y
				x = 0
				y += 1
			if total_bytes_read == options.samples:  # return result if we reached specified sample count
				return result_image
	return result_image


# convert binary data to grayscale color value
def byte_to_grayvalue(byte):
	return (byte, byte, byte)


# main "function"
if __name__ == "__main__":
	options = parse_cli_args()
	process_options(options)

	print("Reading {} samples resulting in an image of {} lines with {} pixels".format(options.samples,
																					   options.height,
																					   options.width))
	input_file = open(options.input_file, "rb")
	result_image = process_image(input_file, options)

	input_file.close()
	result_image.save(options.output_file, options.filetype.value)
	print("Finished processing.")
