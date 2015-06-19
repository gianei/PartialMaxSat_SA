/*
 * Solution.cpp
 *
 *  Created on: 15/06/2015
 *      Author: Antonio
 */

#include <iostream>
#include <stdlib.h>

#include "Solution.h"

Solution::Solution(Instance& inst)
 : instance(inst) {
	values.resize(inst.getNvar(),0);
}

bool Solution::check_satisfied_clause(int index) {
	bool satisfied = false;

	for (int j=0,l=instance.getNvar();j<l;++j){
		if (instance.inst_mat[index][j] == 1){
			if (values[j] == 1){
				satisfied = true;
				break;
			}
		} else if (instance.inst_mat[index][j] == -1){
			if (values[j] == 0){
				satisfied = true;
				break;
			}
		}
	}

	return satisfied;
}

bool Solution::check_satisfied_clause(int index, std::vector<int>& unsat) {
	bool satisfied = false;

	for (int j=0,l=instance.getNvar();j<l;++j){
		if (instance.inst_mat[index][j] == 1){
			if (values[j] == 1){
				satisfied = true;
				break;
			} else
				unsat.push_back(j);
		} else if (instance.inst_mat[index][j] == -1){
			if (values[j] == 0){
				satisfied = true;
				break;
			} else
				unsat.push_back(j);
		}
	}

	return satisfied;
}

bool Solution::is_feasible(){
	for (int i=0,l=instance.getNbclauses();i<l;++i){
		if (is_hard_clause(i) && !check_satisfied_clause(i))
			return false;
	}
	return true;
}

void Solution::copy_solution(const Solution &solution){
	values = solution.getValues();
}

void Solution::generate_solution() {
	std::vector<int> unsatvars;
	bool satisfied = false;

	for (int i=0,l=instance.getNbclauses();i<l;++i){
		satisfied = check_satisfied_clause(i,unsatvars);

		if (is_hard_clause(i) && !satisfied){
			// definição do método para escolha de variavel para satisfazer a expressão
			// resolvido na compilação para ganhar desempenho
#ifdef FIRST_VAR
			values[unsatvars.front()] = 1;
#elif defined LAST_VAR
			values[unsatvars.back()] = 1;
#else
			values[unsatvars[rand()%unsatvars.size()]] = 1;
#endif
		}
		unsatvars.clear();
	}
}

void Solution::neighbour_solution() {
#ifdef NEIGH_FLIP1
	int var = rand()%values.size();
	values[var] = !values[var];
#elif defined NEIGH_SWAP2
	int var1 = rand()%values.size();
	int var2 = rand()%values.size();
	int temp = values[var1];
	values[var1] = values[var2];
	values[var2] = temp;
#endif
}

int Solution::calculate_total() {
	int total = 0;

	for (int i=0,l=instance.getNbclauses();i<l;++i){
		if (check_satisfied_clause(i))
			++total;
	}

	return total;
}

void Solution::print_solution(){
	std::cout << "Values = ";

	for (int i=0,l=values.size();i<l;++i){
		std::cout << values[i] << " ";
	}

	std::cout << std::endl << "Satisfied clauses = " << calculate_total() << std::endl;
}

const std::vector<int>& Solution::getValues() const {
	return values;
}

void Solution::setValues(const std::vector<int>& values) {
	this->values = values;
}

const Instance& Solution::getInstance() const {
	return instance;
}
