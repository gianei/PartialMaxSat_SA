// compilar com flag -std=c++11

#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <chrono>

#include "Instance.h"
#include "Solution.h"

// converter soluções infactiveis para factiveis ou descartar
#define MAKE_FEASIBLE
//#define DISCARD_UNFEASIBLE

inline float randfloat(){
	return static_cast<float>(rand())/static_cast<float>(RAND_MAX);
}

inline float sa_prob(int newvalue, int oldvalue, float temperature){
    return exp(float(newvalue - oldvalue)/temperature);
}

void solve_with_sa(Instance &inst,float startingtemp,float coolingrate,float mintemp,int maxiter){
	std::cout << "Solving with SA:" << std::endl;

	Solution currentsolution(inst),newsolution(inst);
	currentsolution.generate_solution();
	newsolution.generate_solution();

	currentsolution.print_solution();

    int currentvalue = currentsolution.calculate_total();
    int newvalue = 0;
	float currenttemp = startingtemp;

	while (currenttemp > mintemp){
    	int i = 0;
    	while (i++ < maxiter){
    		newsolution.neighbour_solution();
#ifdef MAKE_FEASIBLE
    		newsolution.generate_solution();
#elif defined DISCARD_UNFEASIBLE
    		if (!newsolution.is_feasible())
    			continue;
#endif

    		newvalue = newsolution.calculate_total();

			if (sa_prob(newvalue,currentvalue,currenttemp) > randfloat()){
				currentsolution.copy_solution(newsolution);
				currentvalue = newvalue;
			}
    	}

		currenttemp *= coolingrate;
    }

	currentsolution.print_solution();
}

int main(int argc, char **argv){
	srand(time(NULL));

	if (argc < 6){
		std::cout << "Uso: pmaxsatglpk.exe <arquivo wcnf> <temperatura inicial> <taxa de resfriamento> <temperatura minima> <iterações>" << std::endl;
		return 1;
	}

	float startingtemp = atof(argv[2]);
	float coolingrate = atof(argv[3]);
	float mintemp = atof(argv[4]);
	float maxiter = atof(argv[5]);
	std::cout << "Params: " << startingtemp << " " << coolingrate << " " << mintemp << " " << maxiter << std::endl;

	Instance prob;
	try {
		prob.load(argv[1]);
	} catch(int e){
		std::cerr << "Arquivo wcnf inválido: " << argv[1] << std::endl;
	}

	std::chrono::high_resolution_clock::time_point start = std::chrono::high_resolution_clock::now();
	solve_with_sa(prob,startingtemp,coolingrate,mintemp,maxiter);
	auto elapsed = std::chrono::high_resolution_clock::now() - start;
	std::cout << "Tempo: " << static_cast<long long>(std::chrono::duration_cast<std::chrono::seconds>(elapsed).count()) << " segundos" << std::endl;
}
