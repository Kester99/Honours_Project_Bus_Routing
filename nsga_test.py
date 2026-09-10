from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.problems import get_problem

problem = get_problem("zdt1")

algorithm = NSGA2(pop_size=100)

result = minimize(
    problem,
    algorithm,
    termination=("n_gen", 100),
    seed=1,
    verbose=True
)

print(result.X)
print(result.F)