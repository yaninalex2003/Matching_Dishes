import numpy as np

def one_step_closure(M: np.matrix):
    M_cl = M.copy()
    adding = []
    for i in range(M_cl.shape[0]):
        for j in range(i, M_cl.shape[0]):
            for k in range(M_cl.shape[0]):
                if M_cl[i][k] == 1 and M_cl[j][k] == 1:
                    adding.append((i,j))
    for (a, b) in adding:
        M_cl[a][b] = 1
        M_cl[b][a] = 1
    return M_cl
