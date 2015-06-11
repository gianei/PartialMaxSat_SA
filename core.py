from numpy import *
from pulp import *

# funções específicas do problema

def read_instance():
    with open("instances/hamming8-4.clq.wcnf", mode='r') as f:
        lines = f.readlines()

        cont_clausules = 0
        for line in lines:
            values = str.split(line)
            if values[0] == 'c': continue
            if values[0] == 'p': # definição do tamanho
                num_variables =  int(values[2])
                num_clausules = int(values[3])
                num_top = int (values[4])
                instance = zeros((num_clausules, num_variables), int) # index0: hard=1 soft=0
                hard_clausules = zeros(num_clausules, int)
                continue



            for i in range(1, len(values)-1):
                instance[cont_clausules, abs(int(values[i]))-1] = 1 if int(values[i]) > 0 else -1

            if int(values[0]) == num_top:
                hard_clausules[cont_clausules] = 1

            cont_clausules += 1



    return (instance, hard_clausules, num_variables, num_clausules)

def initial_solution():
    pass

def propos_change():
    pass

def change_solution():
    pass

def final_solution():
    pass

# funções genéricas de simulated annealing

def iternum():
    pass

def initprob():
    pass

def tempfactor():
    pass

def sizefactor():
    pass

def minpercent():
    pass


if __name__ == '__main__':
    print ("hello")
    coisa = read_instance()

    # if len(sys.argv) > 1:
    #     if sys.argv[1] == 'black':
    #         print("Black")


    """
    The Beer Distribution Problem for the PuLP Modeller
    Authors: Antony Phillips, Dr Stuart Mitchell  2007
    """



    # declare your variables
    vars_x = [LpVariable("x"+str(i), 0, 1, LpInteger) for i in range(coisa[2])]
    # x1 = LpVariable("x1", 0, 1, LpInteger)
    # x2 = LpVariable("x2", 0, 1, LpInteger)
    # x3 = LpVariable("x3", 0, 1, LpInteger)

    #declare c variables
    vars_c = [LpVariable("c"+str(i), 0, 1, LpInteger) for i in range(coisa[3])]
    # c1 = LpVariable("c1", 0, 1, LpInteger)
    # c2 = LpVariable("c2", 0, 1, LpInteger)
    # c3 = LpVariable("c3", 0, 1, LpInteger)
    # c4 = LpVariable("c4", 0, 1, LpInteger)
    # c5 = LpVariable("c5", 0, 1, LpInteger)
    # c6 = LpVariable("c6", 0, 1, LpInteger)


    # defines the problem
    prob = LpProblem("problem", LpMaximize)

    # defines the constraints
    for i in range(coisa[3]): #para cada clausula
        restr = []
        contN = 0
        for j in range(coisa[2]): #para cada var
            if coisa[0][i,j] == 1:
                restr.append(vars_x[j])
            if coisa[0][i,j] == -1:
                restr.append(-vars_x[j])
                contN +=1
        restr.append(contN)
        # prob += lpSum([(vars[i][j] if coisa[0][i,j] == 1 else (1 - vars_x[j] if coisa[0][i,j] == -1 else 0 )) for j in range(coisa[2])])>=vars_c[i]

        if coisa[1][i] == 1:
            prob += 1 <= lpSum(restr)
        else:
            prob += vars_c[i] <= lpSum(restr)


    # prob += c1 <= 1 - x1
    # prob += c2 <= 1 - x2
    # prob += c3 <= 1 - x3
    # prob += c4 <= x1 + x2
    # prob += c5 <= 2 - x1 - x3
    # prob += c6 <= x2 + 1 - x3

    # restrições hard
    # for i in range(coisa[3]):
    #     if coisa[1][i] == 1:
    #         prob += vars_c[i] >= 1

    # prob += c1 >= 1
    # prob += c2 >= 1


    # defines the objective function to maximize
    prob += lpSum( vars_c[i] for i in range(coisa[3]))
    # prob += c1 + c2 + c3 + c4 + c5 + c6

    # The problem data is written to an .lp file
    prob.writeLP("P-MaxSAT.lp")

    # The problem is solved using PuLP's choice of Solver (GLPK)
    prob.solve(pulp.GLPK())

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # Each of the variables is printed with it's resolved optimum value
    # for v in prob.variables():
    #     print(v.name, "=", v.varValue)

    # The optimised objective function value is printed to the screen
    print("Cláusulas satisfeitas = ", value(prob.objective))