# roomconf-converter
Converter for room configurations in the AGraphML format to connection maps for deep learning.

# Installation & Requirements

Python 3 is required to run the converter.

Missing python packages can be installed with `pip`:

`pip3 install Pillow numpy`

# Usage

## Simple connection map

Convert an Agraphml to a simple connection map using room and edge types information only:

`python3 agraphml2connmap.py -f <agraphml_filename>`

You will get a PNG with an original file name and `.png` suffix as result.

## Zoned connection map

Convert an Agraphml to a zoned connection map using room, edge, and zone types information.

For this map type, it is required that each room provides a `zone` attribute and each edge provides `sourceZone` and `targetZone` attributes.

`python3 agraphml2connmap.py -f <agraphml_with_zones_filename> -z`

You will get a PNG with an original file name and `_ZONED.png` suffix as result.
