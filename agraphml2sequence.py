import os
import sys
import xml.etree.ElementTree as eT
from argparse import ArgumentParser

import config

parser = ArgumentParser()
parser.add_argument('-f', '--filename', dest='filename', required=True)
args = parser.parse_args()


def get_room_type(room_id, _graph):
    for room in _graph.findall(namespace + 'node'):
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

length = len(room_ids)
connmap = []
for i in range(length):
    id_from = ''
    try:
        id_from = room_ids[i]
    except IndexError:
        pass
    for j in range(length):
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
                    source_number_code = config.room_types[config.room_type_codes[get_room_type(room_ids[i], graph)]]
                    target_number_code = config.room_types[config.room_type_codes[get_room_type(target_id, graph)]]
                    edge_number_code = config.edge_types[config.edge_type_codes[edge.find(namespace + 'data').text]]
                    connection = source_number_code + target_number_code + edge_number_code
                    connmap.append(connection)

with open(full_filename + '_SEQ.txt', 'w') as f:
    f.write(','.join(connmap))
