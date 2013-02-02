def parse_graph(filepath):
	Gco = {}  # dict with key = comic and value = list of character
	with open(filepath, 'r') as f:
		for line in f:
			entry = line.split("\t")
			character = entry[0]
			comic = entry[1]
			if comic not in Gco:
				Gco[comic] = []
			Gco[comic].append(character)
	return Gco

def parse_weighted_graph(Gco):
	Gcha = {}  # dict with key = (character) and value = (dict with key = (character) and value = (weight))
	for comic in Gco:
		for chara1 in Gco[comic]:
			if chara1 not in Gcha:
				Gcha[chara1] = {}
			for chara2 in Gco[comic]:
				if chara2 == chara1:
					continue
				if chara2 not in Gcha[chara1]:
					Gcha[chara1][chara2] = 0
				Gcha[chara1][chara2] += 1
	return Gcha

Gco = parse_graph("marvel.tsv")
Gcha = parse_weighted_graph(Gco)

max_couple = (None, None)
max_value = 0
for chara1 in Gcha:
	for chara2 in Gcha[chara1]:
		if Gcha[chara1][chara2] > max_value:
			max_couple = (chara1, chara2)
			max_value = Gcha[chara1][chara2]

print max_couple, max_value
