from httplib2 import Authentication
import constants
from constants import consumer
import oauth2
from user import User
from user import twitter_request
from database import Database
from database import creds
from twitter_utils import consumer, get_request_token

#class initialization
Database.initialise(database=creds['db'],user=creds['user'],password=creds['passwd'])

#check if user exists
email  = input('Enter your email:')

user = User.load_from_db_by_email(email)

if not user:

    #get request token and parse the returned query string   
    request_token = get_request_token()
    
    #Ask user to authorise our app by providing pin and set it as the verifier
    print('Go to the following site in your browser:')
    print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL,request_token['oauth_token']))

    oauth_verifier = input('what is the pin code:')

    #Create a token object that contains the request token and verifier 
    token = oauth2.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    #Create client with our consumer(app) and verified token obj 
    client = oauth2.Client(consumer,token)

    #Ask Twitter for access token and twitter would return it as we have the verified request token
    response, content =  client.request(constants.ACCESS_TOKEN_URL,'POST')
    access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    print(access_token)

    first_name = input('Enter your First Name:')
    last_name = input('Enter your Last Name:')
    
    #save new user to db
    user = User(email = email, 
                first_name = first_name, 
                last_name = last_name, 
                oauth_token = access_token['oauth_token'], 
                oauth_token_secret = access_token['oauth_token_secret'],
                id = None)
    
    user.save_to_db()

# #Create an 'authorized_token' to perform Twitter API calls on behalf of user 
authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
authorized_client = oauth2.Client(consumer,authorized_token)

#Make Twitter calls!
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=cats+filter:images','GET')
if response.status != 200:
    print("Error occured while searching")
print(content.decode('utf-8'))  

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=cats+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])



