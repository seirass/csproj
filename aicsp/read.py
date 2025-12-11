from collections import defaultdict
import sys 

def read_domains(filename):
    """
    Reads the domains file
        >creates a dictionary that has a key : value of:
            >domain id : domain values
    return the dictionary.
    """
    domains = {}
    with open(filename, 'r') as file:

        lines = file.readlines()

        #skip the first line since it displays the number of domains.

        for line in lines[1:]: 
            parts = line.strip().split()
            n_dom = int(parts[0])
            values = list(map(int,parts[1:]))
            domains[n_dom] = values
        
        return domains
    
def read_variables(filename):
    """
    returns a dictionary in the form of:
        dict = {
            var1 = domain
            ...
            varn = domain
        }
    """
    variables = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.strip().split()
            n_var = int(parts[0])
            values = list(map(int,parts[1:]))
            variables[n_var] = values

        return variables

def read_constraints(filename):
    """
    reads the constraint file and adds the constraints in a dictionary in this manner:
    constraints = {
        (x,y) : ( type , k ) where type is the constraint type: = or >
        (x,y) : ( type , k ) due to the nature of the abs() the constraints are identical between the two
    }

    it also creates a dictionary called neighbors in order to map the neighboring nodes (nodes with constraints between them)
    where neighbors = {
        x : [ n1 , n2 , n3, ... nn]
    }
    as this is needed in order to correctly implement the wdeg heuristic. 
    i have provided a file, that due to a different implementation the 11th instance would complete after the universe's heat death
    """
    constraints = {}
    neighbours = defaultdict(list)

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.strip().split()
            x = int(parts[0])
            y = int(parts[1])
            type = parts[2]
            k = int(parts[3])

            constraints[(x, y)] = (type,k)
            constraints[(y, x)] = (type,k)

            neighbours[x].append(y)
            neighbours[y].append(x)
    
    return constraints,neighbours




        
