#!/usr/bin/python
#author: Dino Rossegger
from LTLFormula import *
import checkRoutines as cr,asciireader as ar,argparse as ap, ltlparser as ltlp, sys

clip=ap.ArgumentParser(description="LTL Model Checker")
clip.add_argument("-i",help="path to the Kripke Structure in ASCII")
clip.add_argument("ltlformula")

args=clip.parse_args()
ltl=ltlp.parseLTL(args.ltlformula)
#print "Parsed LTL Formula: %s"%ltl
nnfltl=ltlp.nnf(Negltl([["x",ltl]]))
#print "NNF Translation: %s"%nnfltl
kripkestruct=ar.genKripke(open(args.i))
ce=cr.check(nnfltl,kripkestruct)
if not ce:
	print "YES, the Kripkestructure satisfies the property"
	sys.exit(10)
else:
	print "NO, the Kripkestructure does not satisfy the property"
	cestring="->".join([str(i.ce()) for i in ce ])
	print "Counterexample: %s"%cestring
	sys.exit(20)
