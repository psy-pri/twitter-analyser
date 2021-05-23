from database import CursorFromConnectionFromPool
import oauth2
import json
import constants
from twitter_utils import consumer

class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User details: {} {} {}>".format(self.screen_name)

    def save_to_db(self):
        #establish db connection
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO public.twitter_users (screen_name,oauth_token,oauth_token_secret) VALUES (%s,%s,%s)',
                        (self.screen_name,self.oauth_token,self.oauth_token_secret))

    @classmethod
    def load_from_db_by_screen_name(cls,screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM public.twitter_users where screen_name = %s',(screen_name,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(screen_name = user_data[1], 
                    oauth_token = user_data[2], 
                    oauth_token_secret = user_data [3], 
                    id = user_data[0])

    def twitter_request(self,uri,method = 'GET'):
        
        self.uri = uri,
        self.method = method
        #get auth token
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer,authorized_token)

        #Make Twitter calls!
        response, content = authorized_client.request(self.uri,self.method)
        if response.status != 200:
            print("Error occured while searching")
        return json.loads(content.encode('utf-8'))