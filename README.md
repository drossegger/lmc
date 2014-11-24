Usage:

./lmc -i PATH_TO_KRIPKE_STRUCTURE LTLFORMULA

Outputs YES (exitcode 10), if the Kripke Structure satisfies the formula and a counterexample (exitcode 20) as transitions if it does not.

You can find a few kripke structures in the directory testcases.

Use the following symbols to define your LTL Formulas:
not		~
and		&
or		|
impl	->
U			U
V/R		V
F			F
G			G

For examples look at testcases.csv. To execute the testcases use ./test.sh

Requirements:
Python >= 2.7
module pyparsing >= 4.4 

