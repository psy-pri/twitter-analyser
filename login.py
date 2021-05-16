import re
import constants
import oauth2
import urllib.parse as urlparse


consumer = oauth2.Consumer(constants.CONSUMER_KEY,constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

response, content = client.request(constants.REQUEST_TOKEN_URL,'POST')
if response.status != 200:
    print('Error fetching request token from Twitter')
    
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
print(request_token)

print('Go to the following site in your browser:')
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL,request_token['oauth_token']))

oauth_verifier = input('what is the pin code:')

token = oauth2.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth2.Client(consumer,token)

response, content =  client.request(constants.AUTHORIZATION_URL,'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
print(access_token)
