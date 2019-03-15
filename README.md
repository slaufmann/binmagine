# binmagine

I know that there are a lot of programs like this out there. But during my master thesis i needed a way to turn binary data into grayscale pixel images and decided to implement it myself to suit my specific needs.


## Functionality

This python program takes a given file and reads it as binary data.
Every byte of data that is read from the file is converted into a value between 0 and 255 to represent the grayscale value.
Byte by byte the given file is read and a grayscale pixel image is produced and later saved to disk.

How many data from the file is read can be controlled as well as the dimensions of the resulting image.
See [Usage](#usage) for details.


## Usage

To run this program, python 3.7 is required.
Running `python3.7 binmagine -h` will produce the following output that explains the options of the command line interface:
```
usage: binmagine.py [-h] [--width WIDTH] [--height HEIGHT] [-s SAMPLES]
                    [-o OUTPUT]
                    file

positional arguments:
  file                  path to the file that should be analysed (file is read
                        as binary data)

optional arguments:
  -h, --help            show this help message and exit
  --width WIDTH         width of the resulting image (default: 512)
  --height HEIGHT       height of the resulting image (this may lead to not
                        reading all samples) (default: 0)
  -s SAMPLES, --samples SAMPLES
                        number of samples that should be taken from the file
                        (takes precedence over dimension parameters) (default:
                        0)
  -o OUTPUT, --output OUTPUT
                        path to output file (file ending does NOT determine
                        file type) (default: out.bmp)
```
