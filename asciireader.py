#author: Dino Rossegger
from Graph import Vertex
import ltlparser as ltlp
def createGraph(adjmatrix):
	vertices=dict()
	for l in range(len(adjmatrix)):
		vertices[l]=(Vertex(name=l,father=l,pre=[], new=[]))
	for l in range(len(adjmatrix)):
		for i in range(len(adjmatrix)):
			if adjmatrix[l][i]=='1':
				vertices[l].addSucc(vertices[i])
				vertices[i].addPre(vertices[l])
	return vertices



def genKripke(f):
	f=f.read().splitlines()
	size=int(f[0])
	incmatrix=f[2:size+2]
	incmatrix=[l.split(' ') for l in incmatrix]
	vertices=createGraph(incmatrix)
	predstart=size+3
	predend=size+3

	for l in f[predstart:]:
		if l[0]=="-" and l[1]=="-":
			break
		else:
			predend+=1
	pred=f[predstart:predend]
		

	for l in pred:
		l=l.split("->")
		p=l[1].strip().strip("{}")
		p=p.split(",")
		for literal in p:
			if literal!="":
				x=ltlp.parseLTL(literal)
				vertices[int(l[0])].addOld(x)
	return vertices.values()



