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

# define command line options
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
parser.add_argument("-o", "--output", default="out.bmp", 
						help="path to output file (file ending does NOT determine file type)")
# parse the arguments and react
args = parser.parse_args()
# get size of the file
fSize = os.stat(args.file).st_size
width = args.width
if (not args.height):
	lines = fSize/width
else:
	lines = args.height
if (args.samples):
	samples = args.samples
	lines = min(lines,(samples/width))
else:
	samples = lines*width

if lines == 0:
	print("file contains not enough samples for at least one line of chosen width {}".format(width))
	exit()
	
# start processing	
print("reading {} samples resulting in an image of {} lines with {} pixels".format(samples, lines, width))
f = open(args.file, "rb")
line = 0
lines = int(lines)
img = Image.new("RGB", (width,lines), "black")
pix = img.load()	# load the pixels to be able to change their values
data = f.read(width)	# read first line of data from file
while (data != "") and (line < lines):
	binData = bytearray(data)
	for i in range(width):
		val = binData[i]
		pix[i,line] = (val, val, val)
	line +=1
	data = f.read(width)

# finished processing, cleaning up	
f.close()
img.save(args.output)
