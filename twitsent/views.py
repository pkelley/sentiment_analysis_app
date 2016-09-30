from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import trainedNB
import sqlite3
from .models import RecentTweets, SentPercent
from django.template.loader import get_template
from django.template import Context

def twit_sent(request):
    return render(request, 'twitsent/twit_sent.html')
    
def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        trainedNB.createTestData(search_id)
        
        #get tweet and sentiment from database
        all_tweets = RecentTweets.objects.all()
        sent = SentPercent.objects.all()
        return render(request, 'twitsent/search.html'\
        ,{'all_tweets': all_tweets,
          'sent': sent
         })
    else:
        return render(request, 'twitsent/twit_sent.html')
    