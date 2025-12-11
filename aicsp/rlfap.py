import read as rd
import csp as c
import time as t 

weight = {}
conf_set = {}
order = {}
domains = rd.read_domains("rlfap/dom11.txt")
variables = rd.read_variables("rlfap/var11.txt")
constraints, neighbours = rd.read_constraints("rlfap/ctr11.txt")
var_to_dom = {}
for i in variables:
    var_to_dom[i] = domains[variables[i][0]] 

for ctr in constraints:
    weight[ctr] = 1


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                weight[(var, B)] += 1   # domain wipe-out so increase weight for both var
                weight[(B, var)] += 1   # and the neighbour (dom/wdeg heuristic)
                conf_set[B].add(var) 
                return False
    return True


def check_constraints(A,A_val,B,B_val):
    global constraints 

    #as not to violate the csp class's definitiion

    operator , k = constraints[(A,B)]
    if operator == '>':
        return abs(A_val - B_val) > k
    if operator == '=':
        return abs(A_val - B_val) == k


def dom_wdeg(assigned,csp):
    """
    implementation of the dom / wdeg heuristic function to drastically reduce the time needed in order for the forward checking algorithm to complete. 
    insertion of global variables as to keep the csp's form intact and not cause any internal problems. 
    initializes the best_score as 0, and the best variable to get as none. 
    the dom / wdeg heuristic functions as follows: 
    dom is the length of the domain of the current variable (as it iterates through the variables) 
    wdeg is the weight degree of the constraints
    the value for each variable is calculated as the 
    length of the domain of the value / the sum of the weights of the constraints with its neighbors. 
    returns the variable with the best value. 
    """
    global var_to_dom
    global weight
    best = None
    best_score = -float('inf')

    for var in csp.variables:
        if var in assigned:
            continue

        #initialized as 1 to avoid division by 0 if push comes to shove. 

        wdeg = 1

        for neighbour in csp.neighbors[var]:
            wdeg += weight[(var,neighbour)]
        
        domain = csp.curr_domains[var] if csp.curr_domains else var_to_dom[var]
        dsize = len(domain)

        if dsize == 0:
            return var

        score = wdeg / dsize 
        
        if score > best_score:
            best_score = score
            best = var

    return best

for var in variables:
        conf_set[var] = set()
        order[var] = 0

rlfap = c.CSP(variables,var_to_dom,neighbours,check_constraints)

start= t.time()
solution = c.backtracking_search(rlfap,select_unassigned_variable=dom_wdeg,order_domain_values=c.unordered_domain_values,inference=forward_checking)

for key, value in solution.items():
    print(f"{key} : {value} ")
print(len(solution))
end = t.time()
diff =  end - start
print(diff)


for ctr in constraints:
    weight[ctr] = 1

