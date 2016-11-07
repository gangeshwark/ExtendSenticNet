'''
    File name: extract_new_concepts.py
    Author: Gangeshwar Krishnamurthy
    Email: gangeshwark@gmail.com
    Date created: 11/03/2016
    Python Version: 2.7
'''
"""
Extracts new concepts, not in SenticNet, from other lexicons and stores it in a file.
"""
from senticnet4_data import senticnet
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import nltk
from add_concepts import preprocess, OUTPUT_BASE_PATH, CURRENT_SENTICNET_DATA_PATH, BING_LIU_DATA_PATH
from datetime import datetime
import logging, logging.config
import os.path
#from logger import *

#initialize_logger("logs")
'''
logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")

'''
    
def extract_new_concepts():
	"""
		Extracts new concepts using SentiWordNet(SWN) and Bing Liu's Opinion lexicon.
		Also adding few manually picked up concepts.

	Arguments: None

	Returns:
		List of new concepts
	"""
	startTime = datetime.now()
	current_concepts = [key for (key, value) in senticnet.iteritems()]
	logging.info("Currently Available Concepts: (sample)")
	logging.info(str(current_concepts[:10]))
	bing_negative_words = []
	bing_positive_words = []

	swn_negative_words = []
	swn_positive_words = []
	new_neg_words, new_pos_words = [], []
	#Section 1: code to extract concepts from SWN.
	#Call preprocess for every word encountered.
	logging.info("Extracting from SWN")
	swn_all_words = swn.all_senti_synsets()
	for word in swn_all_words:
		word_name = word.synset.name().split('.')[0]
		if word.pos_score() > word.neg_score():
			w = preprocess(word_name)
			if w and w is not '':
				swn_positive_words.append(w)
		else:
			w = preprocess(word_name)
			if w and w is not '':
				swn_negative_words.append(w)


	#include only if they are not available in knowledge base of senticnet
	logging.info("Checking SenticNet...")
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
	logging.info("Positive Words")
	new_pos_words = list(set(swn_positive_words)-set(current_concepts))
	logging.info("Negative Words")
	new_neg_words = list(set(swn_negative_words)-set(current_concepts))
	"""
	print "Sample SWN: Length: ", len(new_pos_words), len(new_neg_words)
	print new_pos_words[:10]
	print new_neg_words[:10]
	"""
	#Section 2: code to extract concepts from Bing Liu's Opinion lexicon.
	logging.info("Extracting from Bing Liu")
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
	logging.info("Checking SenticNet...")
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
	logging.info("Positive Words")
	bing_new_pos_words = list(set(bing_positive_words)-set(current_concepts))
	logging.info("Negative Words")
	bing_new_neg_words = list(set(bing_negative_words)-set(current_concepts))
	"""
	print "Sample Bing Liu: Length: ", len(bing_new_pos_words), len(bing_new_neg_words)
	print bing_new_pos_words
	print bing_new_neg_words
	"""
	new_pos_words+=bing_new_pos_words
	new_neg_words+=bing_new_neg_words

	#store them in file.
	with open(OUTPUT_BASE_PATH + '/new_positive_words.txt', 'w+') as out_posi_file:
		for word in new_pos_words:
			out_posi_file.write("%s\n" %word)

	with open(OUTPUT_BASE_PATH + '/new_negative_words.txt', 'w+') as out_neg_file:
		for word in new_neg_words:
			out_neg_file.write("%s\n" %word)
	#startTime = datetime.now()		
	logging.error("Time to execute extract_new_concepts.extract_new_concepts(): {0}".format(datetime.now() - startTime))


if __name__ == '__main__':
	startTime = datetime.now()
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	output_dir = 'logs'
	 
	# create console handler and set level to info
	handler = logging.StreamHandler()
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(funcName)s: %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# create error file handler and set level to error
	handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
	handler.setLevel(logging.ERROR)
	formatter = logging.Formatter("%(asctime)s [%(levelname)s] {%(funcName)s:%(lineno)d}: %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# create debug file handler and set level to debug
	handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(funcName)s: %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	extract_new_concepts()
	logging.error("Time to execute extract_new_concepts.main(): {0}".format(datetime.now() - startTime))
