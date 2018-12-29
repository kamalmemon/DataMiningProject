# import libraries 
import networkx as nx
import numpy as np
import time
from datetime import datetime

# declare constants for file names to save the extracted edges
STATS_FILE_NAME = './stats/wiki_stats.txt';
DELIMITER = '\t';
EDGE_WRITE = './edges/Wiki_edges_';
FILE_PATH_PREFIX = './data/';
FILE_NAME = 'Wiki-Vote';

# read edges from file returns the graph
def readEdgeFromFile(filename, comments=' ', delimiter='\t'):
	G = nx.read_edgelist(FILE_PATH_PREFIX + filename, comments=comments, delimiter=delimiter, nodetype=int,create_using=nx.DiGraph())
	return G;

# write the edges of the provided graph to the file
def writeEdgeToFile(graph, filename, comments=' ', delimiter='\t'):
	G = nx.write_edgelist(graph, EDGE_WRITE + filename, comments=comments, delimiter=delimiter, data=False)
	return G;

# extract the LSCC from the directed graph provided
def largestStronglyConnecteComponentSubGraph(dGraph):
    scc = nx.strongly_connected_components(dGraph);
    print('Strongly connected Components extracted, Extracting the largest SCC')
    return dGraph.subgraph(max(scc, key= len))

# extract LWCC from the directed graph provided and than convert it to undirected graph
def largestWeaklyConnecteComponentSubGraph(dGraph):
    wcc = nx.weakly_connected_components(dGraph);
    print('Weakly connected Components extracted, Extracting the largest W                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                CC')
    directedLwcc =  dGraph.subgraph(max(wcc, key= len))
    
    return directedLwcc.to_undirected();


if __name__ == '__main__':
	# write statistics to file
	file = open(STATS_FILE_NAME,'a')
	file.write('TIME: ' + str(datetime.now()) + ' Starting Edge Extraction')
	file.close()
	print('TIME: ' , str(datetime.now()) , ': Done ')

	# read edges from the file
	directedGraph = readEdgeFromFile(FILE_NAME + '.txt', comments='#', delimiter= DELIMITER)
	print('TIME: ' , str(datetime.now()) , ': Graph read from the file')

	# write statistics to file
	file = open(STATS_FILE_NAME,'a')
	file.write('TIME: ' + str(datetime.now()) + ' Extracting LSCC')
	file.close()	

	# extracting LSCC
	lscc = largestStronglyConnecteComponentSubGraph(directedGraph);
	lscc_edges = lscc.edges();
	lscc_edges_len = len(lscc_edges);

	print('Nodes for the Largest Strongly Connected Components: ' + str(len(lscc.nodes())))
	print('Edges for the Largest Strongly Connected Components: ' + str(lscc_edges_len))

	# writing the extracted edges of LSCC to the file.
	writeEdgeToFile(lscc, 'lscc.txt', comments='#', delimiter=DELIMITER);



	# write statistics to file
	print('TIME: ' + str(datetime.now()) + ' LSCC written to file')
	file = open(STATS_FILE_NAME,'a') 
	file.write('TIME: ' + str(datetime.now()) + '+ Nodes for the Largest Strongly Connected Components: ' + str(len(lscc.nodes())))
	file.write('TIME: ' + str(datetime.now()) + ' Edges for the Largest Strongly Connected Components: ' + str(lscc_edges_len))
	file.close()

	# GC: variable not needed anymore, removing the variable
	del lscc;

	# extracting LWCC
	lwcc = largestWeaklyConnecteComponentSubGraph(directedGraph);

	# GC: variable not needed anymore, removing the variable
	del directedGraph;

	# extracting number of edges for LWCC
	lwcc_edges = lwcc.edges();
	lwcc_edges_len = len(lwcc_edges);

	print('Nodes for the Largest Weakly Connected Components: ' + str(len(lwcc.nodes())))
	print('Edges for the Largest Weakly Connected Components: ' + str(lwcc_edges_len))

	# writing the extracted edges of LWCC to the file.
	writeEdgeToFile(lwcc, 'lwcc.txt', comments='#', delimiter=DELIMITER)

	# write statistics to file
	print('TIME: ' + str(datetime.now()) + ' LWCC written to file')
	file = open(STATS_FILE_NAME,'a') 
	file.write('TIME: ' + str(datetime.now()) + ' Nodes for the Largest Weakly Connected Components: ' + str(len(lwcc.nodes())))
	file.write('TIME: ' + str(datetime.now()) + ' Edges for the Largest Weakly Connected Components: ' + str(len(lwcc.edges())))
	file.close()
