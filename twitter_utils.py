import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY,constants.CONSUMER_SECRET)

def get_request_token():
        
        client = oauth2.Client(consumer)
        #Use consumer object to request for request token
        response, content = client.request(constants.REQUEST_TOKEN_URL,'POST')
        if response.status != 200:
            print('Error fetching request token from Twitter')

        #get request token and parse the returned query string   
        return dict(urlparse.parse_qsl(content.decode('utf-8')))
    
def get_oauth_verifier(request_token):
    #Ask user to authorise our app by providing pin and set it as the verifier
    print('Go to the following site in your browser:')
    print(get_oauth_verifier_url(request_token))

    return input('what is the pin code:')   

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL,request_token['oauth_token'])

def get_access_token(request_token,oauth_verifier):
    #Create a token object that contains the request token and verifier 
    token = oauth2.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    #Create client with our consumer(app) and verified token obj 
    client = oauth2.Client(consumer,token)

    #Ask Twitter for access token and twitter would return it as we have the verified request token
    response, content =  client.request(constants.ACCESS_TOKEN_URL,'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))