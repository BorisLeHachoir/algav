#!/usr/bin/python
import time
import sys

ALPHABET_SIZE = 40
DEBUG = 0

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

####### PatriciaTree #######
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




	def getWords(self, word):
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
				sys.stdout.write(str(i))
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
		print
		for elem in self.children:
			if elem:
				elem.displayPT()

	def getWordCount(self):
		return self.wordCount


def comonPrefix(str1, str2):
	for i in range(len(str1)):
		if str1[i]!=str2[i]:
			return str1[:i]
	return str1


####### M A I N #######
t0 = time.time()
pt = PatriciaTree()

with open("Shakespeare/1henryiv.txt") as f:
     for w in f.readlines():
     	pt.add(w[:-1])

pt.getWords("")

print "Execution time: ", time.time() - t0