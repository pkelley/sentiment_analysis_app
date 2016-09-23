from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import SentAnalysis

def twit_sent(request):
    return render(request, 'twitsent/twit_sent.html')

def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        html = SentAnalysis.createTestData(search_id)
        return HttpResponse(html)
    else:
        return render(request, 'twitsent/twit_sent.html')