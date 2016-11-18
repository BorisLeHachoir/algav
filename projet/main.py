#!/usr/bin/python
import time
import sys

ALPHABET_SIZE = 40
DEBUG = 0
#todo Cpt de NIL et de hauteur a update directement dans l'ajout 
#todo comonPrefix 

def getIdWord(s):
	char=s[0]
	if char=='_':
		return 0
	elif char>='a' and char<='z':
		return ord(char)-ord('a')+1
	elif char>='0' and char<='9':
		return ord(char)-ord('0')+27
	elif char=='&':
		return 37
	elif char=='[':
		return 38
	elif char==']':
		return 39
	else:
		print 'PANIC : '+char+'non connu'

def comonPrefix(str1, str2):
	for i in range(len(str1)):
		if str2[i]:
			if str1[i]!=str2[i]:
				return str1[:i]
	return str1


############################
####### PatriciaTree #######
############################

class PatriciaTree(object):
	def __init__(self):
		self.key = [None] * ALPHABET_SIZE
		self.children = [None] * ALPHABET_SIZE
		self.wordCount = 0

	def add(self, word):
		if self.addrec(word+'_'):
			self.wordCount+=1
		if DEBUG: print "FIN ADD"


	def addrec(self, word):
		#test word est vide
		if word[0] == '_':
			if not self.key[0]: 
				if DEBUG: print "Ajout '_'"
				self.key[0]='_'
				return True
			else:
				if DEBUG: print "MOT DEJA PRESENT"
				return False

		elif not self.key[getIdWord(word)]:
			self.key[getIdWord(word)] = word
			if DEBUG: print "Ajout clef vide"
			return True

		#Si il y a une clef deja presente
		else:
			strpre = comonPrefix(self.key[getIdWord(word)], word)
			suffixkey=self.key[getIdWord(strpre)][len(strpre):]
			suffixword=word[len(strpre):]
			oldkey=self.key[getIdWord(strpre)]
			self.key[getIdWord(strpre)] = strpre

			if DEBUG: print "OLDKEY = ", oldkey, "strpre = ", strpre, "suffixkey = ", suffixkey, "suffixword = ", suffixword

			#cas ou la clef n'as aucun fils
			if oldkey[-1:] == '_':
				if strpre == oldkey:
					if DEBUG: print "MOT DEJA PRESENT"
					return False
				else:
					if DEBUG: print "Ajout clefs sans fils"
					self.children[getIdWord(strpre)]=PatriciaTree()
					self.children[getIdWord(strpre)]=PatriciaTree()
					self.children[getIdWord(strpre)].addrec(suffixkey)
					return self.children[getIdWord(strpre)].addrec(suffixword)
			#cas ou la clef a un fils
			else:
				#Si update de la key, on sauvegarde les anciens fils
				if strpre != oldkey:
					if DEBUG: print "Update de la key"
					saveChildren = self.children[getIdWord(strpre)]
					self.children[getIdWord(strpre)] = PatriciaTree()
					self.children[getIdWord(strpre)].children[getIdWord(suffixkey)] = saveChildren
					self.children[getIdWord(strpre)].addrec(suffixkey)
					return self.children[getIdWord(strpre)].addrec(suffixword)
				else:			
					#On verifie si il existe un fils commencant par la meme lettre
					if not self.children[getIdWord(strpre)]:
						if DEBUG: print "Creation nouveau fils"
						self.children[getIdWord(strpre)] = PatriciaTree()
					#Si l'ancienne clef est prefixe du mot a ajouter
					if strpre == oldkey:
						return self.children[getIdWord(strpre)].addrec(suffixword)
					else:
						print "PANIC: strpre&oldkey"


	def printsearch(self, word):
		print "Recherche de: ", word, ": ", str(self.search(word))

	def search(self, word):
		if word == "" and self.key[0] == '_':
			return True
		mykey = self.key[getIdWord(word)]
		if mykey == None:
			return False
		elif self.key[getIdWord(word)][:-1] == word:
			return True
		elif self.children[getIdWord(mykey)] == None:
			return False
		else:
			prefix = comonPrefix(self.key[getIdWord(word)], word)
			word = word[len(prefix):]
			return self.children[getIdWord(mykey)].search(word)

	def printWords(self, word):
		for k in self.key:
			if k:
				if k[-1:] == '_':
					print word + k[:-1]
				else:
					if self.children[getIdWord(k)]:
						self.children[getIdWord(k)].getWords(word + k)


	def displayKey(self):
		j = 0;
		for i in self.key:
			if i:
				sys.stdout.write(i)
				sys.stdout.write("[")
				sys.stdout.write(str(j))
				sys.stdout.write("]")
				sys.stdout.write(", ")
			j+=1

	def displayChildren(self):
		for i in self.children:
			if i:
				i.displayKey()
				sys.stdout.write(" | ")
		sys.stdout.write("\n")

	def displayPT(self):
		i = 0
		for elem in self.key:
			if elem:
				sys.stdout.write("KEY: ")
				sys.stdout.write(elem)
				sys.stdout.write(" CHILD: ")
				if self.children[getIdWord(elem)]:
					for elem2 in self.children[getIdWord(elem)].key:
						if elem2:
							sys.stdout.write(elem2)
							sys.stdout.write(" | ")
				print
			i+=1
		for elem in self.children:
			if elem:
				elem.displayPT()

	def getWordCount(self):
		return self.wordCount

	def getHeight(self):
		h = 0;
		for c in self.children:
			if c:
				if c.getHeight()+1 > h:
					h =  c.getHeight()+1
		return h

	def getNilptr(self):
		n = 0;
		for c in self.children:
			if c:
				n+= c.getNilptr()
			else:
				n+=1
		return n

#######################
####### M A I N #######
#######################

t0 = time.time()
pt = PatriciaTree()

with open("Shakespeare/1henryiv.txt") as f:
     for w in f.readlines():
     	pt.add(w[:-1])

print "Hauteur de l'arbre: ", pt.getHeight()
print "Nombre de pointeurs NIL: ", pt.getNilptr()
print "Nombre de mots dans l'arbre: ", pt.getWordCount()

print "Execution time: ", time.time() - t0