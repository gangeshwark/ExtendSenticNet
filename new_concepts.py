'''
    File name: extract_concepts.py
    Author: Gangeshwar Krishnamurthy
    Email: gangeshwark@gmail.com
    Date created: 11/03/2016
    Python Version: 2.7
'''
"""

"""
from senticnet4_data import senticnet
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import nltk
from extract_concepts import preprocess, OUTPUT_BASE_PATH, CURRENT_SENTICNET_DATA_PATH, BING_LIU_DATA_PATH



def get_new_concepts():
	"""
		Extracts new concepts using SentiWordNet(SWN) and Bing Liu's Opinion lexicon.
		Also adding few manually picked up concepts.

	Arguments: None

	Returns:
		List of new concepts
	"""
	current_concepts = [key for (key, value) in senticnet.iteritems()]
	print "Currently Available Concepts: (sample)"
	print current_concepts[:10]
	bing_negative_words = []
	bing_positive_words = []

	swn_negative_words = []
	swn_positive_words = []
	new_neg_words, new_pos_words = [], []
	#Section 1: code to extract concepts from SWN.
	#Call preprocess for every word encountered.
	print "Extracting from SWN"
	swn_all_words = swn.all_senti_synsets()
	for word in swn_all_words:
		word_name = word.synset.name().split('.')[0]
		if word.pos_score() > word.neg_score():
			w = preprocess(word_name)
			if w is not '':
				swn_positive_words.append(w)
		else:
			w = preprocess(word_name)
			if w is not '':
				swn_negative_words.append(w)


	#include only if they are not available in knowledge base of senticnet
	print "Checking SenticNet..."
	# Running time O(n^2). Better solution below.
	"""
	for x in xrange(len(swn_positive_words)):
		if swn_positive_words[x] not in current_concepts:
			new_pos_words.append(swn_positive_words[x])

	for x in xrange(len(swn_negative_words)):
		if swn_negative_words[x] not in current_concepts:
			new_neg_words.append(swn_negative_words[x])
	"""
	#Running time O(n*logn)
	print "Positive Words"
	new_pos_words = list(set(swn_positive_words)-set(current_concepts))
	print "Negative Words"
	new_neg_words = list(set(swn_negative_words)-set(current_concepts))
	"""
	print "Sample SWN: Length: ", len(new_pos_words), len(new_neg_words)
	print new_pos_words[:10]
	print new_neg_words[:10]
	"""
	#Section 2: code to extract concepts from Bing Liu's Opinion lexicon.
	print "Extracting from Bing Liu"
	with open(BING_LIU_DATA_PATH + "/positive-words.txt", 'r') as bing_pos_file:
		for line in bing_pos_file:
			w = preprocess(line)
			if w is not '':
				bing_positive_words.append(w)

	with open(BING_LIU_DATA_PATH + "/negative-words.txt", 'r') as bing_neg_file:
		for line in bing_neg_file:
			w = preprocess(line)
			if w is not '':
				bing_negative_words.append(w)
	
	#include only if they are not available in knowledge base of senticnet
	print "Checking SenticNet..."
	# Running time O(n^2). Better solution below.
	"""
	for x in xrange(len(bing_positive_words)):
		if bing_positive_words[x] not in current_concepts:
			new_pos_words.append(bing_positive_words[x])

	for x in xrange(len(bing_negative_words)):
		if bing_negative_words[x] not in current_concepts:
			new_neg_words.append(bing_negative_words[x])
	"""
	#unique concepts
	#Running time O(n*logn)
	print "Positive Words"
	bing_new_pos_words = list(set(bing_positive_words)-set(current_concepts))
	print "Negative Words"
	bing_new_neg_words = list(set(bing_negative_words)-set(current_concepts))
	"""
	print "Sample Bing Liu: Length: ", len(bing_new_pos_words), len(bing_new_neg_words)
	print bing_new_pos_words
	print bing_new_neg_words
	"""
	new_pos_words+=bing_new_pos_words
	new_neg_words+=bing_new_neg_words

	#store them in file.
	with open(OUTPUT_BASE_PATH + '/new_positive_words.txt') as out_posi_file:
		for word in new_pos_words:
			out_posi_file.write("%s\n" %word)

	with open(OUTPUT_BASE_PATH + '/new_negative_words.txt') as out_neg_file:
		for word in new_neg_words:
			out_neg_file.write("%s\n" %word)


if __name__ == '__main__':
	get_new_concepts()