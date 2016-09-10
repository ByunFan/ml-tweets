# -*- coding: utf-8 -*-

from loader import load_data
from vocab import get_n_best_words
from alg_functions import vectorise, svm_train, evaluate
import numpy as np
num_user_tweets = 200
num_val_tweets = 500

following_list, train_data, val_data = load_data(num_user_tweets, num_val_tweets)

num_following = len(following_list)
num_train = len(train_data)
num_val = len(val_data)

relevant_words_count = 5000
best_words_list = get_n_best_words(train_data, relevant_words_count)

X_train, y_train = vectorise(following_list, train_data, best_words_list)
X_val, y_val = vectorise(following_list, val_data, best_words_list)

mean_values = np.mean(X_train, axis=0)
X_train -= mean_values
X_val -= mean_values

variance = np.var(X_train, axis=0)
X_train /= variance
X_val /= variance

X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))])
X_val = np.hstack([X_val, np.ones((X_val.shape[0], 1))])

learning_rate = 0.001
reg = 0.01
num_iters = 2000
batch_size = 500

W = svm_train(X_train, y_train, num_iters, batch_size, reg, learning_rate)

evaluate(X_train, y_train, W, 'Training')
evaluate(X_val, y_val, W, 'Validation')

ics = np.random.choice(num_val, 1)
for i in ics:
	print val_data[i]
	#print following_list[y_val_pred[i]]
	
	
ixs = np.random.choice(num_following, 1)
for i in ixs:
	i = 18
	print following_list[i]
	col = W[:,i]
	args = col.argsort()[-10:][::-1]
	for arg in args:
		print best_words_list[arg]
	print ' - - -'
	args = col.argsort()[:10][::1]
	for arg in args:
		print best_words_list[arg]