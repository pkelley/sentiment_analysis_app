import nltk 
import pickle
import twitter
import sqlite3
import os
from django.db import transaction
from .models import RecentTweets, SentPercent
import re
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords 




api = twitter.Api(consumer_key='Fv3oNDnwH4BVAwMYryuKRqw6M',
                 consumer_secret='u2zhyNMsdftvZWVEZT94IbbgiH7t2YjFEjwPBopAmAwCs71yly',
                 access_token_key='518114279-N2vnFR7bawf45RsLjDSMaUmwtHwr0viwU1RH1LQ6',
                 access_token_secret='lMh2yShTVFLTZVit3jSRMAdLoN1fWN3NvBKrUHSuAf7NZ')
#print api.VerifyCredentials()
class PreProcessTweets:
    def __init__(self):
        self._stopwords=set(stopwords.words('english')+list(punctuation)+['AT_USER','URL'])
        
    def processTweets(self,list_of_tweets):
        # The list of tweets is a list of dictionaries which should have the keys, "text" and "label"
        processedTweets=[]
        # This list will be a list of tuples. Each tuple is a tweet which is a list of words and its label
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]),tweet["label"]))
        return processedTweets
    
    def _processTweet(self,tweet):
        # 1. Convert to lower case
        tweet=tweet.lower()
        # 2. Replace links with the word URL 
        tweet=re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)     
        # 3. Replace @username with "AT_USER"
        tweet=re.sub('@[^\s]+','AT_USER',tweet)
        # 4. Replace #word with word 
        tweet=re.sub(r'#([^\s]+)',r'\1',tweet)
        # 5. Replace repitions in words
        tweet = re.sub(r'(.)\1{2,}', r'\1', tweet)
        '''try:
            tweet = tweet.decode('latin1', 'ignore')
        except UnicodeEncodeError:
            tweet = tweet'''
        #print type(tweet)
        tweet=word_tokenize(tweet)
        # This tokenizes the tweet into a list of words 
        # Let's now return this list minus any stopwords 
        return [word for word in tweet if word not in self._stopwords]
def extract_features(tweet):
    
    my_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path = os.path.join(my_dir, 'word_features.pickle')
    with open(pickle_file_path, 'rb') as pickle_file:
        word_features = pickle.load(pickle_file)
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features['contains(%s)' % word]=(word in tweet_words)
        # This will give us a dictionary , with keys like 'contains word1' and 'contains word2'
        # and values as True or False 
    return features 

def startSentAnalysis(testData, search_string):
    tweetProcessor=PreProcessTweets()
    ppTestData=tweetProcessor.processTweets(testData)
    #print "Processing..."
    #open file where classifier is stored
    my_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path2 = os.path.join(my_dir, 'my_classifier.pickle')
    with open(pickle_file_path2, 'rb') as pickle_file:
        NBayesClassifier = pickle.load(pickle_file)

    NBResultLabels=[NBayesClassifier.classify(extract_features(tweet[0])) for tweet in ppTestData]
    
    #open db file from parent directory for django standards
    my_dir = os.path.dirname(__file__)
    par_dir = os.path.abspath(os.path.join(my_dir, os.pardir))
    db_file = os.path.join(par_dir, 'db.sqlite3')
    
    
    #connect and run sql on tweetDB
    '''conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('drop table if exists RecentTweets')
    sql = 'create table if not exists RecentTweets(tweet TEXT, sentiment TEXT, topic TEXT)'
    c.execute(sql)
    print 'Made table!'
    for x in range(10):
        c.execute("""
            INSERT INTO 
                RecentTweets 
            VALUES 
                (?, ?, ?)
        """, (testData[x]['text'], NBResultLabels[x], search_string))
    conn.commit()
    conn.close()'''
    #creat objects with models in django
    RecentTweets.objects.all().delete()
    SentPercent.objects.all().delete()
    for x in range(10):
        x = RecentTweets.objects.create(tweet = testData[x]['text'], sentiment = NBResultLabels[x], topic = search_string)


    if NBResultLabels.count('positive')>NBResultLabels.count('negative'):
        x = SentPercent.objects.create(topic = search_string, sent_perc = "Positive Sentiment " + str(100*NBResultLabels.count('positive')/len(NBResultLabels))+"%")
        #return "NB Result Positive Sentiment " + str(100*NBResultLabels.count('positive')/len(NBResultLabels))+"%"
    else: 
        x = SentPercent.objects.create(topic = search_string, sent_perc = "Negative Sentiment " + str(100*NBResultLabels.count('negative')/len(NBResultLabels))+"%")
        #return "NB Result Negative Sentiment " + str(100*NBResultLabels.count('negative')/len(NBResultLabels))+"%"


def createTestData(search_string):
    if search_string == "":
        return "Please give a search term"
    else:
        tweets_fetched=api.GetSearch(search_string, count=200)

        testData = [{"text":status.text,"label":None} for status in tweets_fetched]
        return startSentAnalysis(testData, search_string)
        '''try:
            tweets_fetched=api.GetSearch(search_string, count=200)

            testData = [{"text":status.text,"label":None} for status in tweets_fetched]
            return startSentAnalysis(testData)

    
        except:
            return "Sorry, an error occured."'''

