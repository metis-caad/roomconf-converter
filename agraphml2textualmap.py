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


# To be use in the Notebook for function Call   
def find_room_type(room_id, graph, namespace):
    """
    returns the roomType of a edge in AgraphML
    """
    for room in graph.findall(namespace + 'node'):
        if room_id == room.get('id'):
            data = room.findall(namespace + 'data')
            for d in data:
                if d.get('key') == 'roomType':
                    return d.text


namespace = '{http://graphml.graphdrawing.org/xmlns}'
dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
filename = args.filename
full_filename = dirname + '/' + filename
tree = eT.parse(full_filename)
root = tree.getroot()
graph = root[0]
room_ids = [room.get('id') for room in graph.findall(namespace + 'node')]

length = 50  # len(room_ids)
connmap = []
triples = []
for i in range(0, length):
    triple_row = []
    id_from = ''
    try:
        id_from = room_ids[i]
    except IndexError:
        pass
    for j in range(0, length):
        connection = [float('0.' + str(int(hashlib.md5('no connection'.encode('utf-8')).hexdigest(), 16)))]
        triple = ['', '', None]
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
                    source = find_room_type(room_ids[i], graph, namespace).lower()
                    target = find_room_type(target_id, graph, namespace).lower()
                    edge = edge.find(namespace + 'data').text.lower()
                    connection_str = str(source + ' ' + 'connects with' + ' ' + target + ' ' + 'using' + ' ' + edge)
                    connection = [float('0.' + str(int(hashlib.md5(connection_str.encode('utf-8')).hexdigest(), 16)))]
                    triple = [id_from, id_to, edge]
        connmap.append(connection)
        triple_row.append(triple)
    assert len(triple_row) == length
    triples.append(triple_row)
assert len(connmap) == length * length
assert len(triples) == length
connmap_arr = np.asarray([connmap])  # .reshape((length, length))

numpyData = {"array": connmap_arr}
encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
with open(full_filename + '_text.map', 'w') as json_file:
    json.dump(encodedNumpyData, json_file)
