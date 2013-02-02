import random
import Queue
import time


movies = set()
def parse_graph(filepath):
	G = {}
	global movies
	with open(filepath, 'r') as f:
		for line in f:
			entry = line.split("\t")  # [ACTOR][MOVIE][YEAR]
			actor = entry[0]
			movie = entry[1] + entry[2]
			if actor not in G:
				G[actor] = []
			if movie not in G:
				movies.add(movie)
				G[movie] = []
			G[actor].append(movie)
			G[movie].append(actor)
	return G, movies

def parse_cardinalities(filepath):
	card = []
	with open(filepath, 'r') as f:
		for line in f:
			entry = line.split("\t")
			card.append((entry[0], float(entry[1])))
	return card

cnt = 0
start = time.clock()
def centrality(G, node):
	## average shortest distance path distance to each reachable node
	#print(node)
	global start
	global cnt
	cnt += 1
	if (cnt % 100 == 0):
		newClock = time.clock()
		print(cnt, newClock - start)
		start = newClock
	global movies

	if (node in movies):
		return 99

	queue = Queue.Queue()
	queue.put(node)
	marked_distance = {}
	marked_distance[node] = 0
	while (not queue.empty()):
		current = queue.get()
		for neighbor in G[current]:
			if (not neighbor in marked_distance):
				marked_distance[neighbor] = marked_distance[current] + 1
				queue.put(neighbor)

	# only keeps actors
	marked_distance = filter(lambda x: x[0] in movies, marked_distance.iteritems())
	marked_distance = map(lambda x: x[1], marked_distance)

	found_centrality = sum(marked_distance) * 1.0 / len(marked_distance)
	return found_centrality


def topK(aList, k, smaller=lambda x, y: x < y):
	top = aList[:k]
	for elem in aList[k:]:
		for i in range(len(top)):
			if smaller(top[i], elem):
				top[i], elem = elem, top[i]
	return top

G, movies = parse_graph("imdb-1.tsv")

print(len(G))

cardinalities = map(lambda x: (x, centrality(G, x)), G)

with open("card_saved", "w") as f:
	for elem in cardinalities:
		f.write(str(elem[0]) + "\t" + str(elem[1]) + "\n")

#cardinalities = parse_cardinalities("card_saved")

cardinalities = filter(lambda x: x[0] not in movies, cardinalities)

top = topK(cardinalities, 25, lambda x, y: y in movies or x[1] > y[1])

for i, t in enumerate(top):
	print (i, t)
