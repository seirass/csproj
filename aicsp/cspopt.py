def read_file(filename,flights,variables):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split(" ")
            if len(parts) == 2:
                for i in range(int(parts[0])):
                    flights.append(i+1)
            else:

                row = list(map(int,parts))
                variables.append(row)
#############################################TESTING FUNCTIONS#####################################
def assign(flights,pairing,assignment,variables):
    assignment.append(pairing)
    variables.remove(pairing)
    for flight in pairing:
        if flight in flights:
            flights.remove(flight)
            print(f"removed flight {flight}")

def maintain_arc_consistency(variables,pairing):
    for flight in pairing:
        for var in variables[:]:
            if flight in var:
                variables.remove(var)
                print(f"removed variable {var} because of flight {flight}")
                continue

def select_unassigned_flight(variables):
    return variables[0]
#################################################################################################


def solve(assignment, variables, flights, best_cost, current_cost, best_assignment):
    """
    Initially checks whether we have reached a terminal state, a terminal state can be one of the following:
    1) current_cost is greater than the best cost so no need to explore any further
    2) flights are empty, thus no flights remaining to complete the total
    3) variables empty, no solution found for this current branch.

    In order to backtrack, we need to create shallow copies for the variables that will be passed on the recursion
    After selecting the next variable to be assigned, we remove the flights comprising the pairing from the flights
    After selecting the next variable we then remove the pairings that have at least one flight in common with the variable to be assigned.

    Due to the boolean nature of the variable's domain, this implementation functions in the following way:
    >Call it, and it then selects the first unassigned variable,
    >And it branches out ----> add it to the assigned
                         |___> dont add it to the assigned.

    We then call the solve function, with the next shallow copies of the variables.
    Returns assignment and best cost.
    """
    if current_cost >= best_cost:
        return best_cost, best_assignment

    if not flights:
        return current_cost, assignment[:]

    if not variables:
        return best_cost, best_assignment

    var = variables[0]

    assignment_take = assignment[:]
    variables_take = variables[:]
    flights_take = flights[:]

    assignment_take.append(var)
    variables_take.remove(var)

    for f in var:
        if f in flights_take:
            flights_take.remove(f)

    # prune conflicting pairings
    for v in variables_take[:]:
        if any(f in v for f in var):
            variables_take.remove(v)

    cost_take = current_cost + var[0]

    best_cost, best_assignment = solve(assignment_take,variables_take,flights_take,best_cost,cost_take,best_assignment)

    variables_skip = variables[:]
    variables_skip.remove(var)

    best_cost, best_assignment = solve(assignment,variables_skip,flights,best_cost,current_cost,best_assignment)

    return best_cost, best_assignment



flights = [] #keep track of the flights
variables = []
filename = "pairings/17x197.txt"
read_file(filename,flights,variables)

best_cost, best_assignment = solve(
    assignment=[],
    variables=variables,
    flights=flights,
    best_cost=float('inf'),
    current_cost=0,
    best_assignment=None
)

print("Best cost:", best_cost)
print("Best assignment:", best_assignment)


