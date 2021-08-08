import requests
from bs4 import BeautifulSoup
import config
import pandas as pd
import tweepy
import re
from tweepy import OAuthHandler
# from tweets import TwitterClient
from datetime import datetime

#getting the tweets

terms_list = []
with open("terms.txt", "r") as terms:
    for line in terms:
        stripped = line.strip()
        terms_list.append(stripped)

term1 = terms_list[0]
term2 = terms_list[1]
term3 = terms_list[2]
term4 = terms_list[3]
term5 = terms_list[4]

# Getting the url from the text File Amazon
url_list = []
with open("term.txt", "r") as term:
    for line in term:
        stripped = line.strip()
        url_list.append(stripped)

watch1 = url_list[4]
watch2 = url_list[1]
watch3 = url_list[2]
watch4 = url_list[3]
watch5 = url_list[0]


#scrappings

#We use Splash to render the page for us and return the raw HTML which we can parse and extract the information we want.
review_list = []
def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, "html.parser")
    return soup



def get_reviews(soup):

    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
                "SID": item["id"],
                'Product': soup.title.text.replace('Amazon.de:Customer Reviews: ', '').replace('Amazon.de:Kundenrezensionen: ', '').strip(),
                'User': item.find("span", {"class": "a-profile-name"}).text.strip(),
                'Date' : item.find("span", {"data-hook": "review-date" }).text.split('vom ')[-1].split('on ')[-1].replace('.', "").replace(' ', "-").replace('Januar', '01').replace('Februar', '02').replace('März', '03').replace('April', '04').replace('Juni', '06').replace('Mai', '05').replace('Juli', '07').replace('August', '08').replace('September', '09').replace('Oktober', '10').replace('November', '11').replace('Dezember', '12').strip(),
                'Message': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            review_list.append(review)
    except:
        pass


#Getting all pages
def get_all_reviews(urls):
    for x in range(200):
        soup1 = get_soup(urls + str(x))
        print(f'getting page: {x}')
        get_reviews(soup1)
        print(len(review_list))


        if not soup1.find("li", {"class": "a-disabled a-list"}):
            pass
        else:
            break




#Twitter
class TwitterClient(object):
	def __init__(self):

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(config.consumer_key, config.consumer_secret)
			# set access token and secret
			self.auth.set_access_token(config.access_token, config.access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
				return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


	def get_tweets(self, query, count = 10):
		tweets = []

		try:
			# call twitter api
			fetched_tweets = self.api.search(q = query, count = count)

			for tweet in fetched_tweets:
				parsed_tweet = {}

				# saving SID of tweet
				parsed_tweet['SID'] = tweet.id
				# saving User of tweet
				parsed_tweet['User'] = tweet.user.id
				# saving Date of tweet
				parsed_tweet['Date'] = tweet.created_at
				# saving Message of tweet
				parsed_tweet['Message'] = tweet.text.encode("utf-8")

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
						if parsed_tweet not in tweets:
							tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# creating the dataframe
			tweetsFrame = pd.DataFrame(tweets)
			tweetsFrame["Product"] = query
			tweetsFrame["Sentiment"] = ""
			columnss = ['SID', 'Product', 'User', 'Date', 'Message', 'Sentiment']
			tweetsFrame.reindex(columns=columnss)

			return tweetsFrame

		except tweepy.TweepError as e:
			print("Error : " + str(e))







#Scrapping using the functions and defining the columns
get_all_reviews(watch1)
get_all_reviews(watch2)
get_all_reviews(watch3)
get_all_reviews(watch4)
get_all_reviews(watch5)


def main():
	api = TwitterClient()

	# calling function to get tweets
	a = api.get_tweets(query=term1, count=200)
	b = api.get_tweets(query=term2, count=200)
	c = api.get_tweets(query=term3, count=200)
	d = api.get_tweets(query=term4, count=200)
	e = api.get_tweets(query=term5, count=200)
	tweets = a.append([b, c, d, e])


	print(tweets)

	amazonFrame = pd.DataFrame(review_list)
	combinedFrame = pd.concat([amazonFrame, tweets])
	# Unifying the columns
	columns = ['SID', 'Product', 'User', 'Date', 'Message', 'Sentiment']
	combinedFrame.reindex(columns=columns)
	combinedFrame = combinedFrame.set_index('SID')
	combinedFrame = combinedFrame.applymap(str)

	combinedFrame.loc[(combinedFrame.Date == '01y'), 'Date'] = '01'
	combinedFrame
	combinedFrame = combinedFrame.applymap(str)

	return combinedFrame
	print(combinedFrame)

	# Getting rid of the duplicates
	combinedFrame.drop_duplicates(keep='first')


mainFrame = main()

if __name__ == "__main__":
	main()




# Creating the Database
from sqlalchemy import create_engine
engine = create_engine('sqlite:///save_pandas.db', echo=True)
sqlite_connection = engine.connect()
sqlite_table = "DATA"
mainFrame.to_sql(sqlite_table, sqlite_connection, if_exists="replace")
sqlite_connection.close()



