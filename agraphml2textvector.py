import os
import sys
import uuid
import xml.etree.ElementTree as eT
from argparse import ArgumentParser
import numpy as np
import display as gcd
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-f', '--filename', dest='filename', required=True)
args = parser.parse_args()


# To be use in the Notebook for function Call   
def find_room_type(room_id,graph,namespace):
    '''
    returns the roomType of a edge in AgraphML
    '''
    for room in graph.findall(namespace + 'node'):
        if room_id == room.get('id'):
            data = room.findall(namespace + 'data')
            for d in data:
                if d.get('key') == 'roomType':
                    return d.text
# Converts a list of strings to a string                
def converttostr(input_seq, seperator):
    final_str=''
    for i,word in enumerate(input_seq):
        if(i!=(len(input_seq)-1)):      # to make sure the whitespace after the last string is ignored
            final_str+=''.join((word.lower(),seperator,' '))
        else:
            final_str+=''.join((word.lower()))
    return final_str
    
namespace = '{http://graphml.graphdrawing.org/xmlns}'
dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
filename = args.filename
full_filename = dirname + '/' + filename
tree = eT.parse(full_filename)
root = tree.getroot()
graph = root[0]
room_ids = [room.get('id') for room in graph.findall(namespace + 'node')]
length = len(room_ids)
nlpmap = []
source_list=[]
guids_list=[]
for Id in room_ids:
    count=0
    for edge_1 in graph.findall(namespace + 'edge'):
        source_id_1 = edge_1.get('source')
        if source_id_1==Id and count==0:
            count=1                          # count is uses to make sure each unique source is only considered once
            target_list=[]
            edge_list=[]
            target_id_list=[]
            edge_id_list=[]
            conn=[]
            guid_row=[]
            for edge_2 in graph.findall(namespace + 'edge'):    # finds all the target rooms and edgetypes for a unique source room
                source_id_2 = edge_2.get('source')
                if source_id_1==source_id_2:
                    target_id=edge_2.get('target')
                    target_id_list.append(target_id)
                    target_list.append(find_room_type(target_id,graph,namespace))
                    edge_list.append(edge_2.find(namespace + 'data').text.lower())
            source = find_room_type(source_id_1,graph,namespace)
            source_list.append(source_id_1)
            conn.append(source.lower() + ' ' + 'connects with' + ' ' + converttostr(target_list,',') + ' ' + 'using' + ' ' +  converttostr(edge_list,',')) 
            guid_row.append(source_id_1)
            guid_row.append(target_id_list)
            guid_row.append(edge_list)
            guids_list.append(guid_row)
            nlpmap.append(conn)
assert(len(source_list)==len(nlpmap))
nlpmap=np.array(nlpmap)

with open(full_filename + '_txtvec.map', 'w') as query_map_file:
    query_map_file.write(np.array2string(nlpmap).replace('\n', ''))