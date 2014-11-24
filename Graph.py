#author: Dino Rossegger
from collections import deque
class Vertex(object):
	def __init__(self, name, pre, new, father=None,old=[],next=[],succ=[],oldSym=[]):
		self.name=name
		self.succ=deque(succ)
		self.pre=deque(pre)
		self.new=deque(new)
		self.oldSym=deque(oldSym)
		if father==None:
			self.father=name
		else:
			self.father=father
		self.old=deque(old)
		self.next=deque(next)
	def __str__(self):
		string=":"
		for i in self.pre:
			string+=str(i.name)+" "
		string +=":"
		for i in self.succ:
			string+=str(i.name) +" "
		string+=":"
		for i in self.old:
			string+=str(i)+","
		string+=":"
		for i in self.oldSym:
			string+=str(i)+","
		return str(self.name)+string
	def ce(self):
		return self.name
	def __eq__(self,other):
		return self.name == other.name
	def addPre(self,v):
		self.pre.append(v)
	def addOld(self,o):
		self.old.append(o)
	def addSucc(self,v):
		self.succ.append(v)
class Init(Vertex):
	def __init__(self):
		self.name="init"
