# -*- coding: utf-8 -*-

def get_n_best_words(train_data, relevant_words_count):
	entire_dict = {}
	for tweet in train_data:
		for word in tweet[0].split():
			if word in entire_dict:
				entire_dict[word] += 1
			else:
				entire_dict[word] = 1
				
	def dict_sort(tuple):
		return tuple[1]
	
	best_words = sorted(entire_dict.items(), key=dict_sort, reverse=True)
	best_words = best_words[:relevant_words_count]
	best_words_list = [w[0] for w in best_words]
	return best_words_list

