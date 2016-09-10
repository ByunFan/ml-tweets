# -*- coding: utf-8 -*-

import numpy as np

def loss_calc(X, y, W, reg):
	scores = X.dot(W)
	correct_scores = scores[np.arange(X.shape[0]), y-1]
	scores -= np.reshape(correct_scores, (-1,1))
	scores = np.maximum(scores + 1, 0)
	loss_lines = np.sum(scores, axis=1) - 1
	loss = np.mean(loss_lines) + 0.5 * reg * np.sum(W*W)
	return loss
	

def grad_calc(X, y, W, reg):
	scores = X.dot(W)
	correct_scores = scores[np.arange(X.shape[0]), y-1]
	scores -= np.reshape(correct_scores, (-1,1))
	scores = np.maximum(scores + 1, 0)
	scores = np.nan_to_num(scores / scores)
	sum_bin = np.sum(scores, axis=1)
	scores[np.arange(X.shape[0]),y-1] -= sum_bin
	dW = X.T.dot(scores)
	dW /= X.shape[0]
	dW += reg * W
	return dW