import numpy as np

def estimate_m(M):
        eigenvalues, _ = np.linalg.eig(M)

        lambda_i_list = np.sort(eigenvalues)[::-1]

        diffs = np.abs(np.diff(lambda_i_list))

        M = 10
        diffs=diffs[M:]
        m_est = np.argmax(diffs) 

        return m_est + M
