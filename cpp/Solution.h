/*
 * Solution.h
 *
 *  Created on: 15/06/2015
 *      Author: Antonio
 */

#ifndef SOLUTION_H_
#define SOLUTION_H_

// método de criação de solução vizinha escolhido
#define NEIGH_FLIP1
//#define NEIGH_SWAP2

// método de factibilização de uma solução infactivel
//#define RANDOM_VAR
#define FIRST_VAR
//#define LAST_VAR

#include "Instance.h"

class Solution {
public:
	Solution(Instance &inst);

	bool check_satisfied_clause(int index);
	bool check_satisfied_clause(int index, std::vector<int> &unsat);
	bool is_feasible();
	inline bool is_hard_clause(int clause){ return instance.hard_clauses[clause];}

	void generate_solution();
	void neighbour_solution();
	void copy_solution(const Solution &solution);
	int calculate_total();

	void print_solution();

	const std::vector<int>& getValues() const;
	void setValues(const std::vector<int>& values);
	const Instance& getInstance() const;
private:
	std::vector<int> values; // valores para cada variável
	Instance &instance;
};

#endif /* SOLUTION_H_ */
