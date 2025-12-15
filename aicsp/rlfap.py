import read as rd
import csp as c
import time as t 

weight = {}
conf_set = {}
order = {}
var_to_dom = {}



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

def AC3(csp, queue=None, removals=None, arc_heuristic=c.dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable


def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    if not csp.curr_domains[Xi]:
        weight[(Xi, Xj)] += 1   # domain wipe-out so increase weight for both var
        weight[(Xj, Xi)] += 1   # and the neighbour (dom/wdeg heuristic)
    return revised, checks




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


#################################################################
#################### INFORMATION GATHERING ######################
#################################################################

f_solutions = []
instances = ["2-f24","2-f25","3-f10","3-f11","6-w2","7-w1-f4","7-w1-f5","8-f10","8-f11","11","14-f27","14-f28"]
for instance in instances:
    varname = "rlfap/var" + instance + ".txt"
    ctrname = "rlfap/ctr" + instance + ".txt" 
    domname = "rlfap/dom" + instance + ".txt"

    domains = rd.read_domains(domname)
    variables = rd.read_variables(varname)
    constraints, neighbours = rd.read_constraints(ctrname)

    for i in variables:
        var_to_dom[i] = domains[variables[i][0]] 

    for ctr in constraints:
        weight[ctr] = 1

    for var in variables:
        conf_set[var] = set()
        order[var] = 0

    rlfap = c.CSP(variables,var_to_dom,neighbours,check_constraints)

    start = t.time()
    solution = solution = c.backtracking_search(rlfap, select_unassigned_variable=dom_wdeg, order_domain_values=c.unordered_domain_values, inference=mac)
    end = t.time() - start
    if solution is not None:
        f_solutions.append((instance,end,rlfap.nassigns))


    print(varname,ctrname, domname, "\n")
    var_to_dom.clear()
    weight.clear()
    conf_set.clear()
    order.clear()

for sol in f_solutions:
    print(sol, "\n")
