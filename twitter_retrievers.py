# -*- coding: utf-8 -*-

import json
import re
from auth_req import oauth_req, RateLimitError


def get_following(access):
	friends_url = 'https://api.twitter.com/1.1/friends/list.json'
	options = {
		'screen_name' : access['screen_name'],
		'count' : 100
	}
	
	next_cursor = -1
	following_list = []
	while(next_cursor != 0):
		try:
			response = json.loads(oauth_req(friends_url, access, options))
		except RateLimitError :
			return False
		for user in response['users']:
			following_list.append(user['screen_name'])
		next_cursor = response['next_cursor']	
		options['cursor'] = next_cursor	
	follow_file = open('following.json', 'w')
	json.dump(following_list, follow_file)
	follow_file.close()


def get_users_tweets(access, following_list, num_tweets):
	loaded_tweets = []
	try:
		loaded_tweets = json.load(open('train.json'))
		tweets = loaded_tweets
	except IOError :
		tweets = []
	for loaded_tweet in loaded_tweets:
		if loaded_tweet[1] in following_list:
			following_list.remove(loaded_tweet[1])
			
	user_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
	options = {
		'count' : num_tweets,
		'exclude_replies' : True,
		'include_rts' : False
	}
	for name in following_list:
		options['screen_name'] = name
		try:
			user_tweets = oauth_req(user_url, access, options)
		except (RateLimitError):
			break
		for tweet in json.loads(user_tweets):
			text = re.sub(r'[\w]+://t.co/[\w]+', r'[link]', tweet['text'])
			tweets.append((text, name))
	if len(tweets) > 0:
		train_file = open('train.json', 'w')
		json.dump(tweets, train_file)
		train_file.close()
	

def get_home_tweets(access, following_list, num_tweets):
	options = {
	'count' : 100
	}
	home_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
	
	val_data = []
	id_max = -1
	while len(val_data) < num_tweets:
		if id_max > 0:
			options['max_id'] = id_max
		try:
			home_timeline = oauth_req(home_url, access, options)
		except (RateLimitError):
			break
		for tweet in json.loads(home_timeline):
			name = tweet['user']['screen_name']
			if name in following_list and tweet['text'][:4] != 'RT @':
				text = re.sub(r'[\w]+://t.co/[\w]+', r'[link]', tweet['text'])
				val_data.append((text, name))
		id_max = tweet['id']
	
	if len(val_data) > 0:
		val_file = open('val.json', 'w')
		json.dump(val_data, val_file)
		val_file.close()