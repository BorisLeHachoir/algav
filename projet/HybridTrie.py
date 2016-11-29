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
			self.wordCount+=1
		if DEBUG: print "FIN ADD"

	def addrec(self, word, value):
		ht=HybridTrie()
		#Si l'arbre est vide
		if not self.key[0]:
			#Si le mot est de longueur 1 : on l'ajoute
			if len(word)==1:
				if DEBUG: print "Ajout mot a 1 caractere dans un arbre vide"
				ht.key[0]=word[:1]
				ht.key[1]=value
			#Si le mot est plus long que 1
			else:
				if DEBUG: print "Ajout mot dans un arbre vide"
				ht.key[0]=word[:1]
				ht.children[1]=HybridTrie()
				ht.children[1]=ht.children[1].addrec(word[1:], value)
		#Si l'arbre n'est pas vide
		else:
			#Si le mot commence par une lettre inferieure a la cle de la racine
			if word[:1]<self.key[0]:
				if DEBUG: print "Ajout du mot ",word," dans le sous arbre gauche"
				ht.key[0]=self.key[0]
				ht.key[1]=self.key[1]
				ht.children[0]=HybridTrie()
				ht.children[0]=ht.children[0].addrec(word, value)
				ht.children[1]=self.children[1]
				ht.children[2]=self.children[2]
			#Si le mot commence par une lettre superieure a la cle de la racine
			elif word[:1]>self.key[0]:
				if DEBUG: print "Ajout du mot ",word," dans le sous arbre droit"
				ht.key[0]=self.key[0]
				ht.key[1]=self.key[1]
				ht.children[0]=self.children[0]
				ht.children[1]=HybridTrie()
				ht.children[2]=HybridTrie()
				ht.children[2]=ht.children[2].addrec(word, value)
			else:
				if DEBUG: print "Ajout du mot ",word," dans le sous arbre central"
				ht.key[0]=self.key[0]
				ht.key[1]=self.key[1]
				ht.children[0]=self.children[0]
				ht.children[1]=HybridTrie()
				ht.children[1]=ht.children[1].addrec(word, value)
				ht.children[2]=HybridTrie()
		return ht

