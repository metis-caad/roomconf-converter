import hashlib
import os
import sys
import xml.etree.ElementTree as eT
from argparse import ArgumentParser

import numpy as np
from PIL import Image

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
                    return d.text.encode('utf-8')


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
        connection = '0.0,0.0,0.0'
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
                    conn_arr = ['0.' + str(source_number_code),
                                '0.' + str(target_number_code),
                                '0.' + str(edge_number_code)]
                    connection = ','.join(conn_arr)
        connmap.append(connection)

assert len(connmap) == length * length

connmap_arr = np.array(connmap).reshape((length, length))

# print(connmap_arr)

connmap_arr_3d = []
for j in range(length):
    row = connmap_arr[j]
    row_3d = []
    for conn in row:
        conn_splitted = str(conn).split(',')
        conn_3d = []
        for k in range(len(conn_splitted)):
            value = float(conn_splitted[k])
            conn_3d.append(value)
        row_3d.append(conn_3d)
    connmap_arr_3d.append(row_3d)

# print(connmap_arr_3d)

img = Image.fromarray(np.array(connmap_arr_3d), 'RGB').resize(IMG_SIZE)
img.save(full_filename + '_MULTI.png')
