# -*- coding: utf-8 -*-

import json
from twitter_retrievers import get_following, get_users_tweets, get_home_tweets

def load_data(num_user_tweets, num_val_tweets):
	try:
		access = json.load(open('access.json'))
	except IOError :
		print "Please create an access.json file containing identifiers"
		exit(0)
	
	try:
		following_list = json.load(open('following.json'))
	except IOError :
		print "No following list found, creating one"
		get_following(access)
		try:
			following_list = json.load(open('following.json'))
		except:
			print "Failed to retrieve following list"
			exit(0)
	
	
	try:
		train_data = json.load(open('train.json'))
	except IOError :
		print "No training file found, creating one"
		get_users_tweets(access, following_list, num_user_tweets)
		try:
			train_data = json.load(open('train.json'))
		except:
			print "Failed to retrieve training tweet base"
			exit(0)
	
	
	try:
		val_data = json.load(open('val.json'))
	except IOError :
		print "No validation file found, creating one"
		get_home_tweets(access, following_list, num_val_tweets)
		try:
			val_data = json.load(open('val.json'))
		except:
			print "Failed to retrieve validation tweet base"
			exit(0)
	
	return following_list, train_data, val_data