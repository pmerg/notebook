#! /usr/bin/env python 
import tweepy
from datetime import datetime
from conf import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

TWITTER_USER='vrypan'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

today = datetime.now().strftime('%Y%m%d')

last_tweet_id = 766619861816606720
first_tweet_id = ''

output = ''

try: 
	f = open('.last_tweet_id')
	last_tweet_id = int(f.read())
	f.close()
except:
	pass

for statuses in tweepy.Cursor(api.user_timeline, screen_name=TWITTER_USER).pages():
	for s in statuses:
		if not first_tweet_id:
			first_tweet_id = s.id_str
		# if s.created_at.strftime('%Y%m%d') == today:
		if s.id <= last_tweet_id:
			break;
		if s.retweeted:
			text = "RT   \n\>\>\> @%s:%s" % (s.retweeted_status.user.screen_name, s.retweeted_status.text)
		elif hasattr(s,'quoted_status'):
			text = "%s   \n\>\>\> @%s:%s" % (s.text, s.quoted_status['user']['screen_name'], s.quoted_status['text'])
		else:
			text = s.text

		t = "[%s](https://twitter.com/%s/status/%s): %s\n" % (
			s.created_at.strftime('%Y-%m-%d %H:%M'),
			TWITTER_USER,
			s.id_str,
			text)
		for l in s.entities['urls']:
			t = t.replace(l['url'], '[%s](%s)' % (l['url'], l['expanded_url']))
		if 'media' in s.entities:
			for l in s.entities['media']:
				t = t.replace(l['url'], '[%s](%s)' % (l['type'], l['expanded_url']))
		output = "%s\n%s" % (output, t)
	#if s.created_at.strftime('%Y%m%d') != today:
	if s.id <= last_tweet_id:
		break

with open('.last_tweet_id', 'w') as f:
	if s:
		f.write(first_tweet_id)
	f.close()

if output:
	print "\n## my recent tweets"
	print output.encode('utf-8')