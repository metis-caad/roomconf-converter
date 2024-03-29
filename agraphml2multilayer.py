import hashlib
import json
import os
import sys
import xml.etree.ElementTree as eT
from argparse import ArgumentParser
from json import JSONEncoder

import numpy as np

parser = ArgumentParser()
parser.add_argument('-f', '--filename', dest='filename', required=True)
args = parser.parse_args()


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def get_room_type(room_id, _graph):
    for room in _graph.findall(namespace + 'node'):
        if room_id == room.get('id'):
            data = room.findall(namespace + 'data')
            for d in data:
                if d.get('key') == 'roomType':
                    return d.text.encode('utf-8')


namespace = '{http://graphml.graphdrawing.org/xmlns}'
dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
filename = args.filename
full_filename = dirname + '/' + filename
tree = eT.parse(full_filename)
root = tree.getroot()
graph = root[0]

room_ids = [room.get('id') for room in graph.findall(namespace + 'node')]

length = 20  # len(room_ids)
connmap = []
for i in range(length):
    id_from = ''
    try:
        id_from = room_ids[i]
    except IndexError:
        pass
    for j in range(length):
        # initialize with 'no connection'
        connection = [0.0, 0.0, 0.0]
        id_to = ''
        try:
            id_to = room_ids[j]
        except IndexError:
            pass
        if id_from != id_to:
            for edge in graph.findall(namespace + 'edge'):
                source_id = edge.get('source')
                target_id = edge.get('target')
                if id_from == source_id and id_to == target_id:
                    source_number_code = int(hashlib.md5(get_room_type(room_ids[i], graph)).hexdigest(), 16)
                    target_number_code = int(hashlib.md5(get_room_type(target_id, graph)).hexdigest(), 16)
                    edge_number_code = int(hashlib.md5(
                        edge.find(namespace + 'data').text.encode('utf-8')).hexdigest(), 16)
                    connection = [1 - float('0.' + str(edge_number_code)),
                                  1 - float('0.' + str(source_number_code)),
                                  1 - float('0.' + str(target_number_code))]
        connmap.append(connection)

assert len(connmap) == length * length

connmap_arr = np.asarray(connmap)  # .reshape((length, length))

numpyData = {"array": connmap_arr}
encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
with open(full_filename + '_multilayer.connmap', 'w') as multilayer_json_file:
    json.dump(encodedNumpyData, multilayer_json_file)
