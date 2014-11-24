#author: Dino Rossegger
from Graph import *
from LTLFormula import *
from collections import deque

name=0
I=[]
F=[]

V1=[]
V2=[]
AccStates=[]
counter=0
size=0
def new_name():
	global name
	name+=1
	return name-1

def expand(vertex,vertices):
	global I
	global F 
	if vertex.new:
		n=vertex.new.pop()
		if isinstance(n,Const): #checked
			if isinstance(n,Const) and n.label=="False":
				return vertices
			#if vertex.old.count(Negltl([["~",n]])):
				#return vertices
			for v in vertex.old:
				if isinstance(v,Negltl) and v.arg==n:
					return vertices
			vertex.old.append(n)
			vertex.oldSym.append(n)
			return expand(vertex,vertices)
		if isinstance(n,Negltl): #checked
			for v in vertex.old:
				if isinstance(v,Const) and v==n.arg:
					return vertices
			vertex.old.append(n)
			vertex.oldSym.append(n)
			return expand(vertex,vertices)
		if isinstance(n,Orltl):
			v1=Vertex(name=new_name(),father=vertex.name,pre=vertex.pre,new=[],old=vertex.old,next=vertex.next, oldSym=vertex.oldSym)
			v2=Vertex(name=new_name(),father=vertex.name,pre=vertex.pre,new=[] ,old=vertex.old,next=vertex.next, oldSym=vertex.oldSym)
			v1.new=list(set(vertex.new) | set([n.args[0]] if n.args[0] not in vertex.old else []))
			v1.old.append(n)
			v2.new=list(set(vertex.new) | set([n.args[1]] if n.args[1] not in vertex.old else []))
			v2.old.append(n)
			for i in I:
				if vertex==i:
					I.append(v1)
					I.append(v2)
					break
			return expand(v1,expand(v2,vertices))
		if isinstance(n,Ultl):
			F.append(n)
			v1=Vertex(name=new_name(),father=vertex.name,pre=vertex.pre,new=[],old=vertex.old,next=vertex.next, oldSym=vertex.oldSym)
			v2=Vertex(name=new_name(),father=vertex.name,pre=vertex.pre,new=[],old=vertex.old,next=vertex.next, oldSym=vertex.oldSym)
			v1.new=list(set(vertex.new) | set([n.args[0]] if n.args[0] not in vertex.old else []))
			v2.new=list(set(vertex.new) | set([n.args[1]] if n.args[1] not in vertex.old else []))
			v1.next.append(n)
			v1.old.append(n)
			v2.old.append(n)
			for i in I:
				if vertex==i:
					I.append(v1)
					I.append(v2)
					break
			return expand(v1,expand(v2,vertices))
		if isinstance(n,Vltl):
			v1=Vertex(name=new_name(),father=vertex.name,pre=vertex.pre,new=[],old=vertex.old,next=vertex.next, oldSym=vertex.oldSym)
			v2=Vertex(name=new_name(),father=vertex.name,pre=vertex.pre,new=[],old=vertex.old,next=vertex.next, oldSym=vertex.oldSym)
			
			v1.new=list(set(vertex.new) | set([item for item in [n.args[0],n.args[1]] if item not in vertex.old]))
			v2.new=list(set(vertex.new) | set([n.args[1]] if n.args[1] not in vertex.old else []))
			v1.old.append(n)
			v2.old.append(n)
			v2.next.append(n)
			for i in I:
				if vertex==i:
					I.append(v1)
					I.append(v2)
					break
			return expand(v1,expand(v2,vertices))
		if isinstance(n,Andltl):
			vertex.new.append(n.args[0])
			vertex.new.append(n.args[1])
			vertex.old.append(n)
			return expand(vertex,vertices)
		if isinstance(n,Xltl):
			vertex.old.append(n)
			vertex.next.append(n.arg)
			return expand(vertex,vertices)
	else:
		for i in vertices:
			if i.old == vertex.old and i.next == vertex.next:
				i.pre.extend(vertex.pre)
				#i.succ.extend(vertex.succ)
				return vertices
		vertices.append(vertex)

		return expand(Vertex(name=new_name(),pre=[vertex],new=vertex.next,old=[],next=[]),vertices)




def create_buchi(f):
	global I
	global F
	v=Vertex(name=new_name(), pre=[Init()], new=[f])
	I.append(v)
	S=expand(v,deque())
	AccStates=dict()
	F=list(set(F))
	for i in F:
		AccStates[i]=[]
	for i in F:
		for s in S:
			if i not in s.old or i.args[1] in s.old:
					AccStates[i].append(s)
	
	InitialStates=[]
	for s in S:
		if Init() in s.pre:
			InitialStates.append(s)
		for x in S:
			if s in x.pre:
				s.addSucc(x)
	return S,InitialStates,AccStates,len(F)

def myLength(a,b):
	return b[1]-a[1]

def addMod(x,y,modul):
	return (x+y)%modul


def viablePair(left,right):
	true=Const("")
	true.label="True"
	if true in left.oldSym:
		return True
	for lit in left.oldSym:
		if isinstance(lit,Negltl):
			if lit.arg in right.old:
				return False
		if isinstance(lit,Const):
			if lit not in right.old:
				return False
	return True

class Pair(object):
	def __init__(self,l,k,counter=0,visited=False):
		self.l=l
		self.k=k
		self.counter=counter
		self.visited=visited
	def __eq__(self,other):
		return self.l==other.l and self.k==other.k

def checkRec(x,track):
	global V1
	global counter
	lsucc=x.l.succ
	ksucc=x.k.succ
	if x.l in AccStates[counter]:
		counter=addMod(counter,1,size)
	x.visited=True
	V1.append(x)

	succCounter=0
	for lcand in lsucc:
		for kcand in ksucc:
			n=Pair(l=lcand,k=kcand,counter=counter)
			if viablePair(lcand,kcand) and n not in V1:
				succCounter+=1
				track.append(x.k)
				result=checkRec(n,track)
				if result != False:
					return result
				
	if succCounter==0:
		if x.counter==0 and x.l in AccStates[0]:
			result=checkFair(x,x,track)
			if result != False:
				return result

	return False

def checkFair(v,x,track):
	global V2
	global counter
	track.append(v.k)
	V2.append(v)

	if v.l in AccStates[counter]:
		counter=addMod(counter,1,size)
	if x.l in v.l.succ and x.k in v.k.succ and counter==0:
		return track 
	for lcand in v.l.succ:
		for kcand in v.k.succ:
			new=Pair(lcand,kcand)
			if viablePair(lcand,kcand) and new not in V2:
				new.counter=counter
				result=checkFair(new,x,track)
				if result != False:
					return result
	return False





		

def check(ltl,K):
	global AccStates
	global size
	States,IStates,AStates,size=create_buchi(ltl)
	#print "LTL Buchi:"
	#for s in States:
	#	print "  %s"%s
	#print "Accepting States:"
	#for a in AStates.values():
	#	for i in a:
	#		print "  %s"%i 
	#print "Kripke Structure:"

	#for k in K:
	#	print "  %s"%k
	counter=0
	AStates=AStates.values()
	if not AStates:
		AStates=[States]
		size=1
	AccStates=AStates
	KIState=K[0]

	S=deque()
	for i in IStates:
		if viablePair(i,KIState):
			#S.append((i,KIState,0))
			S.append(Pair(i,KIState))
		
	for s in S:
		result=checkRec(s,[])
		if result!=False:
			return result
	return False

	
	#while S:
	#	x=S.pop()
	#	lsucc=x[0].succ
	#	ksucc=x[1].succ
	#	if x[0] in AStates[counter]:
	#		counter=addMod(counter,1,size)
	#	succCounter=0
	#	ce.append(x[1])

	#	for lcand in lsucc:
	#			for kcand in ksucc:
	#				if viablePair(lcand,kcand) and (lcand,kcand) not in V1:
	#					V1.append((lcand,kcand))
	#					S.append((lcand,kcand,counter))
	#					succCounter+=1
	#	if succCounter==0:
	#		if x[2]==0 and x[0] in AStates[0]:
	#			S2.append(x)
	#			while S2:
	#				v=S2.pop()
	#				lsucc=v[0].succ
	#				ksucc=v[1].succ
	#				
	#				if v[0] in AStates[counter]:
	#					counter=addMod(counter,1,size)
	#				if x[0] in lsucc and x[1] in ksucc and counter==0:
	#					return ce
	#				for lcand in lsucc:
	#						for kcand in ksucc:
	#							if viablePair(lcand,kcand) and (lcand,kcand) not in V2:
	#								V2.append((lcand,kcand))
	#								S2.append((lcand,kcand,counter))
	#return False			




	

	


	
	
