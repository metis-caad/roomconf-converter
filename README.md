# roomconf-converter
Converts architectural spatial configurations in the AGraphML format to tensor-based connection maps for deep learning.

The converter is published in the context of the paper ["Exploring optimal ways to represent topological and spatial features of building designs in deep learning methods and applications for architecture"](http://papers.cumincad.org/cgi-bin/works/paper/caadria2021_086) submitted and presented @ [CAADRIA 2021](https://caadria2021.org/).

The research is part of the [metis-II](https://www.ar.tum.de/en/ai/research/artificial-intelligence/ksd-research-group/funded-projects/) project by DFKI and TUM.

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

## Multilayer connection map

Convert an Agraphml to a multilayer connection map with source, target, and connection type layers.

`python3 agraphml2multilayer.py -f <agraphml_filename>`

You will get a text file with an original file name and `_multilayer.connmap` suffix as result.

## One-hot encoded connection map

Convert an Agraphml to a connection map in the form of one-hot vector triples for source, target, and connection type.

`python3 agraphml2onehot.py -f <agraphml_filename>`

You will get a JSON file with an original file name and `_onehot.json` suffix as result.

## Textual connection map

Convert an Agraphml to a connection map in the form of textual expressions for source, target, and connection type.

`python3 agraphml2textualmap.py -f <agraphml_filename>`

You will get a JSON file with an original file name and `_onehot.json` suffix as result.

## Connection map as a sequence

Convert an Agraphml to a connection map and then to a comma-separated sequence. Only existing (non-zero) conections will be available in the sequence.

`python3 agraphml2sequence.py -f <agraphml_filename>`

You will get a TXT with an original file name and `_SEQ.txt` suffix as result.
