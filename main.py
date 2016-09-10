# -*- coding: utf-8 -*-

from loader import load_data
from vocab import get_n_best_words
from alg_functions import vectorise, loss_calc, grad_calc
import numpy as np
from matplotlib import pyplot as plt
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
W = 0.001 * np.random.randn(relevant_words_count+2, num_following)
loss_history = []
for i in range(num_iters):
	indices = np.random.choice(num_train, batch_size)
	X_batch = X_train[indices]
	y_batch = y_train[indices]
	loss = loss_calc(X_batch, y_batch, W, reg)
	grad = grad_calc(X_batch, y_batch, W, reg)
	loss_history.append(loss)
	W -= learning_rate*grad
	if i % 100 == 0:
		print 'iteration %d / %d: loss %f' % (i, num_iters, loss)

plt.plot(loss_history)
y_train_pred = np.argmax(X_train.dot(W), axis=1)
y_val_pred = np.argmax(X_val.dot(W), axis=1)
print 'training accuracy: %f' % (np.mean(y_train == y_train_pred), )
print 'validation accuracy: %f' % (np.mean(y_val == y_val_pred), )