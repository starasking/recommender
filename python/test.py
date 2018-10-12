from IPython.display import Image, HTML
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as la
import re

rows = 5
cols = 4
#Y = np.array([[5, 5, 0, 0],
              #[5, -1, -1, 0],
              #[-1, 4, 0, -1],
              #[0, 0, 5, 4],
              #[0, 0, 5, -1]], np.float32)

Y = np.array([[5, 5, 0, 0],
              [1, -1, -1, 0],
              [-1, -1, 1, -1],
              [-1, 1, -1, -1],
              [-1, -1, -1, 1]], np.float32)

D = (Y > -0.5).astype(float)
Y_norm = Y -  np.matmul(np.array([Y.mean(1)]).transpose(), np.ones((1, Y.shape[1])))

# gradient descent
# X, Y, Theta are matrix
# T for Theta, c for coefficient, a for alpha, b for beta
# a, b need to be decided by validation set, as the frist approcimation, ingore them

coefficient = 1.0 / float(np.count_nonzero(D))
c = coefficient
learning_rate = 0.1
small_co = 1

# cost function
# (DELTA)_ij = 0 when utility_ij = nan, else (DELTA)_ij = 1
# cost_function = 0.5 * (c * ((XT - Y)(DELTS))^2 + a * T * T + b * X * X)
# X: N x K, T as Theta: K x M, Y: N x M
# N: num of items, M: num of user, K: dimention of latent features
# We consider K = M for rank consideration

N = Y.shape[0]
M = Y.shape[1]
K = min(M, N) 

X = np.random.rand(N, K) * small_co
T = np.random.rand(K, M) * small_co

iter_total = 200000
internal = 10000

# diffiential
# x_ik = x_ik - learning_rate * (c * (x_il * t_lj - y_ij)(delta_ij) * t_kj + a * x_ik) // check!!!
# t_kj = t_kj - learning_rate * (c * x_ik * (x_il * t_lj - y_ij)(delta_ij) + b * t_kj)  
print "Start to iterate...."

def cost_function(X, T, Y, c):
    for i in range(0, iter_total):
        medium = (np.matmul(X, T) - Y) * D
        X = X - learning_rate * c * np.matmul(medium, T.transpose())
        T = T - learning_rate * c * np.matmul(X.transpose(), medium)
        cost = la.norm((np.matmul(X, T) - Y) * D) * c 
        raw_input("Press Enter to continue ...")
        print "========================================="
        print (np.matmul(X, T) - Y)*D
        print "----------------------------"
        print np.matmul(X, T)
        print Y * D
        print(cost)
        print(np.count_nonzero((np.matmul(X, T) - Y)> 1))
cost_function(X, T, Y, c)
#plt.plot(t_tmp, x_tmp)
#plt.plot(t_tmp, y_tmp)
