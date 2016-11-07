'''
    File name: extract_concepts.py
    Author: Gangeshwar Krishnamurthy
    Email: gangeshwark@gmail.com
    Date created: 11/05/2016
    Python Version: 2.7
'''
"""
Python file to understand properties of libraries.
"""
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import nltk
import enchant
import logging


BING_LIU_DATA_PATH = 'data/bingliu_lexicon'

#Does sentiwordnet have words with '_' or multi_words?
swn_all_words = swn.all_senti_synsets()
swn_words = []
logging.info(__name__ + " - " + "\nSWN")
for word in swn_all_words:
	word_name = word.synset.name().split('.')[0]
	if '_' in word_name:
		swn_words.append(word_name)

logging.info(__name__ + " - " +  str(len(swn_words)) + str(swn_words[:10]))

#What about Bing Liu?
logging.info(__name__ + " - " + "\nBing Liu")
words = []
with open(BING_LIU_DATA_PATH + "/positive-words.txt", 'r') as bing_pos_file:
	for line in bing_pos_file:
		w = str(line)
		if '_' in w:
			words.append(w)
logging.info(__name__ + " - " + str(len(words)) + str(words[:5]))


words = []
with open(BING_LIU_DATA_PATH + "/negative-words.txt", 'r') as bing_neg_file:
	for line in bing_neg_file:
		w = str(line)
		if '_' in w:
			words.append(w)
logging.info(__name__ + " - " + str(len(words)) + str(words[:5]))

"""
OUTPUT:
SWN
29205 [u'top_round', u'avalanche_lily', u'plumb_level', u'many_a', u'folding_chair', u'japanese_deer', u'custody_case', u'break_bread', u'von_neumann_machine', u'signal_fire']

Bing Liu
0 []
0 []
"""

# Will enchant work with multi-words?
english_d = enchant.Dict("en_US")
for word in swn_words:
	logging.info(__name__ + " - " + "Is '{0}' English? {1}".format(word, english_d.check(word)))