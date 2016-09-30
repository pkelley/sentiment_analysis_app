import twitter
import os
import cPickle as pickle


api = twitter.Api(consumer_key='Fv3oNDnwH4BVAwMYryuKRqw6M',
                 consumer_secret='u2zhyNMsdftvZWVEZT94IbbgiH7t2YjFEjwPBopAmAwCs71yly',
                 access_token_key='518114279-N2vnFR7bawf45RsLjDSMaUmwtHwr0viwU1RH1LQ6',
                 access_token_secret='lMh2yShTVFLTZVit3jSRMAdLoN1fWN3NvBKrUHSuAf7NZ')
#print api.VerifyCredentials()

def createTestData(search_string):
    try:
        tweets_fetched=api.GetSearch(search_string, count=200)

        return [{"text":status.text,"label":None} for status in tweets_fetched]
    
    except:
        return "Sorry, an error occured."

search_string=input("Hi there! What are we searching for today?")
testData=createTestData(search_string)
    
    
def createTrainingCorpusNiek(corpusFile, stanCorpus):
    import csv
    trainingData=[]
    nCount = 0
    with open(corpusFile,'rb') as csvfile:
        lineReader = csv.reader(csvfile,delimiter=',',quotechar="\"")
        for row in lineReader:
            if row[1]=='positive' or row[1]=='negative':
                if row[1]=='neutral' and nCount < 300:
                    nCount += 1
                    trainingData.append({"tweet_id":row[2],"text":row[4],"label":row[1],"topic":row[0]})
                elif row[1]!='neutral':
                    trainingData.append({"tweet_id":row[2],"text":row[4],"label":row[1],"topic":row[0]})
    '''
    with open(stanCorpus,'rb') as csvfile:
        lineReader = csv.reader(csvfile,delimiter=',',quotechar="\"")
        for row in lineReader:
            #stanford uses numbers as labels
            stanLabel = row[0]
            if (stanLabel == 0):
                stanLabel = 'negative'
            elif (stanLabel == 2):
                stanLabel = 'neutral'
            else:
                stanLabel = 'positive'
            trainingData.append({"tweet_id":row[1],"text":row[5],"label":stanLabel,"topic":'none'})'''
    return trainingData





niekCorpusFile="full-corpus.csv"
stanCorpus = "training.1600000.processed.noemoticon.csv"
trainingData=createTrainingCorpusNiek(niekCorpusFile, stanCorpus)


import re
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords 


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
        try:
            tweet = tweet.decode('latin1', 'ignore')
        except UnicodeEncodeError:
            tweet = tweet
        print type(tweet)
        tweet=word_tokenize(tweet)
        # This tokenizes the tweet into a list of words 
        # Let's now return this list minus any stopwords 
        return [word for word in tweet if word not in self._stopwords]
    
tweetProcessor=PreProcessTweets()
ppTrainingData=tweetProcessor.processTweets(trainingData)
ppTestData=tweetProcessor.processTweets(testData)


import nltk 
 
def buildVocabulary(ppTrainingData):
    all_words=[]
    for (words,sentiment) in ppTrainingData:
        all_words.extend(words)
    # This will give us a list in which all the words in all the tweets are present
    
    wordlist=nltk.FreqDist(all_words)
    # This will create a dictionary with each word and its frequency
    word_features=wordlist.keys()
    # This will return the unique list of words in the corpus 
    
    f = open('word_features.pickle', 'wb')
    pickle.dump(word_features, f)
    f.close()
    print "Pickle Updated."
    return word_features

# NLTK has an apply_features function that takes in a user-defined function to extract features 
# from training data. We want to define our extract features function to take each tweet in 
# The training data and represent it with the presence or absence of a word in the vocabulary 

def extract_features(tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features['contains(%s)' % word]=(word in tweet_words)
        # This will give us a dictionary , with keys like 'contains word1' and 'contains word2'
        # and values as True or False 
    return features 

# Now we can extract the features and train the classifier 
word_features = buildVocabulary(ppTrainingData)
trainingFeatures=nltk.classify.apply_features(extract_features,ppTrainingData)
# apply_features will take the extract_features function we defined above, and apply it it 
# each element of ppTrainingData. It automatically identifies that each of those elements 
# is actually a tuple , so it takes the first element of the tuple to be the text and 
# second element to be the label, and applies the function only on the text 
print "Processing..."
NBayesClassifier=nltk.NaiveBayesClassifier.train(trainingFeatures)
print NBayesClassifier
print "Done"



f = open('my_classifier.pickle', 'wb')
pickle.dump(NBayesClassifier, f)
f.close()
print "Pickle Updated."
# We now have a classifier that has been trained using Naive Bayes

NBResultLabels=[NBayesClassifier.classify(extract_features(tweet[0])) for tweet in ppTestData]
print testData[0:10]
print NBResultLabels[0:10]


if NBResultLabels.count('positive')>NBResultLabels.count('negative'):
    print "NB Result Positive Sentiment" + str(100*NBResultLabels.count('positive')/len(NBResultLabels))+"%"
else: 
    print "NB Result Negative Sentiment" + str(100*NBResultLabels.count('negative')/len(NBResultLabels))+"%"
    
    
    
    
    
    

