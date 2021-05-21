from database import CursorFromConnectionFromPool
import oauth2
import json
from constants import consumer
import constants


class User:
    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User details: {} {} {}>".format(self.email,self.first_name,self.last_name)

    def save_to_db(self):
        #establish db connection
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO public.twitter_users (email,first_name,last_name,oauth_token,oauth_token_secret) VALUES (%s,%s,%s,%s,%s)',
                        (self.email,self.first_name,self.last_name,self.oauth_token,self.oauth_token_secret))

    @classmethod
    def load_from_db_by_email(cls,email):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM public.twitter_users where email = %s',(email,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(email = user_data[1], 
                    first_name = user_data[2], 
                    last_name = user_data[3], 
                    oauth_token = user_data[4], 
                    oauth_token_secret = user_data [5], 
                    id = user_data[0])

    def twitter_request(self,uri,method = 'GET'):
        
        self.uri = uri,
        self.method = method
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer,authorized_token)

        #Make Twitter calls!
        response, content = authorized_client.request(self.uri,self.method)
        if response.status != 200:
            print("Error occured while searching")
        return json.loads(content.encode('utf-8'))

    def get_request_token(self):
        
        client = oauth2.Client(consumer)
        #Use consumer object to request for request token
        response, content = client.request(constants.REQUEST_TOKEN_URL,'POST')
        if response.status != 200:
            print('Error fetching request token from Twitter')

        #get request token and parse the returned query string   
        return dict(urlparse.parse_qsl(content.decode('utf-8')))
        