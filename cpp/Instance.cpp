/*
 * Instance.cpp
 *
 *  Created on: 15/06/2015
 *      Author: Antonio
 */

#include <iostream>
#include <fstream>

#include "Instance.h"

Instance::Instance() {}

void Instance::load(const char *filename){
	std::ifstream wcnf(filename);

	char type = 0;
	char discard[256];
	bool fileok = false;

	while (!wcnf.eof()){
		wcnf.get(type);

		if (type == 'p'){
			wcnf >> discard >> nvar >> nbclauses >> top;
			fileok = true;
			break;
		} else
			wcnf.getline(discard,256);
	}

	if (fileok){
		inst_mat.resize(nbclauses, std::vector<int>(nvar,0));
		hard_clauses.reserve(nbclauses);

		for (int i=0;i<nbclauses;++i){
			int val = -9999;
			int weight = -1;
			wcnf >> weight;

			if (weight == top)
				hard_clauses[i] = 1;
			else
				hard_clauses[i] = 0;

			while (val != 0){
				wcnf >> val;
				if (val == 0)
					break;

				if (val < 0)
					inst_mat[i][-val - 1] = -1;
				else
					inst_mat[i][ val - 1] = 1;
			}
		}
		wcnf.close();
	} else {
		wcnf.close();
		throw 1;
	}
}

void Instance::print_mat() {
	for (int i=0;i<nbclauses;++i){
		for (int j=0;j<nvar;++j){
			std::cout << inst_mat[i][j] << " ";
		}
		std::cout << std::endl;
	}
}

void Instance::print_clauses() {
	for (int i=0;i<nbclauses;++i){
		std::cout << hard_clauses[i] << " ";
	}
	std::cout << std::endl;
}

const std::vector<int>& Instance::getHardClauses() const {
	return hard_clauses;
}

void Instance::setHardClauses(const std::vector<int>& hardClauses) {
	hard_clauses = hardClauses;
}

const std::vector<std::vector<int> >& Instance::getInstMat() const {
	return inst_mat;
}

void Instance::setInstMat(const std::vector<std::vector<int> >& instMat) {
	inst_mat = instMat;
}

int Instance::getTop() const {
	return top;
}

void Instance::setTop(int top) {
	this->top = top;
}

int Instance::getNbclauses() const {
	return nbclauses;
}

void Instance::setNbclauses(int nbclauses) {
	this->nbclauses = nbclauses;
}

int Instance::getNvar() const {
	return nvar;
}

void Instance::setNvar(int nvar) {
	this->nvar = nvar;
}
