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