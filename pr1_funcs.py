import math
import sys
import numpy as np
import tkinter as tk
from tkinter import *
from collections import OrderedDict
from tkinter.filedialog import askopenfilename, asksaveasfilename
 

#Extract minterms and dont cares from input string
def extract_minterms_dc (boolfunc):
	minterms = list()
	dc = list()

	#Extract minterms
	min_string = boolfunc[boolfunc.index("(") + 1: boolfunc.index(")")]
	if len(min_string) != 0:
		minterms = min_string.split(",")
	else:
		print("Error: input must contain at least one minterm")
		exit()
	#Convert each minterm string to int
	for i in range(0, len(minterms)): 
	    minterms[i] = int(minterms[i]) 

	#Extract dont cares
	dc_string = ""
	if "d" in boolfunc:
		dc_string = boolfunc[boolfunc.index("d("):]
		dc_string = dc_string[dc_string.index("(") + 1: dc_string.index(")")]

	if len(dc_string) != 0:
		dc = dc_string.split(",")
	#Convert each dont care string to int
	for i in range(0, len(dc)): 
	    dc[i] = int(dc[i]) 

	minterms.sort()
	dc.sort()

	return minterms, dc


#Determing the total number of variables
def find_num_var(minterms, dc):
	if len(dc) != 0:
		num_var = math.floor(math.log2(max(max(minterms), max(dc))) + 1)
	else:
		num_var = math.floor(math.log2(max(minterms)) + 1)
	return num_var


def get_maxterms(minterms, dc, num_var):
	maxterms = list()
	for i in range (int(math.pow(2, num_var))):
		if i not in minterms and i not in dc:
			maxterms.append(i)
	return maxterms


#Make array of function output
def function_output(minterms, dc, num_var):
	func_output = np.zeros(2 ** num_var)
	for i in range (0, len(func_output)):
		if i in minterms:
			func_output[i] = 1
		elif i in dc:
			func_output[i] = -1
		else:
			func_output[i] = 0
	return func_output


#Make array of number of 1s
def number_of_ones (num_var, func_output):
	num_ones = np.zeros(2 ** num_var)
	for i in range (0, len(func_output)):
		num_ones[i] = "{0:b}".format(i).count('1')
	return num_ones
	

#Group minterms with same number of 1s. 
#Entries are list with the minterms and their binary representation in the 
#same number of bits as the number of variables.
def group_num_ones(num_ones,func_output, num_var):
	ones_minterms = list()
	ones_maxterms = list()
	for i in range (0, int(max(num_ones)) + 1):
		temp_list_min = list()
		temp_list_max = list()
		for j in range (0, len(func_output)):
			if num_ones[j] == i and (func_output[j] == 1 or func_output[j] == -1):
				temp_list_min.append([[j], ("{0:0" + str(num_var) + "b}").format(j), False])
			if num_ones[j] == i and (func_output[j] == 0 or func_output[j] == -1):
				temp_list_max.append([[j], ("{0:0" + str(num_var) + "b}").format(j), False])
		ones_minterms.append(temp_list_min)
		ones_maxterms.append(temp_list_max)
	return ones_minterms, ones_maxterms



#Function to find cubes of all degrees
def findCubes(cubes, cube_num, prime_implicants, num_var): 
	new_cubes = list()

	for i in range (0, len(cubes[cube_num - 1]) - 1):
		temp_list = list()
		temp_cube = list()
		for j in range (0, len(cubes[cube_num - 1][i])):
			for k in range (0, len(cubes[cube_num - 1][i + 1])):
				count = 0
				combined_str = ""
				#Find minterms bit differences
				for l in range (0, num_var):
					if cubes[cube_num - 1][i][j][1][l] != cubes[cube_num - 1][i + 1][k][1][l]:
						count += 1
						combined_str += "x"
					else:
						combined_str += cubes[cube_num - 1][i][j][1][l]
				#Make cubes from 1 bit differences
				if count == 1:
					if not(combined_str in temp_list):
						temp_list.append(combined_str)
						temp_cube.append([cubes[cube_num - 1][i][j][0] + cubes[cube_num - 1][i + 1][k][0], combined_str, False])
					cubes[cube_num - 1][i][j][2] = True
					cubes[cube_num - 1][i + 1][k][2] = True

		new_cubes.append(temp_cube)

	cubes.append(new_cubes)

	#Update covered cubes
	for i in range (0, len(cubes[cube_num - 1])):
		for j in range(0, len(cubes[cube_num - 1][i])):
			if cubes[cube_num - 1][i][j][2] == False:
				prime_implicants.append([cubes[cube_num - 1][i][j][0], cubes[cube_num - 1][i][j][1]])

	return cubes, prime_implicants


#Generate coverage table
def generate_coverage_table(prime_implicants, minterms):
	coverage_table = np.zeros(len(prime_implicants) * len(minterms)).reshape(len(prime_implicants), len(minterms))
	for i in range (len(prime_implicants)):
		for j in range (len(prime_implicants[i][0])):
			if prime_implicants[i][0][j] in minterms:
				coverage_table[i][minterms.index(prime_implicants[i][0][j])] = 1
	return coverage_table


#Find essential PIs
def find_EPIs_covered_minterms(coverage_table, minterms, prime_implicants):
	essential_PIs = list()
	covered_minterms = list()
	for i in range (len (coverage_table[0])):
		if np.count_nonzero(coverage_table[:,i]) == 1:
			PI = np.where(coverage_table[:,i] == 1)
			essential_PIs.append(prime_implicants[PI[0][0]][1])
			essential_PIs = list(set(essential_PIs)) 

			essential_terms = np.where(coverage_table[PI[0][0]] == 1)
			for j in range(len(essential_terms[0])):
				essential_terms[0][j] = minterms[essential_terms[0][j]]
			covered_minterms += essential_terms[0].tolist()
			covered_minterms = list(set(covered_minterms)) 
	covered_minterms.sort()
	return essential_PIs, covered_minterms


#Remove essential PIs and covered minterms, and assign letters to non essential PIS
def remove_EPIs_covered_minterms(prime_implicants, essential_PIs, dc, covered_minterms):
	pi_list = [item[1] for item in prime_implicants]

	#Remove essential PIs and assign letters
	counter = 0
	reduced_table = list()
	for i in range(len(prime_implicants)):
		if pi_list[i] not in essential_PIs:
			new_pi = prime_implicants[i]
			assigned_letter = chr(97 + counter)
			new_pi.append(assigned_letter)
			reduced_table.append(new_pi)
			counter += 1


	#Remove covered minterms
	for i in range (len(reduced_table)):
		updated_minterms = list()
		for j in range (len(reduced_table[i][0])):
			if reduced_table[i][0][j] not in dc and reduced_table[i][0][j] not in covered_minterms:
				updated_minterms.append(reduced_table[i][0][j])
		reduced_table[i][0] = updated_minterms

	return reduced_table


#Get uncovered minterms
def get_uncovered_minterms(minterms, covered_minterms):
	uncovered_minterms = list()
	for i in range(len(minterms)):
		if minterms[i] not in covered_minterms:
			uncovered_minterms.append(minterms[i])
	uncovered_minterms.sort()
	return uncovered_minterms


#Petricks Method: group cyclic table terms
def petricks_terms(uncovered_minterms, reduced_table):
	petricks = list()
	for i in range (len(uncovered_minterms)):
		minterm_PIs = list()
		for j in range(len(reduced_table)):
			if uncovered_minterms[i] in reduced_table[j][0]:
				minterm_PIs.append(reduced_table[j][2])
		petricks.append(minterm_PIs)
	return petricks


#(X+Y)(X+Z) = (X+YZ)
def initial_combine(petricks):
	simp_petricks = list()
	combined = np.zeros(len(petricks))
	for i in range (len(petricks)):
		can_combine = False
		for j in range (len(petricks[i])):
			for k in range (len(petricks)):
				if petricks[i][j] in petricks[k] and i != k and combined[i] != 1 and combined[k] != 1:
					temp = list()
					temp.append(petricks[i][j])
					for l in range (len(petricks[i])):
						for m in range (len(petricks[k])):
							if petricks[i][l] != petricks[i][j] and petricks[k][m] != petricks[i][j]:
								s = petricks[i][l] + petricks[k][m]
								temp.append(s)
					combined[i] = 1
					combined[k] = 1
					can_combine = True
					simp_petricks.append(temp)
		if can_combine == False and combined[i] == 0:
			simp_petricks.append(petricks[i])
	return simp_petricks



#Multiply two terms
def multiply_terms(a,b):
	mult = list()
	for i in range(len(a)):
		for j in range(len(b)):
			if a[i] != b[j]:
				temp = ''.join(sorted(a[i] + b[j])) 
				temp = ''.join(OrderedDict.fromkeys(temp))
				mult.append(temp)
	return list(set(mult))


#Distribute all terms
def distribute_all_terms(petricks):
	distributive = petricks[0]
	for i in range(len(petricks)-1):
		distributive = multiply_terms(distributive, petricks[i + 1])
		distributive.sort()
	return distributive


#Combine terms 
def logic_combination(distributive):
	combine_terms = list()
	for i in range (len(distributive)):
		is_min = True
		for j in range (len(distributive)):
			if i != j:
				a = [char for char in distributive[i]]  
				b = [char for char in distributive[j]] 
				if set(b).issubset(set(a)) and len(a) > len(b):
					is_min = False		
		if is_min == True:
			combine_terms.append(distributive[i])
	combine_terms.sort()
	return combine_terms


#Determine the combined term with the least number of variables
def min_PI_from_Petricks(combine_terms, reduced_table, essential_PIs):
	char_count = list()
	for i in range (len(combine_terms)):
		min_chars = 0
		for j in range (len(combine_terms[i])):
			temp = reduced_table[ord(combine_terms[i][j]) - 97][1]
			min_chars += len(temp) - temp.count('x') 
		char_count.append(min_chars)

	min_to_add = combine_terms[char_count.index(min(char_count))]
	return char_count, min_to_add


#Sum of Products conversion
def PI_to_SOP(PI_list): 
	sop = ""
	for i in range (len(PI_list)):
		term = ""
		for j in range (len(PI_list[i])):
			if PI_list[i][j] != "x":
				if PI_list[i][j] == "0":
					term = term + chr(65 + j) + "\'"
				else:
					term += chr(65 + j)
		sop += term + "+"
	sop = sop[:(len(sop) - 1)]
	return sop


#Product of sums conversion
def PI_to_POS(PI_list): 
	pos = ""
	for i in range (len(PI_list)):
		term = "("
		for j in range (len(PI_list[i])):
			if PI_list[i][j] != "x":
				if PI_list[i][j] == "0":
					term = term + chr(65 + j) + "+"
				else:
					term += chr(65 + j) + "\'+"
		pos += term[:(len(term) - 1)] + ")"
	return pos