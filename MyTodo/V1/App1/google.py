from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

class Google:

    @staticmethod
    def validate(a_token):

        try:
            print('pp')
            idinfo = id_token.verify_oauth2_token(a_token,requests.Request())
            print(idinfo)
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            raise AuthenticationFailed( "The token is either invalid or has expired" )

