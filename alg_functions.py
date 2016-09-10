# -*- coding: utf-8 -*-

import numpy as np

def vectorise(following_list, data, best_words_list):
	X = np.zeros((len(data), len(best_words_list)+1))
	y = np.zeros(len(data), dtype=np.int)
	indice = 0
	for tweet in data:
		y[indice] = following_list.index(tweet[1])
		for word in tweet[0].split():
			if word in best_words_list:
				X[indice][best_words_list.index(word)] += 1
			else:
				X[indice][len(best_words_list)] += 1
		indice += 1
	return X, y

def loss_calc(X, y, W, reg):
	scores = X.dot(W)
	correct_scores = scores[np.arange(X.shape[0]), y]
	scores -= np.reshape(correct_scores, (-1,1))
	scores = np.maximum(scores + 1, 0)
	loss_lines = np.sum(scores, axis=1) - 1
	loss = np.mean(loss_lines) + 0.5 * reg * np.sum(W*W)
	return loss
	

def grad_calc(X, y, W, reg):
	scores = X.dot(W)
	correct_scores = scores[np.arange(X.shape[0]), y]
	scores -= np.reshape(correct_scores, (-1,1))
	scores = np.maximum(scores + 1, 0)
	scores = np.nan_to_num(scores / scores)
	sum_bin = np.sum(scores, axis=1)
	scores[np.arange(X.shape[0]),y] -= sum_bin
	dW = X.T.dot(scores)
	dW /= X.shape[0]
	dW += reg * W
	return dW