#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from re import match, sub
from Levenshtein import ratio, jaro_winkler

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

abrev = "(adj.|abs.|abl.|adv.|aor.|cmp.|conj.|caus.|deno.|des.|f.|ger.|intj.|ind.|inf.|m.|nt.|onom.|pas.|plu.|pp.|pr.p.|ppres.|prep.|pret.|ppot.|ptsd.|v.i.|v.t.|n.|v.|sing.|p.ej.)".replace(".", "\.")

def extract_keys ():
	keys = {}

	index = 0
	found = False
	for line in dicc:
		if not found:
			found = True
			key = match("[^ ]+", line).group(0)
			keys[key] = (index, 0)

		if match(".*\.$", line):
			found = False
			keys[key] = (keys[key][0], index + 1)

		index = index + 1
	return keys

def lev_menu_for (word):
	with_ratio = [ (jaro_winkler(word, key), key) for key in keys_without_accents.keys() ]
	with_ratio.sort(reverse = True)

	options = filter(lambda (ratio, key): ratio > 0.9, with_ratio[0:4])
	if options:
		print "Quizás quiso decir:"
		for ratio, key in options:
			print
			search(key)

def search (word):
	word = word.lower()
	
	if not word in keys_without_accents:
		print "No se encontró la entrada."
		lev_menu_for (word)
		return

	with_accents = keys_without_accents[word]
	index_start, index_end = keys[with_accents]
	
	for line in dicc[index_start: index_end]:
		line = sub("^" + with_accents, color.BOLD + with_accents + color.END, line)
		line = sub("( [0-9]\. )", color.BOLD + color.BLUE + "\\1" + color.END, line)
		line = sub(" " + abrev + "([ ;])", color.BOLD + color.RED + " \\1\\2" + color.END, line)

		print line

	return

def search_by_bruteforce (word):
	word = fix_accents(word)

	found = False
	for line in dicc:
		if not found and match("^" + word + " ", line):
			found = True
			word_len = len(word)
			print "\033[1m" + line[:word_len] + "\033[0m" + line[word_len:]
		elif found:
			print line
			if match(".*\.$", line): return

def fix_accents (word):
	replacements = [ ("a-", "ā"), ("u-", "ū"), ("i-", "ı̄"), ("m'", "ṁ"), ("n'", "ṅ") ]
	return replace(word, replacements)

def remove_accents (word):
	replacements = [ ("ā", "a"), ("ū", "u"), ("ı̄", "i"), ("ṁ", "m"), ("ṅ", "n"), ("n.", "n"), ("l.", "l"), ("d.", "d"), ("t.", "t") ]
	return replace(word, replacements)

def replace (word, replacements):	
	for escaped, replacement in replacements:
		word = word.replace(escaped, replacement)
	return word

def without_accents (keys):
	return { remove_accents(key): key for (key, value) in keys.items() }

# MAIN
dicc = [ line.strip("\n") for line in open("pali-es.dic") ]
keys = extract_keys()
keys_without_accents = without_accents(keys)

print "Diccionario Pali a español"

while True:
	print "\nBúsqueda:",
	word = raw_input()
	
	if not word: quit()

	search(word)
