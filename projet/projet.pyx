#!/usr/bin/python
import time
import sys
from sys import stdout
import os

ALPHABET_SIZE = 43
DEBUG = 0
#todo Cpt de NIL et de hauteur a update directement dans l'ajout
#todo comonPrefix

def addAllFiles(tree):
	t = time.time()
	s=35*" "
	for file in os.listdir("Shakespeare"):
		with open("Shakespeare/"+file) as f:
			stdout.flush()
			stdout.write("\r%s" % s)
			stdout.write("\r%s" % "Processing "+file+"...")
			stdout.flush()
			for w in f.readlines():
				tree.add(w[:-1])
		# break #A SUPPRIMER
	stdout.write("\r%s" % s)
	stdout.write("\r%s" % "All files added in "+str(tree.__class__.__name__)+" in "+str(time.time()-t)+" sec\n")

def statsTrie(tree):
	print str(tree.__class__.__name__)+" :"
	print "   words : ",tree.wordCount
	print "   height: ",tree.getHeight()
	print "   Nils  : ",tree.getNilptr(),"\n"

############################
####### PatriciaTree #######
############################

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
	elif char=='$':
		return 40
	elif char=='(':
		return 41
	elif char==')':
		return 42
	else:
		print 'PANIC : '+char+'non connu'

def comonPrefix(str1, str2):
	minStr = str1 if len(str1) <= len(str2) else str2
	for i in range(len(minStr)):
		if str2[i]:
			if str1[i]!=str2[i]:
				return minStr[:i]
	return minStr
	
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
					self.children[getIdWord(strpre)] = PatriciaTree()
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

	def printWords(self, word=""):
		for k in self.key:
			if k:
				if k[-1:] == '_':
					print word + k[:-1]
				else:
					if self.children[getIdWord(k)]:
						self.children[getIdWord(k)].printWords(word + k)

	def listWords(self):
		L=[]
		self.listsWords(L, word="")
		return L

	def listsWords(self, L, word=""):
		for k in self.key:
			if k:
				if k[-1:] == '_':
					L.append(word + k[:-1])
				else:
					if self.children[getIdWord(k)]:
						self.children[getIdWord(k)].listsWords(L, word + k)

	def countWordsRec(self):
		nb = 0
		for k in self.key:
			if k:
				if k[-1:] == '_':
					nb+=1
				else:
					if self.children[getIdWord(k)]:
						nb+=self.children[getIdWord(k)].countWordsRec()
		return nb

	def prefixCount(self, word):
		if word == "" and self.key[0] == '_':
			return self.countWordsRec()
		mykey = self.key[getIdWord(word)]
		if mykey == None:
			return 0
		elif self.key[getIdWord(word)][:-1] == word:
			return self.countWordsRec()
		elif self.children[getIdWord(mykey)] == None:
			return 0
		else:
			prefix = comonPrefix(self.key[getIdWord(word)], word)
			word = word[len(prefix):]
			return self.children[getIdWord(mykey)].search(word)

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

	def merge(self, pt):
			for i, val in enumerate(self.key):
				if not pt.key[i]:
					continue
				#Si il y a une clefs dans pt mais pas dans self
				if pt.key[i] and not val:
					self.key[i] = pt.key[i]
					self.children[i] = pt.children[i]
				#Si clef identique on merge les deux fils si ils existent
				elif self.key[i] == pt.key[i]:
					if DEBUG: print "EGAL"
					if self.children[i]:
						self.children[i].merge(pt.children[i])
				else:
					strpre = comonPrefix(self.key[i], pt.key[i])
					suffixkey=self.key[i][len(strpre):]
					suffixpt=pt.key[i][len(strpre):]
					if DEBUG: print "merge de: ", self.key[i], pt.key[i], "strpre =", strpre, " suffixkey =", suffixkey, " suffixpt =", suffixpt
					pt2 = PatriciaTree()
					if len(suffixkey) == 0:
						if DEBUG: print "len(suffixkey) = 0"
						pt2.key[getIdWord(suffixpt)] = suffixpt
						pt2.children[getIdWord(suffixpt)] = pt.children[i]
						if self.children[i].key[getIdWord(suffixpt)]:
							if DEBUG: print "A"
							self.children[i].merge(pt2)
						else:
							if DEBUG: print "B"
							self.children[i].key[getIdWord(suffixpt)] = suffixpt
							self.children[i].children[getIdWord(suffixpt)] = pt.children[i]

					elif len(suffixpt) == 0:
						if DEBUG: print "len(suffixpt) = 0"
						pt2.key[getIdWord(suffixkey)] = suffixkey
						pt2.children[getIdWord(suffixkey)] = self.children[i]
						if pt.children[i].key[getIdWord(suffixkey)]:
							if DEBUG: print "A"
							pt.children[i].merge(pt2)
						else:
							if DEBUG: print "B"
							pt.children[i].key[getIdWord(suffixkey)] = suffixkey
							pt.children[i].children[getIdWord(suffixkey)] = self.children[i]
						self.children[i] = pt.children[i]
						self.key[i] = strpre
					else:
						if DEBUG: print "LAST"
						pt2.children[getIdWord(suffixkey)] = self.children[i]
						pt2.key[getIdWord(suffixkey)] = suffixkey
						pt2.children[getIdWord(suffixpt)] = pt.children[i]
						pt2.key[getIdWord(suffixpt)] = suffixpt
						self.key[i] = strpre
						self.children[i] = pt2

	def toDot(self):
		print  "digraph graphname {	rankdir=LR splines=polyline; node [shape=record, height=0.02, fontsize=8];"
		self.toDotKeys(0)
		print "}"

	#nodeId est un identifiant non utilise de noeud
	def toDotKeys(self, nodeId):
		mySons = ""
		myID = nodeId
		nodeId+=1
		cpt = 1
		dotcode = "node" + str(myID) + "[label = \""
		for i, k in enumerate(self.key):
			if k:
				#Ajout de la clefs dans le noeud
				dotcode+= "<f" + str(cpt) + "> " + k + "|"
				#Appel recursive pour cree le noeud fils
				if self.children[i]:
					idtmp = self.children[i].toDotKeys(nodeId)
					mySons += "node" + str(myID) + ":f" + str(cpt) + " -> node" + str(nodeId) + "\n"
					nodeId = idtmp
				cpt+=1
		print dotcode[:-1] + "\"];"
		print mySons
		return nodeId+1

##########################
####### HybridTrie #######
##########################

class HybridTrie(object):

	def __init__(self):
		self.key = [None] * 2  #Key, value
		self.children = [None] * 3  #Inf, Eq, Sup
		self.wordCount = 0

	def add(self, word):
		if self.addrec(word, self.wordCount):
			if DEBUG: print "Ajout de "+word+" reussi !"
			self.wordCount+=1
		else:
			if DEBUG: print "Ajout de "+word+" echoue !"
		if DEBUG: print "FIN ADD"

	def addrec(self, word, value):
		#Si le noeud est vide
		if not self.key[0]:
			#On initialise les sous arbres
			self.children[0]=HybridTrie()
			self.children[1]=HybridTrie()
			self.children[2]=HybridTrie()
			#Si le mot est de longueur 1 : on l'ajoute et on cree les 3 sous arbres vides
			if len(word)==1:
				if DEBUG: print "Ajout du car "+word+" dans un arbre vide"
				self.key[0]=word[:1]
				self.key[1]=value
				return True
			#Si le mot est plus long que 1
			else:
				if DEBUG: print "Ajout du mot "+word+" dans un arbre vide, ajout de la cle "+word[:1]
				self.key[0]=word[:1]
				return self.children[1].addrec(word[1:], value)
		#Si l'arbre n'est pas vide
		else:
			#On initialise les sous arbres
			#Si le mot commence par une lettre inferieure a la cle du noeud
			if word[:1]<self.key[0]:
				if DEBUG: print "Ajout du mot "+word+" dans le sous arbre gauche"
				return self.children[0].addrec(word, value)

			#Si le mot commence par une lettre superieure a la cle du noeud
			elif word[:1]>self.key[0]:
				if DEBUG: print "Ajout du mot "+word+" dans le sous arbre droit"
				return self.children[2].addrec(word, value)

			#Si le mot commence par la meme lettre que le noeud
			else:
				if DEBUG: print "Ajout du mot "+word+" dans le sous arbre central"
				if len(word)==1:
					if not type(self.key[1])==int:
						self.key[1]=value
						return True
					if DEBUG: print "echec"
					return False
				else:
					return self.children[1].addrec(word[1:], value)
		
	def printsearch(self, word):
		res=self.searchValue(word)
		print 'Searching for "'+word+'"...', 
		if type(res)==int:
				print "Successful ! ID=",res
		else:
			if res:
				print "Successful !"
			else:
				print "Failed !"

	#Return word's value word exists, else False
	def searchValue(self, word):
		if not self.key:
			return False
		if len(word)==1:
			return self.key[1]
		else:
			if word[:1]==self.key[0]:
				if self.children[1]:
					return self.children[1].searchValue(word[1:])
				else:
					return False
			elif word[:1]>self.key[0]:
				if self.children[2]:
					return self.children[2].searchValue(word[1:])
				else:
					return False
			elif word[:1]<self.key[0]:
				if self.children[0]:
					return self.children[0].searchValue(word[1:])
				else:
					return False
			else:
				print "SEARCH ERROR"

	#Return True if word exists, else False
	def searchBool(self, word):
		if not self.key:
			return False
		if len(word)==1:
			return self.key[1]
		else:
			if word[:1]==self.key[0]:
				if self.children[1]:
					return self.children[1].searchBool(word[1:])
				else:
					return False
			elif word[:1]>self.key[0]:
				if self.children[2]:
					return self.children[2].searchBool(word[1:])
				else:
					return False
			elif word[:1]<self.key[0]:
				if self.children[0]:
					return self.children[0].searchBool(word[1:])
				else:
					return False
			else:
				print "SEARCH ERROR"

	#Return the words in the Trie in alphabetical order
	def listWords(self):
		L=[]
		self.listsWords(L, word="")
		return L

	def listsWords(self, L, word):
		if self.key[0]:
			word+=self.key[0]
			if type(self.key[1])==int:
				L.append(word)
			self.children[0].listsWords(L,word[:-1])
			self.children[1].listsWords(L,word)
			self.children[2].listsWords(L,word[:-1])

	def printWords(self):
		for i in self.listWords():
			print i

	def getNilptr(self):
		n = 0;
		for c in self.children:
			if c:
				n+=c.getNilptr()
			else:
				n+=1
		return n

	def getHeight(self):
		h = 0;
		for i in range(3):
			c=self.children[i]
			if c:
				hc=c.getHeight()
				if hc+1 > h:
					h=hc+1
		return h

	def display(self, n=0):
		print self.key,
		for x in range(n):
			print "\t",
		if self.children[0]:
			n+=1
			print self.children[0].display(n),
		if self.children[1]:
			n+=1
			print self.children[1].display(n),
		if self.children[2]:
			n+=1
			print self.children[2].display(n),
		print "\n"

	def toDot(self):
		print  "digraph graphname {	rankdir=LR splines=polyline; node [shape=record, height=0.02, fontsize=8];"
		self.toDotKeys(0)
		print "}"



	#nodeId est un identifiant non utiliser de noeud
	def toDotKeys(self, nodeId):
		mySons = ""
		myID = nodeId
		nodeId+=1
		cpt = 1
		dotcode = "node" + str(myID) + "[label = \""







		for i, k in enumerate(self.key):
			if k:
				#Ajout de la clefs dans le noeud
				dotcode+= "<f" + str(cpt) + "> " + k + "|"
				#Appel recursive pour cree le noeud fils
				if self.children[i]:
					idtmp = self.children[i].toDotKeys(nodeId)
					mySons += "node" + str(myID) + ":f" + str(cpt) + " -> node" + str(nodeId) + "\n"
					nodeId = idtmp
				cpt+=1
		print dotcode[:-1] + "\"];"
		print mySons
		return nodeId+1


#######################
####### M A I N #######
#######################

t0 = time.time()
pt = PatriciaTree()
pt2 = PatriciaTree()

# pt.add("boobs")
# pt.add("booboo")
# pt.add("boobies")
# addAllFiles(pt)


# with open("Shakespeare/1henryvi.txt") as f:
# 	for w in f.readlines():
# 		pt.add(w[:-1])
#
# pt.printWords("")
#pt.toDot()

ht=HybridTrie()
# ht.add("abc")
# ht.add("bca")
# ht.add("cba")
# ht.add("[oui]$")
# ht.add("$")
# ht.add("2d")
# ht.add("wordCount")
# ht.add("displayRacine")
# ht.add("else")
# ht.add("zo")
# ht.displayRacine()
# ht.add("abcd")
# ht.printsearch("abc")
# ht.add("abc")
#ht.key[0]='a'
#ht.children=HybridTrie()
#ht.children.key[0]='b'
# ht.display()


# print len(ht.listWords())
# Lpt=pt.listWords()
# print "Dans pt mais pas dans ht :\n",sorted(list(set(Lpt)-set(Lht)))
# print "Dans ht mais pas dans pt :\n",sorted(list(set(Lht)-set(Lpt)))	

# print ht.wordCount
# print pt.wordCount

addAllFiles(ht)
statsTrie(ht)
addAllFiles(pt)
statsTrie(pt)

# print "pt's Height :",pt.getHeight()

print "Total execution time: ", time.time() - t0