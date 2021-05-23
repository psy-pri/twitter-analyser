from database import Database,creds
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from twitter_utils import get_request_token,get_access_token,get_oauth_verifier,get_oauth_verifier_url
from user import User

#class initialization
Database.initialise(database=creds['db'],user=creds['user'],password=creds['passwd'])

# Create your views here.
def login(request):
    request_token = get_request_token()
    request.session['request_token'] = request_token
    
    return redirect(get_oauth_verifier_url(request_token))

def auth(request):
    oauth_verifier = request.GET.getlist('oauth_verifier')
    access_token = get_access_token(request.session['request_token'], oauth_verifier)
    
    #check user exists
    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    
    if not user:
        #save new user to db
        user = User(screen_name = access_token['screen_name'], 
                oauth_token = access_token['oauth_token'], 
                oauth_token_secret = access_token['oauth_token_secret'],
                id = None)
    user.save_to_db()
    
    request.session['screen_name'] = user.screen_name
    return redirect('/profile')

def profile(request):
    screen_name = request.session['screen_name']
    return render(request,'profile.html',{'screen_name':screen_name})