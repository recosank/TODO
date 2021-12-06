from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import custom_user
from .serializers import SetNewPasswordSerializer,google_serializer, passwd_rlink_serializer, user_serializer,ChangePasswordSerializer #,MyTokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.viewsets import ReadOnlyModelViewSet,ViewSet,ModelViewSet
#from rest_framework.mixins import ListModelMixin,CreateModelMixin
#from rest_framework_simplejwt.tokens import RefreshToken     
#from rest_framework_simplejwt.authentication import JWTAuthentication
#from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import jwt
from django.http import HttpResponsePermanentRedirect
import os
from django.utils.encoding import smart_bytes,smart_str,force_str,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .token import get_tokens_for_user

#class CustomRedirect(HttpResponsePermanentRedirect):
#
#    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']
#

 


class GoogleSocialAuthView(APIView):

    serializer_class = google_serializer
    permission_classes = (AllowAny,)
    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data)
        
class signup(APIView):
    permission_classes=(AllowAny,)
    def post(self,req,*args, **kwargs):
        sr = user_serializer(data=req.data)
        if sr.is_valid():
            sr.save()
            user_data = sr.data
            user = custom_user.objects.filter(email=user_data['email']).last()
            #token = MyTokenObtainPairSerializer().get_token(user).access_token
            token = get_tokens_for_user(user)
            print(token)
            current_site = get_current_site(req).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token['access'])
            email_body = 'eyy '+user.username + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data)
            return Response(
            {'data': sr.data},
            
        )

        return Response(
            {'data': sr.errors},status=status.HTTP_417_EXPECTATION_FAILED
        )


class VerifyEmail(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        token = request.GET.get('token')
        print("verify token" + token)
        try:
            payload = jwt.decode(token, 'django-insecure-l!&=((8-$rh9!fjk1@_y(ud!w)g@cj^##@mt20trute#gv@&a+', algorithms=["HS256"])
            print(payload)
            user = custom_user.objects.get(id=payload['user_id'])
            print(user)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'})
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'})
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'})

class lgin(APIView):

    permission_classes=(AllowAny,)
    
    def post(self,req,*args, **kwargs):
        print('loginstart')
        data=req.data
        re = Response()
        user = authenticate(req,username = data['username'],password = data['password'])
        if user and not user.is_verified:
            return Response({
                "email":"email not verified"
            })
        if user is not None:
            data = get_tokens_for_user(user)
            print('userlogin')
            
    
            
            
            login(req,user)
       
            return Response(
            {'data': data},
   
        )
        raise ValidationError('not auth')


       
class lgout(APIView):
    def get(self,req,*args, **kwargs):
        
        logout(req)

        return Response({'msg':"User Logged out successfully"})

class passwd_resetlink(APIView):
    permission_classes=(AllowAny,)
    serializer_class = passwd_rlink_serializer
    
    def post(self,req,*args, **kwargs):
        sr = self.serializer_class(data=req.data)
        if sr.is_valid():
            return Response({'success': True, 'message': 'Password reset link sent'})
  

class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes=(AllowAny,)
    #serializer_class = SetNewPasswordSerializer

    def get(self, request, uid, token):
        print('here')
        #redirect_url = request.GET.get('redirect_url')
        #print(redirect_url)

        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = custom_user.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': False, 'message': 'Password cant be reset'})
  
                #if len(redirect_url) > 3:
                #
                #    return CustomRedirect(redirect_url+'?token_valid=False')
                #else:
                #    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            #if redirect_url and len(redirect_url) > 3:
            #    return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uid+'&token='+token)
            return Response({'success': True,'uuid':uid,'token':token ,'message': 'password reset token verified'})
  
            #else:
            #    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'})

            #try:
            #    if not PasswordResetTokenGenerator().check_token(user):
            #        return CustomRedirect(redirect_url+'?token_valid=False')
            #        
            #except UnboundLocalError as e:
            #    return Response({'error': 'Token is not valid, please request a new one'})

class SetNewPasswordAPIView(APIView):
    permission_classes=(AllowAny,)
    #serializer_class = 
    
    
    
    def patch(self, request,*args, **kwargs):
        print('strt rest')
        
        sr = SetNewPasswordSerializer(data=request.data)
        
        
        if sr.is_valid():
            uid = sr.data.get('uid')
        #print(uid)
        #id = force_str(urlsafe_base64_decode(uid))
        #usr = custom_user.objects.get(id=id)
        #password = serializer.data.get('password')
        #usr.set_password(password)
        #usr.save()
            return Response({'success': True, 'message': 'Password reset success'})

        return Response(sr.errors)
class ChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = ChangePasswordSerializer
    model = custom_user
    

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]})
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
              
                'message': 'Password updated successfully',
                
            }

            return Response(response)

        return Response("chk your new password again",status=status.HTTP_406_NOT_ACCEPTABLE)

