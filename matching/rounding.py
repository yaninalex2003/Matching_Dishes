import numpy as np

def rounding_procedure(relation_matrix, m):
        N_dishes = len(relation_matrix)

        clusters = []
        for i in range(N_dishes):
            clusters.append([i])

        B = np.copy(relation_matrix)
        cols = N_dishes
        while cols > m:
            A = B.T@B
            np.fill_diagonal(A, 0)
    
            i, j = np.unravel_index(A.argmax(), A.shape)
            ind1, ind2 = min(i, j), max(i, j)

            if (A[ind1][ind2] < N_dishes / (3*m)):
                break

            l1, l2 = len(clusters[ind1]), len(clusters[ind2])

            B[ind1] = (B[ind1] * l1 + B[ind2] * l2) / (l1 + l2)
            newinds = list(range(cols))
            newinds.pop(ind2)
            B = B[:, newinds]

            for el in clusters[ind2]:
                clusters[ind1].append(el)
            clusters.pop(ind2)
            cols-=1
        return clusters

def rounding_matrix(relation_matrix, m):
    clusters = rounding_procedure(relation_matrix, m)
    rounding_relation_matrix = np.zeros_like(relation_matrix)
    for cluster in clusters:
        for el1 in cluster:
            for el2 in cluster:
                rounding_relation_matrix[el1][el2] = 1
    
    return rounding_relation_matrix
