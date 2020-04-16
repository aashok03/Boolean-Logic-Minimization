import pr1_funcs
import pr1_input
import pr1_output
import numpy as np
import sys


input_funcs = pr1_input.get_text()

all_answers = list()

print ("\nDebugging Log:\n\n")

for z in range (len(input_funcs)):

	boolfunc = input_funcs[z]
	print("Input function: ", boolfunc)

	minterms, dc = pr1_funcs.extract_minterms_dc(boolfunc)
	num_var = pr1_funcs.find_num_var (minterms, dc)
	print("Number of variables: ", num_var)

	func_output = pr1_funcs.function_output(minterms, dc, num_var)
	num_ones = pr1_funcs.number_of_ones(num_var, func_output)
	ones_minterms, ones_maxterms = pr1_funcs.group_num_ones(num_ones, func_output, num_var)
	

	#SOP calculations using minterms and don't cares
	print("\n\nSOP calculations:\n")

	print("Minterms: ", minterms)
	print("Don't Cares: ", dc)
	print("\n")

	min_cubes = list()
	min_cubes.append(ones_minterms)
	min_prime_implicants = list()
	for i in range (1, num_var + 1):
		min_cubes, min_prime_implicants = pr1_funcs.findCubes(min_cubes, i, min_prime_implicants, num_var)

	for i in range(len(min_cubes)):
		print(str(i) + "-cubes:\n", np.asarray(min_cubes[i]))
		print ("\n")
	print("PIs: ", min_prime_implicants)

	min_coverage_table = pr1_funcs.generate_coverage_table(min_prime_implicants, minterms)
	print("Coverage Table:\n", min_coverage_table)
	print("Rows of table: ", [item[1] for item in min_prime_implicants])
	print("Columns of table: ", minterms)
	print ("\n")
	
	min_essential_PIs, min_covered_minterms = pr1_funcs.find_EPIs_covered_minterms(min_coverage_table, minterms, min_prime_implicants)
	print("Essential PIs: ", min_essential_PIs)
	print("Covered Minterms: ", min_covered_minterms)

	min_reduced_table = pr1_funcs.remove_EPIs_covered_minterms(min_prime_implicants, min_essential_PIs, dc, min_covered_minterms)
	print("Remaining PIs: ", min_reduced_table)
	
	min_uncovered_minterms = pr1_funcs.get_uncovered_minterms(minterms, min_covered_minterms)
	print("Uncovered minterms: ", min_uncovered_minterms)
	print("\n")

	min_all_PIs = min_essential_PIs.copy()

	if len(min_uncovered_minterms) != 0:
		min_petricks = pr1_funcs.petricks_terms(min_uncovered_minterms, min_reduced_table)
		print("Petricks: ", min_petricks)

		min_simp_petricks = pr1_funcs.initial_combine(min_petricks)
		print("Combine with (X + Y)(X + Z) = (X + YZ): ", min_simp_petricks)

		min_distributive = pr1_funcs.distribute_all_terms(min_simp_petricks)
		print("Distributed Terms: ", min_distributive)
		
		min_combine_terms = pr1_funcs.logic_combination(min_distributive)	
		print("Simplify terms: ", min_combine_terms)

		min_char_count, min_to_add = pr1_funcs.min_PI_from_Petricks(min_combine_terms, min_reduced_table, min_essential_PIs)
		print("Character count: ", min_char_count)
		print("Min PI term to add from Petricks:", min_to_add)
		print("\n")

		for i in range (len(min_to_add)):
			min_all_PIs.append(min_reduced_table[ord(min_to_add[i]) - 97][1])
	
	print("All PIs: ", min_all_PIs)

	SOP = pr1_funcs.PI_to_SOP (min_all_PIs)
	print("SOP: ", SOP)

	print("\n\n---------------------------------------------------------------\n\n")

	

	#POS calculations using maxterms and don't cares
	print("POS calculations:\n")

	maxterms = pr1_funcs.get_maxterms(minterms, dc, num_var)
	print("Maxterms: ", maxterms)
	print("Don't Cares: ", dc)
	print("\n")

	max_cubes = list()
	max_cubes.append(ones_maxterms)
	max_prime_implicants = list()
	for i in range (1, num_var + 1):
		max_cubes, max_prime_implicants = pr1_funcs.findCubes(max_cubes, i, max_prime_implicants, num_var)
	
	for i in range(len(max_cubes)):
		print(str(i) + "-cubes:\n", np.asarray(max_cubes[i]))
		print ("\n")
	print("PIs: ", max_prime_implicants)

	max_coverage_table = pr1_funcs.generate_coverage_table(max_prime_implicants, maxterms)
	print("Coverage Table:\n", max_coverage_table)
	print("Rows of table: ", [item[1] for item in max_prime_implicants])
	print("Columns of table: ", maxterms)
	print ("\n")

	max_essential_PIs, max_covered_minterms = pr1_funcs.find_EPIs_covered_minterms(max_coverage_table, maxterms, max_prime_implicants)
	print("Essential PIs: ", max_essential_PIs)
	print("Covered Maxterms: ", max_covered_minterms)

	max_reduced_table = pr1_funcs.remove_EPIs_covered_minterms(max_prime_implicants, max_essential_PIs, dc, max_covered_minterms)
	print("Remaining PIs: ", max_reduced_table)
	
	max_uncovered_minterms = pr1_funcs.get_uncovered_minterms(maxterms, max_covered_minterms)
	print("Uncovered maxterms: ", max_uncovered_minterms)
	print("\n")

	max_all_PIs = max_essential_PIs.copy()

	if len(max_uncovered_minterms) != 0:
		max_petricks = pr1_funcs.petricks_terms(max_uncovered_minterms, max_reduced_table)
		print("Petricks: ", max_petricks)
		
		max_simp_petricks = pr1_funcs.initial_combine(max_petricks)
		print("Use (X + Y)(X + Z) = (X+ YZ): ", max_simp_petricks)

		max_distributive = pr1_funcs.distribute_all_terms(max_simp_petricks)
		print("Distributed Terms: ", max_distributive)
		
		max_combine_terms = pr1_funcs.logic_combination(max_distributive)	
		print("Combined terms: ", max_combine_terms)

		max_char_count, max_to_add = pr1_funcs.min_PI_from_Petricks(max_combine_terms, max_reduced_table, max_essential_PIs)
		print("Character count: ", max_char_count)
		print("Max PI term to add from Petricks:", max_to_add)
		print("\n")

		for i in range (len(max_to_add)):
			max_all_PIs.append(max_reduced_table[ord(max_to_add[i]) - 97][1])
	
	print("All PIs: ", max_all_PIs)
	
	POS = pr1_funcs.PI_to_POS (max_all_PIs)
	print("POS: ", POS)

	final_result = boolfunc + " = " + SOP + " = " + POS
	all_answers.append(final_result)
	print("\n\nSimplified Final Result: ", final_result)
	
	print("\n\n============================================================================")
	print("============================================================================\n\n")

pr1_output.show_output(all_answers)