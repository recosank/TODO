
#from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken     
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
         

        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def get_tokens_for_user(user):
    #refresh = RefreshToken.for_user(user)
    refresh = MyTokenObtainPairSerializer().get_token(user)
    print(refresh)  
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

