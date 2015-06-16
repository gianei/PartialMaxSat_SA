/*
 * Instance.h
 *
 *  Created on: 15/06/2015
 *      Author: Antonio
 */

#ifndef INSTANCE_H_
#define INSTANCE_H_

#include <vector>

class Instance {
public:
	friend class Solution;
	Instance();

	void load(const char *filename);

	void print_mat();
	void print_clauses();

	const std::vector<int>& getHardClauses() const;
	void setHardClauses(const std::vector<int>& hardClauses);
	const std::vector<std::vector<int> >& getInstMat() const;
	void setInstMat(const std::vector<std::vector<int> >& instMat);
	int getTop() const;
	void setTop(int top);
	int getNbclauses() const;
	void setNbclauses(int nbclauses);
	int getNvar() const;
	void setNvar(int nvar);
private:
	std::vector<std::vector<int> > inst_mat;
	std::vector<int> hard_clauses;

	int top;
	int nvar;
	int nbclauses;
};

#endif /* INSTANCE_H_ */
