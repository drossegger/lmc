#author: Dino Rossegger
from pyparsing import ParseResults
class Const(object):
	reprsymbol="Const"
	def __init__(self,t):
		if isinstance(t,list) or isinstance(t,ParseResults):
			self.label= ' '.join(t)
		else:
			self.label=t
	def __str__(self):
		return self.label
	def __eq__(self,other):
		return self.label == other.label

class UnOp(object):
	label="UnOp"
	def __init__(self,t):
		self.arg=t[0][1]
	def __str__(self):
		return self.reprsymbol + str(self.arg)

	def __eq__(self,other):
		return self.reprsymbol == other.reprsymbol and self.arg == other.arg

class BinOp(object):
	label="UnOp"
	def __init__(self,t):
		self.args=t[0][0::2]
		sep = " %s " % self.reprsymbol
		self.label="(" + sep.join(map(str,self.args)) + ")"
	def __str__(self):
		sep = " %s " % self.reprsymbol
		return "(" + sep.join(map(str,self.args)) + ")"

	def __eq__(self,other):
		return self.reprsymbol == other.reprsymbol and  self.args[0] == other.args[0] and self.args[1] == other.args[1]
		#CAUTION

class Andltl(BinOp):
	reprsymbol="&"
class Orltl(BinOp):
	reprsymbol="|"
class Fltl(UnOp):
	reprsymbol="F"
class Gltl(UnOp):
	reprsymbol="G"
class Xltl(UnOp):
	reprsymbol="X"
class Negltl(UnOp):
	reprsymbol="~"
class Ultl(BinOp):
	reprsymbol="U"
class Vltl(BinOp):
	reprsymbol="V"
class Impltl(BinOp):
	reprsymbol="->"






