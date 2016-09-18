from django.shortcuts import render

def twit_sent(request):
    return render(request, 'twitsent/twit_sent.html')