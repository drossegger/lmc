#author: Dino Rossegger
from LTLFormula import *
from collections import deque
from pyparsing import (infixNotation, opAssoc, Keyword, Word, alphas,nestedExpr)

negop="~"
fop="F"
gop="G"
xop="X"
andop="&"
orop="|"
impop="->"
uop="U"
vop="V"

def nnf(f):
	if isinstance(f,Const):
		return f
	if isinstance(f,Fltl):
		return nnf(Ultl([[Const(["True"]),uop,f.arg]]))
	if isinstance(f,Gltl):
		return nnf(Negltl([[negop,Fltl([[fop,Negltl([[negop,f.arg]])]])]]))
	if isinstance(f,Xltl):
		return Xltl([[xop,nnf(f.arg)]])
	if isinstance(f,Negltl):
		if isinstance(f.arg,Fltl):
			return nnf(Negltl([[negop,nnf(f.arg)]]))
		if isinstance(f.arg,Gltl):
			sf2=f.arg.arg
			sf1=Negltl([[negop,sf2]])
			sf=Fltl([[fop,sf1]])
			return nnf(sf)
		if isinstance(f.arg,Negltl):
			return nnf(f.arg.arg)
		if isinstance(f.arg,Xltl):
			sf2=f.arg.arg
			sf1=Negltl([[negop,sf2]])
			sf=Xltl([[xop,sf1]])
			return nnf(sf)
		if isinstance(f.arg,Ultl):
			sfl=Negltl([[negop,f.arg.args[0]]])
			sfr=Negltl([[negop,f.arg.args[1]]])
			return nnf(Vltl([[sfl,vop,sfr]]))
		if isinstance(f.arg,Vltl):
			sfl=Negltl([[negop,f.arg.args[0]]])
			sfr=Negltl([[negop,f.arg.args[1]]])
			return nnf(Ultl([[sfl,uop,sfr]]))
		if isinstance(f.arg,Const):
			if f.arg.label=="True":
				f.arg.label="False"
				return f.arg
			elif f.arg.label=="False":
				f.arg.label="True"
				return f.arg
			return f
		if isinstance(f.arg,Andltl):
			sfl=Negltl([[negop,f.arg.args[0]]])
			sfr=Negltl([[negop,f.arg.args[1]]])
			return nnf(Orltl([[sfl,orop,sfr]]))
		if isinstance(f.arg,Orltl):
			sfl=Negltl([[negop,f.arg.args[0]]])
			sfr=Negltl([[negop,f.arg.args[1]]])
			return nnf(Andltl([[sfl,orop,sfr]]))
		if isinstance(f.arg,Impltl):
			sfl=f.arg.args[0]
			sfr=Negltl([[negop,f.arg.args[1]]])
			#print Andltl([[sfl,andop,sfr]])
			return nnf(Andltl([[sfl,andop,sfr]]))
			

	if isinstance(f,Ultl):
		return Ultl([[nnf(f.args[0]),uop,nnf(f.args[1])]])

	if isinstance(f,Vltl):
		return Vltl([[nnf(f.args[0]),vop,nnf(f.args[1])]])

	if isinstance(f,Andltl):
		return Andltl([[nnf(f.args[0]),andop,nnf(f.args[1])]])
	if isinstance(f,Orltl):
		return Orltl([[nnf(f.args[0]),andop,nnf(f.args[1])]])
	if isinstance(f,Impltl):
		sfl=Negltl([[negop,f.args[0]]])
		return Orltl([[nnf(sfl),orop,nnf(f.args[1])]])


def parseLTL(s):
	TRUE = Keyword("True")
	FALSE = Keyword("False")
	symbol = TRUE | FALSE | Word("abcdefghijklmnopqrstuvwxyz")
	equation = symbol + "==" + symbol | symbol + "<" + symbol | symbol

	symbol.setParseAction(Const)

	expr= infixNotation(symbol,
			[
				(negop, 1, opAssoc.RIGHT, Negltl),
				(fop, 1, opAssoc.RIGHT, Fltl),
				(gop, 1, opAssoc.RIGHT, Gltl),
				(xop, 1, opAssoc.RIGHT, Xltl),
				(andop, 2, opAssoc.RIGHT, Andltl),
				(orop, 2, opAssoc.RIGHT, Orltl),
				(impop, 2, opAssoc.RIGHT, Impltl),
				(uop, 2, opAssoc.RIGHT, Ultl),
				(vop, 2, opAssoc.RIGHT, Vltl)
			])
	return expr.parseString(s)[0]

#def parsePrefix(s):
	#s=s.lstrip()
	#if s[0]=="(":
	#	s=s.lstrip("(")
	#	s=s.rstrip(")")
	#if s[0]==negop:
	#	return Negltl([[negop,parsePrefix(s[1:])]])
	#if s[0]==fop:
	#	return Fltl([[fop,parsePrefix(s[1:])]])
	#if s[0]==gop:
	#	return Gltl([[gop,parsePrefix(s[1:])]])
	#if s[0]==andop:
