import xml.etree.ElementTree as eT
import os
import sys
import uuid
from argparse import ArgumentParser
import numpy as np
import python_scripts.display as gcd


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
                
def find_room_area(room_id,graph,namespace):
    '''
    returns the area of room in AgraphML
    '''
    for room in graph.findall(namespace + 'node'):
        if room_id == room.get('id'):
            data = room.findall(namespace + 'data')
            for d in data:
                if d.get('key') == 'area':
                    return d.text
                
def find_edge_type(edge_id,graph,namespace):
    '''
    returns the edgeType of a edge in AgraphML
    '''
    for edge in graph.findall(namespace + 'edge'):
        if edge_id == edge.get('id'):
            data = edge.findall(namespace + 'data')
            for d in data:
                if d.get('key') == 'edgeType':
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

# function to convert AGraphML to sentences                
def parse_graph(name):
    '''
        Parses a GraphML and converts it to Text Connection Map
        Parameter:
        ----------
        name: The name of the GraphML file which needs to be parsed 
        
        Returns:
        --------
        A Text Connection Map which is based on number of unique edge sources
    
    '''
    namespace = '{http://graphml.graphdrawing.org/xmlns}'
    tree = eT.parse('/home/jupyter/ksd.client.phoenix/data/aGraphML-housing/'+name)
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
    if name.endswith('.graphml'): 
        name = name[:-8]
    if name.endswith('.agraphml'):
        name = name[:-9]
    with open('/home/jupyter/ksd.client.phoenix/data//query_triple/'+name+'.map',
          'w') as query_triples_file:
         query_triples_file.write(str(guids_list))
    with open('/home/jupyter/ksd.client.phoenix/data/housing/'+name+'.map', 'w') as query_map_file:
         query_map_file.write(np.array2string(nlpmap).replace('\n', ''))
    return nlpmap


# Converts GraphML to an Adjacency matrix with sentences
def parse_graph_matrix(name):
    '''
        Parses a GraphML and converts it to Text Connection Map (matrix)
        Parameter:
        ----------
        name: The name of the GraphML file which needs to be parsed 
        
        Returns:
        --------
        A Text Connection Map which is a adjacency matrix of the graph
    '''
    namespace = '{http://graphml.graphdrawing.org/xmlns}'
    tree = eT.parse('/home/jupyter/ksd.client.phoenix/data/aGraphML-housing/'+name)
    root = tree.getroot()
    graph = root[0]
    room_ids = [room.get('id') for room in graph.findall(namespace + 'node')]
    length = len(room_ids)
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
            
            connection = 'no connection'        # initialize eaach connection with "no connection"
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
                        source = find_room_type(room_ids[i],graph,namespace).lower()
                        target = find_room_type(target_id,graph,namespace).lower()
                        edge = edge.find(namespace + 'data').text.lower()
                        connection = str(source + ' ' + 'connects with' + ' ' + target + ' ' + 'using' + ' ' +  edge)
                        triple = [id_from, id_to, edge]
            connmap.append(connection)
            triple_row.append(triple)
        assert len(triple_row) == length
        triples.append(triple_row)
    assert len(connmap) == length * length
    assert len(triples) == length
    connmap=np.array(connmap)
    if name.endswith('.graphml'): 
        name = name[:-8]
    if name.endswith('.agraphml'):
        name = name[:-9]
    with open('/home/jupyter/ksd.client.phoenix/data/query_triple/'+name+'.map',
          'w') as query_triples_file:
         query_triples_file.write(str(triples))
    with open('/home/jupyter/ksd.client.phoenix/data/housing/'+name+'.map', 'w') as query_map_file:
         query_map_file.write(np.array2string(connmap).replace('\n', ''))
    return connmap