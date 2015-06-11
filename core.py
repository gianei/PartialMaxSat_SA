from numpy import *
from pulp import *
import argparse


# funções específicas do problema

class Instance():
    def __init__(self, file_wcnf, max_running_time_seconds):
        # args
        self.file_wcnf = file_wcnf
        self.max_running_time_seconds = max_running_time_seconds

        self.num_variables = None
        self.num_clauses = None
        self.num_top = None

        self.instance_matrix = None  # matrix [variables, clauses]: 0 = not existent, 1 = positive, -1 = negated
        self.hard_clauses = None  # instantiate an array for each clause: hard=1 soft=0

        self.read_instance()

    def read_instance(self):

        with open(self.file_wcnf, mode='r') as f:
            print('Reading file ', self.file_wcnf)
            lines = f.readlines()

            clause_i = 0
            for line in lines:
                values = str.split(line)

                if values[0] == 'c':
                    continue

                if values[0] == 'p':  # size definition
                    self.num_variables = int(values[2])
                    self.num_clauses = int(values[3])
                    self.num_top = int(values[4])

                    self.instance_matrix = zeros((self.num_clauses, self.num_variables), int)

                    self.hard_clauses = zeros(self.num_clauses, int)
                    
                    continue

                # populate variables
                for i in range(1, len(values) - 1):
                    var_j = abs(int(values[i])) - 1
                    self.instance_matrix[clause_i, var_j] = (1 if int(values[i]) > 0 else -1)

                # populate hard clauses
                if int(values[0]) == self.num_top:
                    self.hard_clauses[clause_i] = 1

                clause_i += 1

    def initial_solution(self):
        pass

    def propose_change(self):
        pass

    def change_solution(self):
        pass

    def final_solution(self):
        pass

    # funções genéricas de simulated annealing

    def iternum(self):
        pass

    def initprob(self):
        pass

    def tempfactor(self):
        pass

    def sizefactor(self):
        pass

    def minpercent(self):
        pass


def solve_with_glpk(instance):
    # defines the problem
    problem = LpProblem("problem", LpMaximize)
    # declare variables
    # CNF variables
    vars_x = [LpVariable("x" + str(i), 0, 1, LpInteger) for i in
              range(instance.num_variables)]  # LpVariaveble contained in {0,1}
    # CNF clauses
    vars_c = [LpVariable("c" + str(i), 0, 1, LpInteger) for i in range(instance.num_clauses)]
    # defines the constraints
    for i in range(instance.num_clauses):  #for each CNF clause
        restriction = []
        count_negated = 0
        for j in range(instance.num_variables):  #for each clause variable
            if instance.instance_matrix[i, j] == 1:
                restriction.append(vars_x[j])
            if instance.instance_matrix[i, j] == -1:
                restriction.append(-vars_x[j])
                count_negated += 1
        restriction.append(count_negated)

        #defines proper limitation according if soft or hard clause
        if instance.hard_clauses[i] == 1:
            problem += 1 <= lpSum(restriction)
        else:
            problem += vars_c[i] <= lpSum(restriction)


    # defines the objective function to maximize
    problem += lpSum(vars_c[i] for i in range(instance.num_clauses))
    problem.solve(pulp.GLPK(keepFiles=1, options=['--tmlim ' + str(instance.max_running_time_seconds)]))
    print("Satisfied clauses = ", value(problem.objective))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-f', '--file', help='String to open file', default="instances/hamming6-2.clq.wcnf")
    parser.add_argument('-t', '--time', help='Max running time in seconds', type=int, default=3600)
    args = vars(parser.parse_args())

    instance = Instance(args['file'], args['time'])

    solve_with_glpk(instance)