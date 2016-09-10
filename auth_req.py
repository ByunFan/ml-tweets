import oauth2

class RateLimitError(Exception):
	pass

def oauth_req(url, access, options={},  http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=access['consumer_key'], secret=access['consumer_secret'])
    token = oauth2.Token(key=access['token_key'], secret=access['token_secret'])
    client = oauth2.Client(consumer, token)
    url = url_maker(url, options)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    if int(resp['x-rate-limit-remaining']) < 1:
        print "End of capacity for this window, try again in 15 minutes"
        raise RateLimitError()
    return content

def url_maker(url,options):
	if options != {}:
		first_opt = True
		for key in options:
			if first_opt:
				url += '?'
				first_opt = False
			else:
				url += '&'
			url += key + '=' + str(options[key])
	return url

