from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import codecs
import os


#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""


print("FileName:")
fn  = input()
file_name = "data/"+fn+".txt"


keywords = ["Goa","Punjab", "Election", "Aap", "BJP", "Congress"]

class listener(StreamListener):
	def __init__(self):
		self.n = 0
	
	def on_data(self, data):
		try:
			all_data = json.loads(data)
			print(all_data['text'])
			with open(file_name, "a") as f:
				f.write(all_data['text'].lower())
				f.write("\n")
			return(True)
		except:
			return True
	def on_error(self, status):
		print(status)

	
def get_tweet():
	try:
		auth = OAuthHandler(ckey, csecret)
		auth.set_access_token(atoken, asecret)
		twitterStream = Stream(auth, listener())
		print("Starting streaming on %s" % keywords)
		twitterStream.filter(languages=["en"], track=keywords)
	except:
		return True

get_tweet()

