
import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse 

class MF(object):

    def __init__(self, Y_data, K, lam = 0.1, Xinit = None, Winit = None, learning_rate = 0.5, max_iter = 1000, print_every = 100, user_based = 0):
        self.Y_raw = Y_data.copy()
        self.Y_data = Y_data.copy()
        self.K = K
        self.lam = lam
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.print_every = print_every
        self.user_based = user_based

        self.n_users = int(np.max(Y_data[:, 0])) + 1 
        self.n_items = int(np.max(Y_data[:, 1])) + 1
        
        if Xinit is None: 
            self.X = np.random.randn(self.n_items, K)
        else:
            self.X = Xinit 
        
        if Winit is None: 
            self.W = np.random.randn(K, self.n_users)
        else: 
            self.W = Winit
        
        # item biases
        self.b = np.random.randn(self.n_items)
        self.d = np.random.randn(self.n_users)
        self.n_ratings = Y_data.shape[0]
        self.mu = 0

    def normalize_Y(self):
        if self.user_based:
            user_col = 0
            item_col = 1
            n_objects = self.n_users
        else:
            user_col = 1
            item_col = 0 
            n_objects = self.n_items

        users = self.Y_data[:, user_col] 
        self.muu = np.zeros((n_objects,))
        for n in range(n_objects):
            ids = np.where(users == n)[0].astype(np.int32)
            item_ids = self.Y_data[ids, item_col]  
            ratings = self.Y_data[ids, 2]
            m = np.mean(ratings) 
            if np.isnan(m):
                m = 0
            self.muu[n] = m
            self.Y_data[ids, 2] = ratings - m       
            
    def loss(self):
        L = 0 
        for i in range(self.n_ratings):
            n, m, rate = int(self.Y_data[i, 0]), int(self.Y_data[i, 1]), self.Y_data[i, 2]
            L += 0.5*(self.X[m, :].dot(self.W[:, n]) + self.b[m] + self.d[n] + self.mu - rate)**2
            
        # regularization
        L /= self.n_ratings
        L += 0.5*self.lam*(np.linalg.norm(self.X, 'fro') + np.linalg.norm(self.W, 'fro') + \
                          np.linalg.norm(self.b) + np.linalg.norm(self.d))
        return L 

    
    def get_items_rated_by_user(self, user_id):
        ids = np.where(self.Y_data[:,0] == user_id)[0] 
        item_ids = self.Y_data[ids, 1].astype(np.int32)
        ratings = self.Y_data[ids, 2]
        return (item_ids, ratings)
        
    def get_users_who_rate_item(self, item_id):
        ids = np.where(self.Y_data[:,1] == item_id)[0] 
        user_ids = self.Y_data[ids, 0].astype(np.int32)
        ratings = self.Y_data[ids, 2]
        return (user_ids, ratings)
        
    def updateX(self):
        for m in range(self.n_items):
            user_ids, ratings = self.get_users_who_rate_item(m)
            
            Wm = self.W[:, user_ids]
            dm = self.d[user_ids]
            xm = self.X[m, :]
            
            error = xm.dot(Wm) + self.b[m] + dm + self.mu - ratings 
            
            grad_xm = error.dot(Wm.T)/self.n_ratings + self.lam*xm
            grad_bm = np.sum(error)/self.n_ratings + self.lam*self.b[m]
            self.X[m, :] -= self.learning_rate*grad_xm.reshape((self.K,))
            self.b[m]    -= self.learning_rate*grad_bm
    
    def updateW(self):
        for n in range(self.n_users):
            item_ids, ratings = self.get_items_rated_by_user(n)
            Xn = self.X[item_ids, :]
            bn = self.b[item_ids]
            wn = self.W[:, n]
            
            error = Xn.dot(wn) + bn + self.mu + self.d[n] - ratings
            grad_wn = Xn.T.dot(error)/self.n_ratings + self.lam*wn
            grad_dn = np.sum(error)/self.n_ratings + self.lam*self.d[n]
            self.W[:, n] -= self.learning_rate*grad_wn.reshape((self.K,))
            self.d[n]    -= self.learning_rate*grad_dn
    
    def fit(self):
        self.normalize_Y()
        for it in range(self.max_iter):
            self.updateX()
            self.updateW()
            if (it + 1) % self.print_every == 0:
                rmse_train = self.evaluate_RMSE(self.Y_raw)
                print ('iter =', it + 1, ', loss =', self.loss(), ', RMSE train =', rmse_train)
    
    
    def pred(self, u, i):
        u = int(u)
        i = int(i)
        if self.user_based == 1:
            bias = self.muu[u]
        else:
            bias = self.muu[i]
        
        pred = self.X[i, :].dot(self.W[:, u]) + self.b[i] + self.d[u] + bias
#         if pred < 0:
#             return 0 
#         if pred > 5: 
#             return 5 
#         return pred 
        return max(0, min(5, pred)) 
    
    def pred_for_user(self, user_id):
        ids = np.where(self.Y_data_n[:, 0] == user_id)[0]
        items_rated_by_u = self.Y_data_n[ids, 1].tolist()              
        
        y_pred = self.X.dot(self.W[:, user_id])
        predicted_ratings= []
        for i in range(self.n_items):
            if i not in items_rated_by_u:
                predicted_ratings.append((i, y_pred[i]))
        return predicted_ratings
    
    def evaluate_RMSE(self, rate_test):
        n_tests = rate_test.shape[0]
        SE = 0 
        for n in range(n_tests):
            pred = self.pred(rate_test[n, 0], rate_test[n, 1])
            SE += (pred - rate_test[n, 2])**2 

        RMSE = np.sqrt(SE/n_tests)
        return RMSE
'''
#Example       
r_cols = ['user_id', 'item_id', 'rating']
ratings = pd.read_csv('ex.dat', sep = ' ', names = r_cols, encoding='latin-1')
Y_data = ratings.values

rs = MF(Y_data, K = 3, max_iter = 1000, print_every = 100, lam = 0.1)

rs.fit()
rs.pred(6, 1)
print ('RMSE_train = ', rs.evaluate_RMSE(Y_data))
'''

#Load data
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

ratings_base = pd.read_csv('ml-100k/ub.base', sep='\t', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('ml-100k/ub.test', sep='\t', names=r_cols, encoding='latin-1')

rate_train = ratings_base.values
rate_test = ratings_test.values

rate_train[:, :2] -= 1
rate_test[:, :2] -= 1

#user
rs = MF(rate_train, K = 100, lam = .01, print_every = 20, learning_rate = 2, max_iter = 200)
rs.fit()

RMSE = rs.evaluate_RMSE(rate_test)
print ('\nUser-based MF, RMSE =', RMSE)
'''
#item
rs = MF(rate_train, K = 2, lam = 0.1, print_every = 2, learning_rate = 2, 
        max_iter = 50, user_based = 0, Xinit = rs.X, Winit = rs.W)
rs.fit()

RMSE = rs.evaluate_RMSE(rate_test)
print ('\nItem-based MF, RMSE =', RMSE)
'''