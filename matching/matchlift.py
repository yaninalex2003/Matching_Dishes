import numpy as np
import cvxpy as cp

def match_lift(M, m, lam = 0.5):
    N_dishes = len(M)

    X_opt = cp.Variable((N_dishes, N_dishes), value = M, symmetric=True)
    W = lam * np.ones((N_dishes, N_dishes)) - M
    X_wide  = X_opt - np.ones((N_dishes, N_dishes)) / m

    objective = cp.Minimize(cp.scalar_product(W, X_opt))
    constraints = [ cp.diag(X_opt) == np.ones(N_dishes), X_wide >> 0, X_opt >= 0, 1 >= X_opt]

    cp.Problem(objective, constraints).solve()
    return X_opt.value
