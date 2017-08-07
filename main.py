import pynorm
import sys

cols = int(sys.argv[1])

while True:
	inpt = raw_input("Enter dependencies with '-' split by ' ' (ex. 1-23 2-3)... ")
	if not pynorm.ValidCheck(cols, inpt): break

graph = pynorm.BuildGraph(inpt, cols)
cands = pynorm.CalCands(graph)
print "The Table's Candidate Key(s) are: ", cands

nrml_form, cause = pynorm.CatNF(cands, inpt)
print "The Table's Normal Form is: ", nrml_form

if(cause is not None):
	print "Because of the Functional Depedence: ", cause