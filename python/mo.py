# run with python3
import numpy as np
import re
import math
import sys
import codecs

user_list = []
users_products = []
product_set = set()

with open("../data/mo_itemCF_related") as infile:
    for line in infile.readlines():
        value = line.split()
        user_list.append(value[0])
        products = re.findall('[0-9]+', value[1])   #TODO better find
        for product in products:
            product_set.add(product)
        users_products.append(products)

items_dict = dict()
with open("../data/mo_items.output") as infile:
    for line in infile.readlines():
        value = line.split()
        items_dict[value[0]] = value[1:]

product_list = list(product_set)
#print(len(product_list))
#print(product_list)
#print(items_dict)
#input("press enter to continue...")
dims = len(product_list)

user_itemSet_dict = dict()
user_itemMatrix_list = []

for i in range(0, len(user_list)):
    item_unit_matrix = np.zeros((dims, dims))
    user_indexs = []
    user_itemSet_dict[user_list[i]] = set(users_products[i])
    for product in set(users_products[i]):
        user_indexs.append(product_list.index(product))
    for i_idx in user_indexs:
        for j_idx in user_indexs:
            item_unit_matrix[i_idx][j_idx] = 1
    user_itemMatrix_list.append(item_unit_matrix)

item_matrix = sum(user_itemMatrix_list)
similarity = np.zeros((dims, dims))
A = np.zeros((dims, dims))

for i in range(0, dims):
    for j in range(0, dims):
        similarity[i][j] = item_matrix[i][j]/math.sqrt(item_matrix[i][i] * item_matrix[j][j])
        if (i != j ):
            A[i][j] = similarity[i][j]

similarity_normed = A * 1./np.max(A, axis = 0)

normed_sorted = np.argsort(-similarity_normed, axis = 1)
without_normed_sorted = np.argsort(-A, axis = 1)
for i in range(0, dims):
    for j in range(1, 11):
        #print(items_dict[product_list[i]], items_dict[product_list[j]], similarity_normed[i][j]) 
        #print(items_dict[product_list[i]],
                #items_dict[product_list[normed_sorted[i][j]]],
                #similarity_normed[i][normed_sorted[i][j]]) 
        print(items_dict[product_list[i]],
                items_dict[product_list[without_normed_sorted[i][j]]],
                A[i][without_normed_sorted[i][j]]) 
        #input("press key to continue...")

#print np.set_printoptions(threshold=np.inf)
#save  procuct_list,  user_itemSet_dict, item_matrix
