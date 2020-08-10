import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import linear_model
from sklearn.linear_model import Ridge
import math

#Reading user file:
u_cols =  ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols,
 encoding='latin-1')

n_users = users.shape[0]
#print ("Number of users:'", n_users)
#print(users.head())

# Reading items file:
i_cols = ['movie id', 'movie title' ,'release date','video release date',
'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s',
'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

items = pd.read_csv('ml-100k/u.item', sep='|', names=i_cols, encoding='latin-1')

n_items = items.shape[0]
#print("Number of items: ", n_items)
#print(items.head())

#Reading ratings file:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

ratings_base = pd.read_csv('ml-100k/ua.base', sep='\t', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('ml-100k/ua.test', sep='\t', names=r_cols, encoding='latin-1')

rate_train = ratings_base.values
rate_test = ratings_test.values

#print ('Number of traing rates:', rate_train.shape[0])
#print(ratings_base.head())
#print('Number of test rates:', rate_test.shape[0])
#print(ratings_test.head())

X0 = items.values
X_train_counts = X0[:, -19:]
#print(X_train_counts)

# tfidf
transformer = TfidfTransformer(smooth_idf=True, norm='l2')
tfidf = transformer.fit_transform(X_train_counts.tolist()).toarray()

def get_items_rated_by_user(rate_matrix, user_id):
    y = rate_matrix[:,0]
    ids = np.where(y == user_id+1)[0]
    items_ids = rate_matrix[ids,1]-1
    scores = rate_matrix[ids,2]
    return(items_ids, scores)

d = tfidf.shape[1]
W = np.zeros((d,n_users))
b = np.zeros((1, n_users))

for n in range(n_users):
    ids, scores = get_items_rated_by_user(rate_train, n)
    clf = Ridge(alpha=0.01, fit_intercept=True)
    Xhat = tfidf[ids,:]

    clf.fit(Xhat, scores)
    W[:,n]=clf.coef_
    b[0,n]=clf.intercept_

# predicted scores
Yhat = tfidf.dot(W)+b

# Example with id_user = 10
n = 10
np.set_printoptions(precision=2)
ids, scores = get_items_rated_by_user(rate_test,n)
Yhat[n,ids]
print("Rated movies ids : ", ids)
print("True ratings     : ", scores)
print("Predicted ratings: ", Yhat[ids,n])

# RMSE
def evalute(Yhat, rates, W, b):
    se = 0
    cnt = 0
    for n in range(n_users):
        ids, scores_truth = get_items_rated_by_user(rates,n)
        scores_pred = Yhat[ids,n]
        e = scores_truth-scores_pred
        se += (e*e).sum(axis = 0)
        cnt += e.size
    return math.sqrt(se/cnt)

print("RMSE for training: ", evalute(Yhat, rate_train, W, b))
print("RMSE for test    : ", evalute(Yhat, rate_test, n, b))