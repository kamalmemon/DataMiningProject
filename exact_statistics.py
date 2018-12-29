# imported libraries for python
import networkx as nx
import numpy as np
import time
from datetime import datetime

# imported libraries for multiprocessing
import multiprocessing
import sys

# constants used to define the path where the data is to be saved.
STATS_FILE_NAME = './stats/wiki_stats.txt';
DELIMITER = '\t';
FILE_NAME = 'Wiki_edges_';
FILE_PATH_PREFIX = './edges/';
PATH_DISTRIBUTION_PATH = './path_distribution/lscc_wiki.txt';
CONNECTED_COMPONENT = 'lscc'; 	# the value of the file name could be 'lscc' or 'lwcc'

# Function used to read the edges from file and return the graph.
def readEdgeFromFile(filename, comments=' ', delimiter='\t'):
	G = nx.read_edgelist(FILE_PATH_PREFIX + FILE_NAME + filename + '.txt', comments=comments, delimiter=delimiter, nodetype=int,create_using=nx.DiGraph())
	return G;

# extracts the statistics from the path distribution provided
def getStatisticsForDistribution(dist):
	dist_mean = np.mean(dist);
	dist_median = np.percentile(dist, 50);
	dist_diameter = max(dist);
	dist_eff_diameter = np.percentile(dist, 90);
	return dist_mean, dist_median, dist_diameter, dist_eff_diameter 

# Finds the shortest path for a single source
def getPairsShortestPath(G, i, cuttoff=None):
   	length = nx.single_source_shortest_path_length
	print('processing node: '+ str(i)) 
	count = 0;
	for n in G:       	
		if count == i:
			yield (n, dict(length(G, n, cutoff=None)))
			break;
		count = count + 1;

# A worker function called from each process to individually process the shortest path distribution of the node provided and save it in an array
def worker(G, num, return_dict):
	p = getPairsShortestPath(G,num);
	plist = list(p);
	return_dict.append(plist[0][1].values()[1:]);
	
if __name__ == '__main__':
	# writing time to statistics file
	file = open(STATS_FILE_NAME,'a') 
	file.write('TIME: ' + str(datetime.now()) + ' Reading Edges from File');
	file.close();
	
	# read the edges of the graph for the provided component
	graph = readEdgeFromFile(CONNECTED_COMPONENT, comments='#', delimiter= DELIMITER)	
	
	# writing time to statistics file
	file = open(STATS_FILE_NAME,'a') 
	file.write('TIME: ' + str(datetime.now()) + ' Edge Reading complete');
	file.write('TIME: ' + str(datetime.now()) + ' Start creating shortest path distribution');
	file.close();

	# initialize the multiprocessing manager and initialize the required arrays
   	manager = multiprocessing.Manager()
    	return_dict = manager.list()
    	jobs = []
	dist_list = [];
	final_list = np.array([]);
 	
	# define the batch size of process to run in parallel
	BATCH_SIZE = 800
	nodes_traversed = False;
	start_range = 0;
	end_range = BATCH_SIZE;
	no_nodes = len(graph.nodes());

	# keep creating new batches till all the nodes are traversed
	while nodes_traversed != True:
		if(end_range == no_nodes):
			nodes_traversed = True;
		# for each node in the batch create a new process
		for i in range(start_range, end_range):
        		p = multiprocessing.Process(target=worker, args=(graph, i, return_dict))
        		jobs.append(p)
        		p.start()
		# wait for all the processes to end
    		for proc in jobs:
        		proc.join()

		# merge the list from all the processes
		if(len(return_dict) == BATCH_SIZE):
			for item in return_dict:
				final_list = np.append(final_list,np.array(item))
		else:
			final_list = np.array(dist_list);		
		# write the distribution of this batch to the file
		file = open(PATH_DISTRIBUTION_PATH,'a') 
		np.savetxt(file, final_list, delimiter=',', newline = ',', fmt='%d')
		file.close();

		print('End of batch from ' + str(start_range) + ':' + str(end_range))
		
		# update the parameters to start new batch		
		start_range = end_range;
		end_range = min(end_range + BATCH_SIZE, no_nodes);	
		return_dict = manager.list();
		final_list = np.array([]);
		jobs=[];

	# writing time to statistics file
	file = open(STATS_FILE_NAME,'a') 
	file.write('TIME: ' + str(datetime.now()) + ' Shortest path Distribution completed');
	file.write('TIME: ' + str(datetime.now()) + ' Extracting Statistics');
	file.close();

	# read the distribution from the file
	dist = np.genfromtxt(PATH_DISTRIBUTION_PATH, delimiter=',', dtype=int);

	# writing time to statistics file
	file = open(STATS_FILE_NAME,'a') 
	file.write('TIME: ' + str(datetime.now()) + ' Path distribution read from file');
	file.close();

	# extract the statistics from the path distribution read
	mean, median, diameter,eff_diameter = getStatisticsForDistribution(dist.flatten());

	print('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Mean: '+ str(mean));
	print('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Median: '+ str(median));
	print('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Diameter: '+ str(diameter));
	print('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Effective Diameter: '+ str(eff_diameter));

	# writing time to statistics file
	file = open(STATS_FILE_NAME,'a') 
	file.write('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Mean: '+ str(mean));
	file.write('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Median: '+ str(median));
	file.write('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Diameter: '+ str(diameter));
	file.write('TIME: ' + str(datetime.now()) + CONNECTED_COMPONENT + ' EXACT Effective Diameter: '+ str(eff_diameter));
	file.close()

