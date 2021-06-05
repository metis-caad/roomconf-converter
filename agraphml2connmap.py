import os
import sys
import xml.etree.ElementTree as eT
from argparse import ArgumentParser

import numpy as np
from PIL import Image

import config

parser = ArgumentParser()
parser.add_argument('-f', '--filename', dest='filename', required=True)
parser.add_argument('-z', '--zoned', dest='zoned', action='store_true')
args = parser.parse_args()

IMG_SIZE = (200, 200)
zoned = args.zoned


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
        # initialize with 'no connection'
        connection = 0.0
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
                    if zoned:
                        try:
                            connection = float('0.' + edge_number_code + edge.get('sourceZone') + edge.get('targetZone')
                                               + source_number_code + target_number_code)
                        except TypeError:
                            print('ERROR: Zones could not be found for a room or an edge. No image will be produced.')
                            exit()
                    else:
                        connection = float('0.' + edge_number_code + source_number_code + target_number_code)
        connmap.append(connection)

assert len(connmap) == length * length

connmap_arr = np.array(connmap).reshape((length, length))

# print(connmap_arr)

if not zoned:
    img = Image.fromarray(connmap_arr, 'L').resize(IMG_SIZE)
    img.save(full_filename + '.png')
else:
    connmap_dict = {}
    for row in connmap_arr:
        for val in row:
            if val > 0.:
                zones = str(val)[4:6]
                room1 = str(val)[6:8]
                room2 = str(val)[8:]
                if len(room2) == 1:
                    room2 += '0'
                if zones not in connmap_dict:
                    connmap_dict[zones] = [room1, room2]
                else:
                    values = connmap_dict[zones]
                    values.append(room1)
                    values.append(room2)
                    connmap_dict[zones] = values

    # print(connmap_dict)

    connmap_zones = []
    for z in connmap_dict:
        zone_counts = {
            config.ZONE_WET: 0,
            config.ZONE_DRY: 0,
            config.ZONE_LIVING: 0,
            config.ZONE_SLEEPING: 0,
            config.ZONE_HABITATION: 0,
            config.ZONE_SERVICE: 0
        }
        for room_code in connmap_dict[z]:
            room_type = config.room_code_numbers[room_code].upper()
            for zn in config.all_zones:
                if room_type in config.all_zones[zn]:
                    count = zone_counts[zn]
                    count += 1
                    zone_counts[zn] = count
        zone_counts_sorted = sorted(zone_counts.items(), key=lambda kv: kv[1], reverse=True)
        for x in zone_counts_sorted:
            connmap_zones.append(config.all_zones_colors_priority[x[0]][0])

    # print(connmap_zones)

    image_map = []
    length_zones = len(connmap_zones)
    for j in range(length_zones):
        for k in range(length_zones):
            image_map.append(float('0.' + connmap_zones[k]))

    assert len(image_map) == length_zones * length_zones

    image_map_reshaped = np.array(image_map).reshape((length_zones, length_zones))

    # print(zcm_reshaped)

    img = Image.fromarray(image_map_reshaped, 'L').resize(IMG_SIZE)
    img.save(full_filename + '_ZONED.png')
