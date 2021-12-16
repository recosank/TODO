from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import custom_user
from .serializers import SetNewPasswordSerializer,google_serializer, passwd_rlink_serializer, user_serializer,ChangePasswordSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics,status
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import jwt
from django.utils.encoding import smart_bytes,smart_str,force_str,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .token import get_tokens_for_user

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
            user = custom_user.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {'email': 'Successfully activated'}
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {'error': 'Activation Expired'}
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {'error': 'Invalid token'}
            )

class lgin(APIView):
    permission_classes=(AllowAny,)
    
    def post(self,req,*args, **kwargs):
        print('loginstart')
        data=req.data
        re = Response()
        user = authenticate(req,username = data['username'],password = data['password'])
        if user and not user.is_verified:
            return Response(
                {"email":"email not verified"}
            )
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
        return Response(
            {'msg':"User Logged out successfully"}
        )

class passwd_resetlink(APIView):
    permission_classes=(AllowAny,)
    serializer_class = passwd_rlink_serializer
    
    def post(self,req,*args, **kwargs):
        sr = self.serializer_class(data=req.data)
        if sr.is_valid():
            return Response(
                {'success': True, 'message': 'Password reset link sent'}
            )
  
class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes=(AllowAny,)
    
    def get(self, request, uid, token):
        print('here')
        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = custom_user.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'success': False, 'message': 'Password cant be reset'}
                )
            return Response(
                {'success': True,'uuid':uid,'token':token ,'message': 'password reset token verified'}
            )
        except DjangoUnicodeDecodeError as identifier:
            return Response(
                {'error': 'Token is not valid, please request a new one'}
            )

class SetNewPasswordAPIView(APIView):
    permission_classes=(AllowAny,)
   
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
            return Response(
                {'success': True, 'message': 'Password reset success'}
            )
        return Response(sr.errors)

class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    model = custom_user

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        sr = self.serializer_class(data=request.data,context={'request': request})
        print("hey im here")
        if sr.is_valid(raise_exception=True):
            #if not self.object.check_password(serializer.data.get("old_password")):
            #    return Response(
            #        {"message": "Wrong old password."}
            #    )
            #
            #self.object.set_password(serializer.data.get("new_password"))
            #self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
            }
            return Response(response)
        
        return Response(
            {"message":"chk your new password again"},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )

