/*
 * Solution.h
 *
 *  Created on: 15/06/2015
 *      Author: Antonio
 */

#ifndef SOLUTION_H_
#define SOLUTION_H_

#include "Instance.h"

class Solution {
public:
	Solution(Instance &inst);

	bool check_satisfied_clause(int index);
	bool check_satisfied_clause(int index, std::vector<int> &unsat);
	void generate_solution();
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
