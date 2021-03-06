import numpy as np 
import networkx as nx
import gossip as gs
import random 

class network:
	def __init__(self, n, m):
		self.network = nx.DiGraph()
		self.network = nx.barabasi_albert_graph(n, m, seed=None) 

	def assign_information_value(self, sigma): 				#calculating mew for every vertex based on homophily
		for n,d in self.network.nodes_iter(data=True):
			self.network.node[n]['mew'] = []
			self.network.node[n]['color'] = 0
			self.network.node[n]['mewFinal'] = 0
		for n,d in self.network.nodes_iter(data=True):
			if len(self.network.node[n]['mew']) == 0:
				self.network.node[n]['mew'].append(random.random())
				for j in self.network.neighbors(n):
					random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					while (random_number<0 or random_number>1.0):
						random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					self.network.node[j]['mew'].append(random.gauss(np.mean(self.network.node[n]['mew']), sigma))
			else:
				for j in self.network.neighbors(n):
					random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					while (random_number<0 or random_number>1.0):
						random_number = random.gauss(np.mean(self.network.node[n]['mew']), sigma)
					self.network.node[j]['mew'].append(random_number)
		for n,d in self.network.nodes_iter(data=True):
			if len(self.network.node[n]['mew'])>0:
				self.network.node[n]['mewFinal'] = np.mean(self.network.node[n]['mew'])
			else:
				self.network.node[n]['mewFinal']=0
#			print self.network.node[n]['mew_final']

	def gossip_value_for_edge(self):
		max_degree = 0
		for n,d in self.network.nodes_iter(data=True):
			if max_degree < self.network.degree(n):
				max_degree = self.network.degree(n)

		for m in self.network.edges_iter():
			self.network.edge[m[0]][m[1]]['gossip'] = (self.network.degree(m[0])*self.network.degree(m[1])*1.0)/(max_degree*max_degree)
#			print self.network.edge[m[0]][m[1]]['gossip']

	def information_diffusion(self, num_nodes, beta):
#		patients_zero = [random.randint(0,num_nodes) for r in xrange(beta)]
#		for i in patients_zero:
#			self.network.node[i]['color'] = 1
#		print patients_zero
#		for i in patients_zero:
#			for j in self.network.neighbors(i):
		root_node = random.randint(0,num_nodes-1)
		self.network.node[root_node]['color']=1
		ordered_edges = list(nx.bfs_edges(self.network,root_node))
		print ordered_edges 
		t_name = "plots/file_name"
		count = 0
		for i in ordered_edges:
			count = count +1 
#			print self.network.node[i[0]]['color']==1,  self.network.node[i[1]]['color']==0
			if(self.network.node[i[0]]['color']==1 and self.network.node[i[1]]['color']==0):
#				probability =100* self.network.node[i[1]]['mew_final']*self.network.edge[i[0]][i[1]]['gossip']
				probability = random.random()
				print i, probability
				if probability > beta:
#					print "hello from other side"
					self.network.node[i[1]]['color']=1
			if(count%100==0):
				name = t_name + str(count)+".gml"
				nx.write_gml(self.network,name)
		
				


num_nodes = 1000
x = network(num_nodes,3)
x.assign_information_value(0.3) #sigma = standard deviation
x.gossip_value_for_edge()
x.information_diffusion(num_nodes, 0.2) #number of patient zeros
