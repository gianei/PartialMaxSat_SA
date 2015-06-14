from numpy import *
from pulp import *
import argparse
from numpy.random.mtrand import randint, choice
import cProfile


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
    
            #print(self.instance_matrix)
            #print(self.hard_clauses)


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

class Solution:
    def __init__(self,instance):
        self.solution = None
        self.instance = instance

        self.generate_solution()

    def check_satisfied_unsat_clause(self, clause):
        satisfied = False
        unsatvars = []

        a = nonzero(clause)
        for j in nditer(a[0]):
            # print ("%d <%d>" % (it[0], it.index))
            if (clause[j] == 1):
                if (self.solution[j] == 1):
                    satisfied = True
                    break
                else:
                    unsatvars.append(j)
            elif (clause[j] == -1):
                if (self.solution[j] == 0):
                    satisfied = True
                    break
                else:
                    unsatvars.append(j)
#        print("Unsatisfied variables:",unsatvars)
#        print("Satisfied?",satisfied)

        return satisfied,unsatvars

    def check_satisfied_clause(self, clause):
        satisfied = False

        a = nonzero(clause)
        for j in nditer(a[0]):
            # print ("%d <%d>" % (it[0], it.index))
            if (clause[j] == 1):
                if (self.solution[j] == 1):
                    satisfied = True
                    break
            elif (clause[j] == -1):
                if (self.solution[j] == 0):
                    satisfied = True
                    break

        return satisfied

    def generate_solution(self):
        # self.solution = [randint(0,1) for i in range(self.instance.num_variables)]    #generates only zeros (wrong)
        self.solution = [0 for i in range(self.instance.num_variables)]                 #same as above
        # self.solution = random.random_integers(0,1,self.instance.num_variables)       #generate [0,1] (right but slower)
        # self.solution = zeros(self.instance.num_variables, dtype="int")                 #generate zeros

        a = where(self.instance.hard_clauses) #indexes of hard clauses
        for i in nditer(a[0]):
            satisfied, possiblevars = self.check_satisfied_unsat_clause(self.instance.instance_matrix[i])

            if not satisfied:
                self.solution[choice(possiblevars)] = 1

        return

    def get_solution_total(self):
        total = 0
        #hard clauses are always satisfied at this point
        total += count_nonzero(self.instance.hard_clauses)

        a = where(self.instance.hard_clauses == 0) #indexes of soft clauses
        for i in nditer(a[0]):
            satisfied = self.check_satisfied_clause(self.instance.instance_matrix[i])

            if satisfied:
                    total += 1

        return total

def sa_prob(newvalue,oldvalue,temperature):
    return exp((newvalue - oldvalue)/temperature)

def solve_with_sa(instance,startingtemp,coolingrate,mintemp,maxiter):
    print ("Solving with SA:")
    currentsolution = Solution(instance)
    currentvalue = currentsolution.get_solution_total()
    currenttemp = startingtemp

    while currenttemp > mintemp:
        i = 0
        while i < maxiter:
            newsolution = Solution(instance)
            newvalue = newsolution.get_solution_total()
            
            if (sa_prob(newvalue,currentvalue,currenttemp) > random.random()):
                currentsolution = newsolution
                currentvalue = newvalue

            i += 1
        currenttemp *= coolingrate

    print("Solution:",currentsolution.solution)
    print ("Satisfied clauses =", currentvalue)

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
    print("Satisfied clauses =", value(problem.objective))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-f', '--file', help='String to open file', default="instances/hamming8-4.clq.wcnf")
    parser.add_argument('-t', '--time', help='Max running time in seconds', type=int, default=3600)
    args = vars(parser.parse_args())

    instance = Instance(args['file'], args['time'])

    #solve_with_glpk(instance)
    cProfile.run('solve_with_sa(instance,10,0.75,0.1,10)')
    #solve_with_sa(instance,10,0.75,0.1,10)