# -*- coding: utf-8 -*-

#####
# Name: Amee Joshipura
# Id: 260461226
###

import pdb #Use pdb.set_trace() to make a break in your code.
import numpy as np
import Queue

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
	#algorithm from the lecture slides
	revised = False
	#for each possible value, d, in the domain of Xi
	for d in csp.domains[Xi]:
		#if the domain of Xj has only one value and 
		#if that value is the same as the selected value,d, from the domain of Xi
		#then remove it from the domain of Xi and set reduced to true
		if len(csp.domains[Xj])==1:
			if d == csp.domains[Xj][0]:
				csp.domains[Xi].remove(d)
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
	#algorithm from the lecture slides
	#queue 'arcs' of all the arcs in csp
	arc = csp.arcs()
	#while the queue is not empty
	while len(arc)>0:
		#get the first tuple element of the queue
		(Xi, Xj) = arc.pop()
		#check if any revision has occurred in the domain of Xi
		revised,csp=reduce(Xi,Xj,csp)
		#if revised and domain of Xi is non empty, then add all other pairs Xk, Xi
		#where Xk is in the constraints ('neighbors')of Xi
		#Xk is not Xi, and then repeat the process by checking in the loop
		#if domain of Xk needs revision
		if revised:
			#if after revision, domain of Xi is empty
			#return false indicating arc inconsistency
			if not csp.domains[Xi]:
				return csp,False
			for Xk in csp.constraints[Xi]:
				if Xk != Xj:
					arc.append((Xk,Xi))
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
	#if a constraint of X is already in assignments, ie assigned a value
	#check if that value is same value
	#if v and assigned value of the constraint are same, return false
	#because they cannot have the same value
	for var in assignment:
		for c in csp.constraints[X]:
			if var==c:
				if assignment[var]==v:
					return False	
	return True



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
	#check for a value from a domain
	#check if it is compatible
	#AC-3 to find inconsistency - remove from domain if inconsistent
	#if inconsistency found, backtrack
	#if not, move forward
	if len(assignments)==len(csp.variables):
		return assignments
	v=[v for v in csp.variables if v not in assignments]
    v=v[0]
	for d in csp.domains[v]:
		if is_compatible(v,d,assignments,csp):
			assignments[v]=d
			csp2=csp.copy()
			csp2,isOK=AC3(csp2)
			if isOK:
				result=backtrack(assignments,csp2)
				if result!=False:
					return result
			assignments.pop(v)
	return False



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
	#build the assignments as we traverse through all variables
	#backtrack and assign simultaneously 			
	return backtrack({}, csp)
