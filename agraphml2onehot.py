import os
import sys
import xml.etree.ElementTree as eT
from argparse import ArgumentParser

import numpy as np
from PIL import Image

import config

parser = ArgumentParser()
parser.add_argument('-f', '--filename', dest='filename', required=True)
args = parser.parse_args()

IMG_SIZE = (200, 200)


def get_room_type(room_id, _graph):
    for room in _graph.findall(namespace + 'node'):
        if room_id == room.get('id'):
            data = room.findall(namespace + 'data')
            for d in data:
                if d.get('key') == 'roomType':
                    return d.text


room_types_sorted = sorted(config.room_type_codes.keys())
edge_types_sorted = sorted(config.edge_type_codes.keys())


def one_hot_vector(ind, size):
    vector = []
    for x in range(size):
        if x == ind:
            vector.append(1)
        else:
            vector.append(0)
    return vector


def get_vector(entity_type, category):
    if category == 'room':
        ind = room_types_sorted.index(str(entity_type).upper())
        return one_hot_vector(ind, len(room_types_sorted))
    else:
        ind = edge_types_sorted.index(str(entity_type).upper())
        return one_hot_vector(ind, len(edge_types_sorted))


namespace = '{http://graphml.graphdrawing.org/xmlns}'
dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
filename = args.filename
full_filename = dirname + '/' + filename
tree = eT.parse(full_filename)
root = tree.getroot()
graph = root[0]

room_ids = [room.get('id') for room in graph.findall(namespace + 'node')]

length = len(room_ids)
connmap = []
for i in range(length):
    id_from = ''
    try:
        id_from = room_ids[i]
    except IndexError:
        pass
    for j in range(length):
        # initialize with 'no connection'
        connection = []
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
                    source_vector = get_vector(get_room_type(room_ids[i], graph), 'room')
                    target_vector = get_vector(get_room_type(target_id, graph), 'room')
                    edge_vector = get_vector(edge.find(namespace + 'data').text, 'edge')
                    connection.append(source_vector)
                    connection.append(target_vector)
                    connection.append(edge_vector)
        connmap.append(connection)

assert len(connmap) == length * length

connmap_arr = np.array(connmap).reshape((length, length))

print(connmap_arr)

# img = Image.fromarray(connmap_arr, 'L').resize(IMG_SIZE)
# img.save(full_filename + '.png')
