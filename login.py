from httplib2 import Authentication
from user import User, twitter_request
from database import Database, creds
from twitter_utils import get_access_token, get_oauth_verifier, get_request_token

#class initialization
Database.initialise(database=creds['db'],user=creds['user'],password=creds['passwd'])

#check if user exists
screen_name  = input('Enter your username:')

user = User.load_from_db_by_screen_name(screen_name)

if not user:

    #get request token and parse the returned query string   
    request_token = get_request_token()
    
    #Ask user to authorise our app by providing pin and set it as the verifier
    oauth_verifier = get_oauth_verifier(request_token)

    #Ask Twitter for access token and twitter would return it as we have the verified request token
    access_token = get_access_token(request_token,oauth_verifier)

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=cats+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])



