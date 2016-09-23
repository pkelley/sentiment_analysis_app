import twitter

api = twitter.Api(consumer_key='Fv3oNDnwH4BVAwMYryuKRqw6M',
                 consumer_secret='u2zhyNMsdftvZWVEZT94IbbgiH7t2YjFEjwPBopAmAwCs71yly',
                 access_token_key='518114279-N2vnFR7bawf45RsLjDSMaUmwtHwr0viwU1RH1LQ6',
                 access_token_secret='lMh2yShTVFLTZVit3jSRMAdLoN1fWN3NvBKrUHSuAf7NZ')
#print api.VerifyCredentials()

def createTestData(search_string):
    try:
        tweets_fetched=api.GetSearch(search_string, count=100)

        return ["<p>Tweet:" + status.text + "\n</p>" for status in tweets_fetched]#[{"text":status.text, "label":None} for status in tweets_fetched] #"Great! We fetched " + str(len(tweets_fetched)) + " tweets with the term "+ search_string+"!"
    except:
        return "Sorry, an error occured."

