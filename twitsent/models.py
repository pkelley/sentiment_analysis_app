from __future__ import unicode_literals

from django.db import models

class RecentTweets(models.Model): 
    tweet = models.CharField(max_length=500)
    sentiment = models.CharField(max_length=20)
    topic = models.CharField(max_length=30)
    '''def getTweet(self):
        return self.tweet
    def getSent(self):
        return self.sentiment'''
    
class SentPercent(models.Model): 
    topic = models.CharField(max_length=30)
    sent_perc = models.CharField(max_length=50)
    
    
    
    
