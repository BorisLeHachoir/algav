#!/usr/bin/python
import time
import sys
from sys import stdout
import os
import multiprocessing
from multiprocessing import Process, Queue

def addAllShakespeareFiles(tree):
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
	stdout.write("\r%s" % s)
	stdout.write("\r%s" % "All Shakespeare files added in "+str(tree.__class__.__name__)+" in "+str(time.time()-t)+" sec\n")

def addOneShakespeareFile(tree):
	t = time.time()
	s=35*" "
	with open("Shakespeare/comedy_errors.txt") as f:
		stdout.flush()
		stdout.write("\r%s" % s)
		stdout.write("\r%s" % "Processing comedy_errors.txt...")
		stdout.flush()
		for w in f.readlines():
			tree.add(w[:-1])
	stdout.write("\r%s" % s)
	stdout.write("\r%s" % "Shakespeare/comedy_errors.txt added in "+str(tree.__class__.__name__)+" in "+str(time.time()-t)+" sec\n")

def statsTrie(tree):
	print str(tree.__class__.__name__)+" :"
	print "   Words         : ",tree.getWordCount()
	print "   Max height    : ",tree.getHeight()
	print "   Average Depth : ",tree.averageDepth()
	print "   Nils Pointers : ",tree.getNilptr(),"\n"

def addExample(pt):
	phrase="a quel genial professeur de dactylographie sommes nous redevables de la superbe phrase ci dessous, un modele du genre, que toute dactylo connait par coeur puisque elle fait appel a chacune des touches du clavier de la machine a ecrire ?"
	for i in phrase.split(" "):
		pt.add(i)

############################
####### PatriciaTrie #######
############################

def comonPrefix(str1, str2):
	minStr = str1 if len(str1) <= len(str2) else str2
	for i in range(len(minStr)):
		if str2[i]:
			if str1[i]!=str2[i]:
				return minStr[:i]
	return minStr
	
class PatriciaTrie(object):
	def __init__(self):
		self.key = [None] * 128
		self.children = [None] * 128
		self.wordCount = 0

	#Add word
	def add(self, word):
		if self.addrec(word+'_'):
			self.wordCount+=1

	def addrec(self, word):
		#test word est vide
		if word[0] == '_':
			if not self.key[0]:
				self.key[0]='_'
				return True
			else:
				return False

		elif not self.key[ord(word[:1])]:
			self.key[ord(word[:1])] = word
			return True

		#Si il y a une clef deja presente
		else:
			strpre = comonPrefix(self.key[ord(word[:1])], word)
			suffixkey=self.key[ord(strpre[:1])][len(strpre):]
			suffixword=word[len(strpre):]
			oldkey=self.key[ord(strpre[:1])]
			self.key[ord(strpre[:1])] = strpre


			#cas ou la clef n'as aucun fils
			if oldkey[-1:] == '_':
				if strpre == oldkey:
					return False
				else:
					self.children[ord(strpre[:1])] = PatriciaTrie()
					self.children[ord(strpre[:1])].addrec(suffixkey)
					return self.children[ord(strpre[:1])].addrec(suffixword)
			#cas ou la clef a un fils
			else:
				#Si update de la key, on sauvegarde les anciens fils
				if strpre != oldkey:
					saveChildren = self.children[ord(strpre[:1])]
					self.children[ord(strpre[:1])] = PatriciaTrie()
					self.children[ord(strpre[:1])].children[ord(suffixkey[:1])] = saveChildren
					self.children[ord(strpre[:1])].addrec(suffixkey)
					return self.children[ord(strpre[:1])].addrec(suffixword)
				else:
					#On verifie si il existe un fils commencant par la meme lettre
					if not self.children[ord(strpre[:1])]:
						self.children[ord(strpre[:1])] = PatriciaTrie()
					#Si l'ancienne clef est prefixe du mot a ajouter
					if strpre == oldkey:
						return self.children[ord(strpre[:1])].addrec(suffixword)
					else:
						print "PANIC: strpre&oldkey"

	#Delete word
	def nbChildren(self):
		cpt = 0
		for c in self.children:
			if c:
				cpt+=1
		return cpt

	def delete(self, word):
		word += '_'
		if self.deleterec(word):
			self.wordCount-=1

	def deleterec(self, word):
		if word[0] == '_':
			if self.key[0] == '_':
				self.key[0] = None
				return True
			return False

		elif self.key[ord(word[:1])] == None:
			return False

		elif word == self.key[ord(word[:1])]:
			self.key[ord(word[:1])] = None
			return True

		else:
			idKey = ord(word[:1])
			myKey = self.key[idKey]
			strpre = comonPrefix(myKey, word)
			suffixword=word[len(strpre):]
			#Si la suppression a eu lieu et qu'il n'y a qu'un fils, on le remonte
			if self.children[idKey].deleterec(suffixword):
				if self.nbChildren() == 1:
					#recherche de notre fils
					for c in self.children:
						if c:
							#recherche de sa clef
							for k in c.key:
								if k:
									self.key[idKey] = myKey + k
									#On remonte d'un niveau ses fils si ils existent
									if c.children[ord(k[:1])]:
										self.children[idKey] = c.children[ord(k[:1])]	
				return True
			return False


	# Search word
	def printsearch(self, word):
		print "Recherche de: ", word, ": ", str(self.search(word))

	def search(self, word):
		if word == "" and self.key[0] == '_':
			return True
		if word == "":
			return False
		mykey = self.key[ord(word[:1])]
		if mykey == None:
			return False
		elif self.key[ord(word[:1])][:-1] == word:
			return True
		elif self.children[ord(mykey[:1])] == None:
			return False
		else:
			prefix = comonPrefix(self.key[ord(word[:1])], word)
			word = word[len(prefix):]
			return self.children[ord(mykey[:1])].search(word)


	# Lists words
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
					if self.children[ord(k[:1])]:
						self.children[ord(k[:1])].listsWords(L, word + k)

	# Counts words
	def countWordsRec(self):
		nb = 0
		for k in self.key:
			if k:
				if k[-1:] == '_':
					nb+=1
				else:
					if self.children[ord(k[:1])]:
						nb+=self.children[ord(k[:1])].countWordsRec()
		return nb

	# Counts words with same prefix
	def prefixCount(self, word):
		if word == "" and self.key[0] == '_':
			return self.countWordsRec()
		mykey = self.key[ord(word[:1])]
		if mykey == None:
			return 0
		elif self.key[ord(word[:1])][:-1] == word:
			return self.countWordsRec()
		elif self.children[ord(mykey[:1])] == None:
			return 0
		else:
			prefix = comonPrefix(self.key[ord(word[:1])], word)
			word = word[len(prefix):]
			return self.children[ord(mykey[:1])].search(word)

	# Word Count
	def getWordCount(self):
		return self.wordCount

	# Depth
	def isLeaf(self):
		for c in self.children:
			if c:
				return False
		return True

	def averageDepth(self):
		tab = []
		self.averageDepthRec(tab, 0)
		return float(sum(tab))/len(tab)

	def averageDepthRec(self, tab ,depth):
		if self.isLeaf():
			tab.append(depth)
		else:
			for c in self.children:
				if c:
					c.averageDepthRec(tab, depth+1)

	# Height
	def getHeight(self):
		h = 0;
		for c in self.children:
			if c:
				if c.getHeight()+1 > h:
					h =  c.getHeight()+1
		return h

	# Nils pointers
	def getNilptr(self):
		n = 0;
		for c in self.children:
			if c:
				n+= c.getNilptr()
			else:
				n+=1
		return n

	def merge(self, pt):
		self.mergeRec(pt)
		self.wordCount = self.countWordsRec()

	# Merge 2 PatriciaTries
	def mergeRec(self, pt):
		for i, val in enumerate(self.key):
			if not pt.key[i]:
				continue
			#Si il y a une clefs dans pt mais pas dans self
			if pt.key[i] and not val:
				self.key[i] = pt.key[i]
				self.children[i] = pt.children[i]
			#Si clef identique on merge les deux fils si ils existent
			elif self.key[i] == pt.key[i]:
				if self.children[i]:
					self.children[i].merge(pt.children[i])
			else:
				strpre = comonPrefix(self.key[i], pt.key[i])
				suffixkey=self.key[i][len(strpre):]
				suffixpt=pt.key[i][len(strpre):]
				pt2 = PatriciaTrie()
				if len(suffixkey) == 0:
					pt2.key[ord(suffixpt[:1])] = suffixpt
					pt2.children[ord(suffixpt[:1])] = pt.children[i]
					if self.children[i].key[ord(suffixpt[:1])]:
						self.children[i].merge(pt2)
					else:
						self.children[i].key[ord(suffixpt[:1])] = suffixpt
						self.children[i].children[ord(suffixpt[:1])] = pt.children[i]

				elif len(suffixpt) == 0:
					pt2.key[ord(suffixkey[:1])] = suffixkey
					pt2.children[ord(suffixkey[:1])] = self.children[i]
					if pt.children[i].key[ord(suffixkey[:1])]:
						pt.children[i].merge(pt2)
					else:
						pt.children[i].key[ord(suffixkey[:1])] = suffixkey
						pt.children[i].children[ord(suffixkey[:1])] = self.children[i]
					self.children[i] = pt.children[i]
					self.key[i] = strpre
				else:
					pt2.children[ord(suffixkey[:1])] = self.children[i]
					pt2.key[ord(suffixkey[:1])] = suffixkey
					pt2.children[ord(suffixpt[:1])] = pt.children[i]
					pt2.key[ord(suffixpt[:1])] = suffixpt
					self.key[i] = strpre
					self.children[i] = pt2

	# Display
	def display(self):
		dotFile=open("PatTrieDot", 'w')
		dotFile.write("digraph graphname { splines=polyline; node [shape=record, height=0.02, fontsize=8];\n")
		self.toDotKeys(0, dotFile)
		dotFile.write("}\n")
		dotFile.close()
		os.system('dot -Tpdf PatTrieDot -o PT.pdf')

	def toDotKeys(self, nodeId, dotFile):
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
					idtmp = self.children[i].toDotKeys(nodeId, dotFile)
					mySons += "node" + str(myID) + ":f" + str(cpt) + " -> node" + str(nodeId) + "\n"
					nodeId = idtmp
				cpt+=1
		dotFile.write(dotcode[:-1] + "\"];\n")
		dotFile.write(mySons)
		return nodeId+1

	def addMergeAllfiles(self):
		t = time.time()
		Lpat=[]
		s=35*" "
		for file in os.listdir("Shakespeare"):
			with open("Shakespeare/"+file) as f:
				Lpat.append(PatriciaTrie())
				stdout.flush()
				stdout.write("\r%s" % s)
				stdout.write("\r%s" % "Processing "+file+"...")
				stdout.flush()
				for w in f.readlines():
					Lpat[-1].add(w[:-1])
			stdout.write("\r%s" % s)
		# Pat=PatriciaTrie()
		for i in Lpat:
			self.merge(i)

	def addMergeAllfilesMultiprocessing(self):
		q = Queue()
		cpt = 0 
		for file in os.listdir("Shakespeare"):
			cpt+=1
			pt = PatriciaTrie()
			p = multiprocessing.Process(target=pt.addfile, args=("Shakespeare/"+file,q))
			p.start()
		for i in range(cpt):
			self.merge(q.get())

	def addfile(self, filename, q):
		with open(filename) as f:
			for w in f.readlines():
				self.add(w[:-1])	
			q.put(self)


	def PatToHyb(self):
		ht=HybridTrie()
 		L=self.listWords()
 		self.PatToHyb2Rec(ht, L)
 		return ht

	def PatToHybRec(self, ht, L):
		n=len(L)/2
		L1=L[:n]
		L2=L[n+1:]
		o=L[n]
		ht.add(o)
		if len(L1)>0:
			self.PatToHyb2Rec(ht, L1)
		if len(L2)>0:
			self.PatToHyb2Rec(ht, L2)

##########################
####### HybridTrie #######
##########################

class HybridTrie(object):

	def __init__(self):
		self.key = [None] * 2  #Key, value
		self.children = [None] * 3  #Inf, Eq, Sup
		self.wordCount = 0

	# Add word
	def add(self, word):
		if self.addrec(word, self.wordCount):
			self.wordCount+=1

	def addrec(self, word, value):
		#Si le noeud est vide
		if not self.key[0]:
			#On initialise les sous arbres
			self.children[0]=HybridTrie()
			self.children[1]=HybridTrie()
			self.children[2]=HybridTrie()
			#Si le mot est de longueur 1 : on l'ajoute et on cree les 3 sous arbres vides
			if len(word)==1:
				self.key[0]=word[:1]
				self.key[1]=value
				return True
			#Si le mot est plus long que 1
			else:
				self.key[0]=word[:1]
				return self.children[1].addrec(word[1:], value)
		#Si l'arbre n'est pas vide
		else:
			#On initialise les sous arbres
			#Si le mot commence par une lettre inferieure a la cle du noeud
			if word[:1]<self.key[0]:
				return self.children[0].addrec(word, value)

			#Si le mot commence par une lettre superieure a la cle du noeud
			elif word[:1]>self.key[0]:
				return self.children[2].addrec(word, value)

			#Si le mot commence par la meme lettre que le noeud
			else:
				if len(word)==1:
					if not type(self.key[1])==int:
						self.key[1]=value
						return True
					return False
				else:
					return self.children[1].addrec(word[1:], value)
		
	#Delete word
	def delete(self, word):
		if len(word)==0:
			self.key[1]=None
		for i in range(3):
			if self.children[i].key[0]==word[:1]:
				self.children[i].delete(word[1:])

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

	# Search word (return value)
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

	# Search word
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

	# List Words
	def listWords(self):
		L=[]
		self.listsWords(L)
		return L
	def listsWords(self, L, word=""):
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

	# Count Nils
	def getNilptr(self):
		n = 0
		for c in self.children:
			if c:
				n+=c.getNilptr()
			else:
				n+=1
		return n

	# Height
	def getHeight(self):
		h = 0
		for i in range(3):
			c=self.children[i]
			if c:
				hc=c.getHeight()
				if hc+1 > h:
					h=hc+1
		return h

	def getWordCount(self):
		return self.wordCount

	# Depth
	def averageDepth(self):
		L=self.listAverageDepth()
		return float(sum(L))/len(L)
	
	def listAverageDepth(self, n=0):
		L=[]
		for i in range(3):
			c=self.children[i]
			if c:
				L.extend(c.listAverageDepth(n+1))
			else:
				L.append(n)
		return L

	# Count Words with same prefix
	def prefixCount(self, word=""):
		if len(word)>0:
			if self.key[0]==word[:1]:
				return self.children[1].prefixCount(word[1:])
			elif self.key[0]<word[:1]:
				return self.children[2].prefixCount(word)
			elif self.key[0]>word[:1]:
				return self.children[0].prefixCount(word)
			else:
				return 0
		else:
			if type(self.key[1]==int):
				return len(self.listWords())+1
			return len(self.listWords())

	# Display
	def display(self):
		dotFile=open("HybTrieDot", 'w')
		dotFile.write("digraph graphname { splines=polyline; node [shape=record, height=0.02, fontsize=8];\n")
		self.toDotRec(0, dotFile)
		dotFile.write("}\n")
		dotFile.close()
		os.system('dot -Tpdf HybTrieDot -o HT.pdf')

	def toDotRec(self, myID, dotFile):
		newID = myID
		if self.key[0]:
			newID +=1
			strEndColor = ""
		if type(self.key[1])==int:
			strEndColor = "color=red "
		dotFile.write("node" + str(myID) + "[" + strEndColor + "label = \"<f1>|<f2> " + str(self.key[0]) + "|<f3>\"]\n")
		if self.children[0].key[0]:
			save = newID
			newID = self.children[0].toDotRec(newID, dotFile)
			dotFile.write("node" + str(myID) + ":f1 -> node" + str(save)+"\n")
		if self.children[1].key[0]:
			save = newID
			newID = self.children[1].toDotRec(newID, dotFile)
			dotFile.write("node" + str(myID) + ":f2 -> node" + str(save)+"\n")
		if self.children[2].key[0]:
			save = newID
			newID = self.children[2].toDotRec(newID, dotFile)
			dotFile.write("node" + str(myID) + ":f3 -> node" + str(save)+"\n")
		return newID

	def HybToPat(self):
		pt=PatriciaTrie()
		for i in self.listWords():
			pt.add(i)

	def balance(self):
		ht=HybridTrie()
		L=self.listWords()
		self.balanceRec(ht, L)
		return ht

	def balanceRec(self, ht, L):
		n=len(L)/2
		L1=L[:n]
		L2=L[n+1:]
		o=L[n]
		ht.add(o)
		if len(L1)>0:
			self.balanceRec(ht, L1)
		if len(L2)>0:
			self.balanceRec(ht, L2)

#####################
####### Tests #######
#####################

def PatriciaTrieExample():
	ptExample = PatriciaTrie()
	addExample(ptExample)
	ptExample.display()
	os.system('rm PatTrieDot')
	os.system('mv PT.pdf PatriciaTrieExample.pdf')
	print "PatriciaTrieExample.pdf created..."

def HybridTrieExample():
	htExample = HybridTrie()
	addExample(htExample)
	htExample.display()
	os.system('rm HybTrieDot')
	os.system('mv HT.pdf HybridTrieExample.pdf')
	print "HybridTrieExample.pdf created..."

def PatriciaTrieAllFiles():
	ptShakespeare=PatriciaTrie()
	addAllShakespeareFiles(ptShakespeare)
	statsTrie(ptShakespeare)
	print "Creating PatriciaTrieAllFiles.pdf... (may take a few minutes)"
	ptShakespeare.display()
	os.system('rm PatTrieDot')
	os.system('mv PT.pdf PatriciaTrieAllFiles.pdf')
	print "PatriciaTrieAllFiles.pdf created..."

def HybridTrieAllFiles():
	htShakespeare=HybridTrie()
	addAllShakespeareFiles(htShakespeare)
	statsTrie(htShakespeare)
	print "Creating HybridTrieAllFiles.pdf... (may take a few minutes)"
	htShakespeare.display()
	os.system('rm HybTrieDot')
	os.system('mv HT.pdf HybridTrieAllFiles.pdf')
	print "HybridTrieAllFiles.pdf created..."

def PatriciaTrieOneFile():
	ptShakespeare=PatriciaTrie()
	addOneShakespeareFile(ptShakespeare)
	statsTrie(ptShakespeare)
	print "Creating PatriciaTrieOneFile.pdf... (may take a few seconds)"
	ptShakespeare.display()
	os.system('rm PatTrieDot')
	os.system('mv PT.pdf PatriciaTrieOneFile.pdf')
	print "PatriciaTrieOneFile.pdf created..."

def HybridTrieOneFile():
	htShakespeare=HybridTrie()
	addOneShakespeareFile(htShakespeare)
	statsTrie(htShakespeare)
	print "Creating HybridTrieOneFile.pdf... (may take a few seconds)"
	htShakespeare.display()
	os.system('rm HybTrieDot')
	os.system('mv HT.pdf HybridTrieOneFile.pdf')
	print "HybridTrieOneFile.pdf created..."

def PatriciaTrieMerging():
	ptMerge=PatriciaTrie()
	ptMerge.addMergeAllfiles()
	print "\r",
	statsTrie(ptMerge)

def PatriciaTrieMergingMultiProcessing():
	ptMergeMP=PatriciaTrie()
	print "Creating PatriciaTrie by merges on multiprocess..."
	ptMergeMP.addMergeAllfilesMultiprocessing()
	statsTrie(ptMergeMP)

def HybridTrieBalancedExample():
	htExample=HybridTrie()
	addExample(htExample)
	htBalanced=htExample.balance()
	htBalanced.display()
	os.system('rm HybTrieDot')
	os.system('mv HT.pdf HybridTrieExampleBalanced.pdf')
	print "HybridTrieExampleBalanced.pdf created..."


#######################
####### M A I N #######
#######################

##### Initialisation du chrono #####
t0 = time.time()

##### Jeu de test #####

# PatriciaTrieExample()
# HybridTrieExample()

# PatriciaTrieAllFiles()
# HybridTrieAllFiles()

# PatriciaTrieOneFile()
# HybridTrieOneFile()

# PatriciaTrieMerging()
# PatriciaTrieMergingMultiProcessing()

# HybridTrieBalancedExample()

##### Affichage du chrono #####
print "Total execution time: ", time.time() - t0


