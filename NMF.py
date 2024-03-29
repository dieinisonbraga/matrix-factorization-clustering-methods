import numpy as np


def simple_nmf(A, k, num_iter, init_W=None, init_H=None, print_enabled=False):
    '''
    Run multiplicative updates to perform nonnegative matrix factorization on A.
    Return matrices W, H such that A = WH.
    Parameters:
        A: ndarray
            - m by n matrix to factorize
        k: int
            - integer specifying the column length of W / the row length of H
            - the resulting matrices W, H will have sizes of m by k and k by n, respectively
        num_iter: int
            - number of iterations for the multiplicative updates algorithm
        init_W: ndarray
            - m by k matrix for the initial W
        init_H: ndarray
            - k by n matrix for the initial H
        print_enabled: boolean
            - if ture, output print statements
    Returns:
        W: ndarray
            - m by k matrix where k = dim
        H: ndarray
            - k by n matrix where k = dim
    '''

    print('Applying multiplicative updates on the input matrix...')

    if print_enabled:
        print('---------------------------------------------------------------------')
        print('Frobenius norm ||A - WH||_F')
        print('')

    # Initialize W and H
    if init_W is None:
        W = np.random.rand(np.size(A, 0), k)
    else:
        W = init_W

    if init_H is None:
        H = np.random.rand(k, np.size(A, 1))
    else:
        H = init_H
    delta = 0.0000001
    # Decompose the input matrix
    for n in range(num_iter):
        
        # Update H
        W_TA = W.T @ A
        W_TWH = W.T @ W @ H + delta

        for i in range(np.size(H, 0)):
            for j in range(np.size(H, 1)):
                H[i, j] = H[i, j] * W_TA[i, j] / W_TWH[i, j]

        # Update W
        AH_T = A @ H.T
        WHH_T =  W @ H @ H.T + delta

        for i in range(np.size(W, 0)):
            for j in range(np.size(W, 1)):
                W[i, j] = W[i, j] * AH_T[i, j] / WHH_T[i, j]

        if print_enabled:
            frob_norm = np.linalg.norm(A - W @ H, 'fro')
            print("iteration " + str(n + 1) + ": " + str(frob_norm))

    return W, H



def nmf_kl(X, k, num_iter, init_W=None, init_H=None, print_enabled=False):
    '''
    Run multiplicative updates to perform nonnegative matrix factorization on X.
    Return matrices W, H such that X = WH.
    Parameters:
        X: ndarray
            - m by n matrix to factorize
        k: int
            - integer specifying the column length of W / the row length of H
            - the resulting matrices W, H will have sizes of m by k and k by n, respectively
        num_iter: int
            - number of iterations for the multiplicative updates algorithm
        init_W: ndarray
            - m by k matrix for the initial W
        init_H: ndarray
            - k by n matrix for the initial H
        print_enabled: boolean
            - if ture, output print statements
    Returns:
        W: ndarray
            - m by k matrix where k = dim
        H: ndarray
            - k by n matrix where k = dim
    '''

    print('Applying multiplicative updates on the input matrix...')
    #X = preprocessing.normalize(X, norm='l1', axis=0)

    if print_enabled:
        print('---------------------------------------------------------------------')
        print('Frobenius norm ||X - WH||_F')
        print('')

    # Initialize W and H
    if init_W is None:
        W = np.random.rand(np.size(X, 0), k)
    else:
        W = init_W

    if init_H is None:
        H = np.random.rand(k, np.size(X, 1))
    else:
        H = init_H
    delta = 0.0000001
    # Decompose the input matrix
    for n in range(num_iter):
        
        # Update H
        WH = W@H + delta
        for a in range(np.size(H, 0)):
            for j in range(np.size(H, 1)):
                 H[a,j] = H[a,j]*np.sum(W[:,a]*X[:,j]/WH[:,j])/np.sum(W[:,a])
        
        # Update W
        WH = W@H + delta
        for i in range(np.size(W, 0)):
            for a in range(np.size(W, 1)):                
                W[i,a] = W[i,a]*np.sum(H[a,:]*X[i,:]/WH[i,:])/np.sum(H[a,:])
        

        if print_enabled:
            frob_norm = np.linalg.norm(X - W @ H, 'fro')
            print("iteration " + str(n + 1) + ": " + str(frob_norm))

    return W, H

def KL(a, b):
    a = np.asarray(a, dtype=np.float)
    b = np.asarray(b, dtype=np.float)

    return np.sum(np.where(a != 0, a * np.log(a / b), 0))
