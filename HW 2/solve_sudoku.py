# -*- coding: utf-8 -*-

#####
# Name: Amee Joshipura
# Id: 260461226
###

import pdb #Use pdb.set_trace() to make a break in your code.
import numpy as np

###################
# Solve sudoku #
###################

#####
# reduce: Fonction used by AC3 to reduce the domain of Xi using constraints from Xj.
#
# Xi: Variable (tuple (Y,X)) with reduced domain, if possible.
#
# Xj: Variable (tuple (Y,X)) with reduced domain, if possible.
#
# csp: Object of class CSP containing all information relative to constraint 
#      satisfaction for Sudoku.
#
# return: A tuple containing a boolean indicating if there were changes to the domain, and the csp.
### 

def reduce(Xi, Xj, csp):
	revised = False
	count = 0
	for d in csp.domains[Xi]:
		for dj in csp.domains[Xj]:
			if not((d,dj) in csp.constraints[Xj]):
				count+=1
		if count==0:
			csp.domains[Xj].remove(d)
			revised = True
    return revised,csp



#####
# AC3: Function used to reduce the domain of variables using AC3 algorithm.
#
# csp: Object of class CSP containing all information relative to constraint 
#      satisfaction for Sudoku.
#
# return: A tuple containing the optimized csp and a boolean variable indicating if there are no violated constraints.
### 

def AC3(csp):
	arc = Queue()
	arc.put((Xi, Xj) for Xi in csp.constraints for Xj in csp.constraints[Xi])
	while not arc.empty():
		(Xi, Xj) = arc.get()
		if reduce(Xi,Xj,csp):
			if not csp.domains[Xi]:
				return csp,False
			for Xk in csp.variables:
				if (Xk not Xi) and (Xk not Xj):
					if Xk[0]==Xi[0]:
						arc.put((Xk,Xi))
					if Xk[1]==Xi[1]:
						arc.put((Xk,Xi))
					#column is 0-2, 3-5, 6-8
					#and row is 0-2, 3-5, 6-8
					if (Xk[0] in [0,1,2])and(Xi[0] in [0,1,2]):
						if (Xk[1] in [0,1,2]) and (Xi[1] in [0,1,2]):
							arc.put((Xk,Xi))
						else if (Xk[1] in [3,4,5]) and (Xi[1] in [3,4,5]):
							arc.put((Xk,Xi))
						else if (Xk[1] in [6,7,8]) and (Xi[1] in [6,7,8]):
							arc.put((Xk,Xi))
					else if (Xk[0] in [3,4,5])and(Xi[0] in [3,4,5]):
						if (Xk[1] in [0,1,2]) and (Xi[1] in [0,1,2]):
							arc.put((Xk,Xi))
						else if (Xk[1] in [3,4,5]) and (Xi[1] in [3,4,5]):
							arc.put((Xk,Xi))
						else if (Xk[1] in [6,7,8]) and (Xi[1] in [6,7,8]):
							arc.put((Xk,Xi))
					else if (Xk[0] in [6,7,8])and(Xi[0] in [6,7,8]):
						if (Xk[1] in [0,1,2]) and (Xi[1] in [0,1,2]):
							arc.put((Xk,Xi))
						else if (Xk[1] in [3,4,5]) and (Xi[1] in [3,4,5]):
							arc.put((Xk,Xi))
						else if (Xk[1] in [6,7,8]) and (Xi[1] in [6,7,8]):
							arc.put((Xk,Xi))
    return csp,True



#####
# is_compatible: Function verifying the correctness of an assignment.
#
# X: Tuple containing the position in y and in x of the cell concerned by the assignment.
#
# v: String representing the value (between [1-9]) affected by the assignment.
#
# assignment: dict mapping cells (tuple (Y,X)) to values.
#
# csp: Object of class CSP containing all information relative to constraint 
#      satisfaction for Sudoku.
#
# return: A boolean indicating if the assignment of the value v in cell X is legal.
### 

def is_compatible(X,v, assignment, csp):
	blockY, blockX = (X//3)*3, (X//3)*3
	if not(((v,X) in csp.constraints[X]) or ((X,v) in csp.constraints[X]) or (((blockY+i//3, blockX+i%3) in csp.constraints[X])for i in range(9))):
		return True			
    return False



#####
# backtrack : Function used to find the missing assignments on the Sudoku grid using Backtracking Search.
#
#
# assignment: dict mapping cells (tuple (Y,X)) to values.
#
# csp: Object of class CSP containing all information relative to constraint 
#      satisfaction for Sudoku.
#
# return: The dictionary of assignments (cell => value)
### 

def backtrack(assignments, csp):
    return assignments



#####
# backtracking_search : Main function for backtracking
#
# csp: Object of class CSP containing all information relative to constraint 
#      satisfaction for Sudoku.
# The member variables are:
#      'variables'   : list of cases (tuple (Y,X)) 
#      'domains'    : dict mapping a cell to a list of possible values
#      'constraints' : dict mapping a cell to a list of cells who's value must be different from the first cell
#
# return: The dictionary of assignments (cell => value)
### 

def backtracking_search(csp):
	assignments = {}
	prevList = {}
	prev = '' #to remember the previous element
	notFound = false #boolean is set to true if no assignment is found
	invalidValue = {}
	for v in csp.variables:
		if notFound:
			v = prev
			del assignment[v]
		else:
			prevList[v] = prev
		if v in zip(*state.find(' ')):
			for d in csp.domains[v]:
				if is_compatible(v,d, assignments, csp) and (d not in invalidValue[v]):
					assignments[v] = d
					invalidValue[v] = d
					notFound = true
					prev = v
					break
		if v not in assignments:
			notFound = true
	return backtrack(assignments, csp)
