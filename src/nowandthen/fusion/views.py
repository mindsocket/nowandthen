#from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

def about(request):
    """Vanilla "about" page"""
    return render_to_response('about.html', context_instance=RequestContext(request))
    
