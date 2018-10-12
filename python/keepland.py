import pandas as pd
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
import random
import collections
import re

# read data from file to database
# depending on the format of the input file
# TODO: replace the codes below by using more concise and sophisticated functions
userid = []
times = []
score_list = []
course_list = []
time_list = []

with open("../data/keepland") as infile:
    for line in infile.readlines():
        value = line.split(";")
        userid.append(value[0])
        times.append(int(value[1]))
        course_list.append(re.findall('"([^"]*)"', value[2]))
        score_list.append(value[3])
        time_list.append(re.findall('"([^"]*)"', value[4]))

db = pd.DataFrame(columns = ['times', 'course_list', 'scoure_list', 'time_list'], index = userid)
db['times'] = times
db['score_list'] = score_list
db['course_list'] = course_list
db['time_list'] = time_list

course_set = set()
total_course_list = []
num_user = db.shape[0]
for row in range(0, num_user):
    for course in db['course_list'][row]:
        course_set.add(course)
        total_course_list.append(course)
num_class = len(course_set)

print("Basic statistic information of keepland in August of 2018")
print("Number of users: {}".format(num_user))
print("Number of classes: {}".format(num_class))
print("Number of attendances: {}".format(len(total_course_list)))
print("Times of attendance of users:")
print("max = {}, min = {}, avg = {}".format(db['times'].max(), db['times'].min(), db['times'].mean()))
print("There are {} users who only attended once".format(times.count(1)))
print("Popularity of classes:")
counter = collections.Counter(total_course_list)
print(counter.values())

subset_30 = [ i for i in times if i >= 30]
subset_1to10 = [ i for i in times if i < 11]
subset_11to30 = [ i for i in times if i >= 11 and i < 30]

fig, axes = plt.subplots(nrows = 2, ncols = 2)
ax0, ax1, ax2, ax3 = axes.flatten()

ax0.hist(times, bins = 30)
ax0.set_title('histgram of kl-class in 2018-08')

ax1.hist(subset_1to10, bins = 10)
ax2.hist(subset_11to30, bins = 20)
ax3.hist(subset_30, bins = 7)
fig.tight_layout()
#plt.show()

# utility matrix
utility = np.zeros((num_class, num_user))
print utility.shape
courses = list(course_set)

for u in range(0, num_user):
    for c in db['course_list'][u]:
        for i in range(0, len(courses)):
            if c == courses[i]:
                utility[i][u] += 1

#latent factor model

# musk matrix
def get_random_matrix(U, ratio):
    rows = U.shape[0]
    cols = U.shape[1]
    D = np.ones((rows, cols))
    for i in range(0, rows):
        for j in range(0, cols):
            if(U[i][j] == 0):
                randtmp = random.uniform(0, 1)
                if(randtmp > ratio):
                    D[i][j] = 0
    return D

def learn_utility(X, T, Y, D, c, l, iter_total, num_recom):
    for i in range(0, iter_total):
        M = (np.matmul(X, T) - Y) * D
        X = X - l * c * np.matmul(M, T.transpose())
        T = T - l * c * np.matmul(X.transpose(), M)
        cost = la.norm(M)
        recoms = np.argsort(-np.matmul(X, T), axis = 0)
        np.delete(recoms, np.s_[num_recom:], axis = 0)
    return cost, recoms

def training(U, init_co_x, init_co_t, iter_total, learning_rate, ratio, num_recom):
    Y = U
    M = U.shape[1]
    N = U.shape[0]
    K = min(U.shape[0], U.shape[1])
    X = np.random.rand(N, K) * init_co_x
    T = np.random.rand(K, M) * init_co_t

    D = get_random_matrix(Y, ratio)
    coefficient = 1.0 / float(np.count_nonzero(D))
    cost, recoms = learn_utility(X, T, Y, D, coefficient, learning_rate, iter_total, num_recom)
    return recoms

#parameters
learning_rate = 0.2
init_co_x = 5 # amplitude of randomly initialized maxtix 
init_co_t = 5 # amplitude of randomly initialized maxtix 
iter_total = 10000
sample_num = 1 #10
ratio = 0.9 # 0.9 for recommend, 1 - 0.9 for training
num_recom = num_class # the frist num_recommmended classes num_recom <= num_class

# trainging result
recoms = training(utility, init_co_x, init_co_t, iter_total, learning_rate, ratio, num_recom)
np.set_printoptions(threshold=np.inf)
print "=================================================================================================="
print recoms[:, :15]
print '--------------------------------------------------------------------------------------------------'
print utility[:, :15]

#def training_sample_avg(){}
