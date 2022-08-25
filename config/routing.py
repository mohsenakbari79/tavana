from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Websocket import routing as manager_routing
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
# from rest_framework_simplejwt.state import User
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from jwt import decode as jwt_decode
from django.conf import settings

@database_sync_to_async
def get_user(validated_token):
    print("get user token")
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        print(f"{user}")
        return user
        
    except Exception as e:
        print("\nERROR :",e)
        return AnonymousUser()
    # except User.DoesNotExist:
    #     return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        print(scope, receive, send)

        headers = dict(scope['headers'])
        token_key=None
        try:
            if b'authorization' in headers:
                token_name ,token_key = headers[b'authorization'].decode("utf8").split(" ")
            elif b'token' in scope['query_string']:
                for token in scope['query_string'].decode("utf8").split('&'):
                    if 'token' in token:
                        token_key = token.split('=')[1]

        except ValueError:
            token_key = None

        if token_key is None:
            return AnonymousUser()
        try:
            UntypedToken(token_key)
            decoded_data = jwt_decode(token_key, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            print(e)
            return AnonymousUser()


            
            
        print(decoded_data)


        scope['user'] =  await get_user(decoded_data)
        try:
            # print(scope, receive, send)
            respons=await super().__call__(scope, receive, send)
        except Exception as e:
            print("EXVEPTI NJSn",e)
        print("\n\n\n\n ",respons)
        return respons


