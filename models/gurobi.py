# Import packages
import gurobipy as gp
from gurobipy import GRB

def gp_solver(indices: set, lhs_terms: list, rhs: list, constraints: dict, verbose: bool) -> dict:
    """ Run the Gurobi solver """

    # Create a model
    if not verbose:
        # Suppress output if verbose false
        env = gp.Env(empty=True)
        env.setParam("OutputFlag",0)
        env.start()
        model = gp.Model("visma", env=env)
    else:
        model = gp.Model('visma')

    # List of indices to assign values to. That is, here x_ik = 1 if and only if integer k in integers is assigned to index i in indices. 
    integers: list[int] = [*range(len(indices))]
    x = model.addVars(indices, integers, vtype=GRB.BINARY, name="x")

    # Constraints

    # Each variable must be assigned to exactly one index
    c1 = model.addConstrs((x.sum(i, '*') == 1 for i in indices), name="binary")

    # Each value should only appear once, i.e. distinct variables
    c2 = model.addConstrs((x.sum('*', k) == 1 for k in integers), name="distinct")

    # Equation constraint, i.e. lhs = rhs
    lhs_sum = 0
    for term in lhs_terms:
        for idx, letter in enumerate(term):
            for k in integers:
                lhs_sum += x[letter, k] * k * 10**(len(term) - idx - 1)

    rhs_sum = 0
    for idx, letter in enumerate(rhs):
        for k in integers:
            rhs_sum += x[letter, k] * k * 10**(len(rhs) - idx - 1)

    # Main constraint, the cryptarithmetic equation
    c3 = model.addConstr(lhs_sum == rhs_sum, name="equation")

    # Additional constraints
    for con_key, con_value in constraints.items():
        ah = model.addConstr(x[con_key, con_value] == 0, name=f"{con_key}_not_{con_value}")

    # Objectice
    model.setObjective(sum(x[i, k] for i in indices for k in integers), gp.GRB.MAXIMIZE)

    # Verify model formulation
    # model.write('visma.lp')

    # Run optimization engine
    model.optimize()

    # Output report
    result: dict = {}
    for v in list(filter(lambda v: v.x == 1, model.getVars())):
        result[v.varName[4:5]] = v.varName[2:3]

    return result
