from django.contrib.auth import authenticate
from django.urls.base import reverse
from rest_framework import serializers, settings
from .models import custom_user
from .utils import Util
from V1.App2.models import profile
from django.utils.encoding import smart_bytes,smart_str,force_str
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from .google import Google
from .socialuser import create_social_user


class user_serializer(serializers.ModelSerializer):
    
    #tokens = serializers.SerializerMethodField()

    class Meta:
        model = custom_user
        fields = ('username','password','email') #'tokens','email')
        
        extra_kwargs = {'password':{"write_only":True}}
    
    #def get_tokens(self,usr):
    #    
    #    refresh = MyTokenObtainPairSerializer().get_token(usr)
    #    return {
    #        'refresh': str(refresh),
    #        'access': str(refresh.access_token),
    #    }
    
    def create(self, validated_data):
        
        ins = self.Meta.model(**validated_data)
        print(ins)
        password = self.validated_data['password']
        if password is None:
            return serializers.ValidationError('psdnot found')
        ins.set_password(password)
        ins.save()
       
        profile.objects.create(user=ins)
        return ins


class login_Serializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    class Meta:
        model = custom_user
        fields = ('username','password','email')

    def validate(self,attrs):
        u_name = attrs.get("username")
        user = custom_user.objects.get(username=u_name)
        auth_u = authenticate(username=u_name,password = attrs['password'])
        if user.exists() & user[0].auth_provider != 'email':
            raise AuthenticationFailed('login by ' + user[0].auth_provider )
        if not auth_u:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

class passwd_rlink_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=132)

    class Meta:
        fields = ('username',)
    
    def validate(self, attrs):
        print('strt vs')
        username = attrs.get('username')
        print(username)
        if username is not None:
            user_obj = custom_user.objects.get(username=username)
            print(user_obj)
            if user_obj is not None:
                uid = urlsafe_base64_encode(smart_bytes(user_obj.id))
                p_token = PasswordResetTokenGenerator().make_token(user_obj)
                reverseurl = reverse('password-reset-link-ck',kwargs={'uid':uid,'token':p_token})
                absurl = 'http://127.0.0.1:8000'+reverseurl
                email_body = 'eyy '+username + ' Use the link below to verify your email \n' + absurl
                data = {'email_body': email_body, 'to_email': user_obj.email,
                    'email_subject': 'Verify your email'}
                Util.send_email(data)
        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    p_token = serializers.CharField(
        min_length=1, write_only=True)
    uid = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('p_token')
            uidb64 = attrs.get('uid')
            id = force_str(urlsafe_base64_decode(uidb64))
            usr = custom_user.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(usr, token):
                raise AuthenticationFailed('The reset link is invalid try agian with new link')

            usr.set_password(password)
            usr.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link iss invalid')
        return super().validate(attrs)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True,write_only=True)
    new_password = serializers.CharField(required=True,write_only=True)
    confirm_password = serializers.CharField(required=True,write_only=True)
    
    class Meta:
        model = custom_user
        fields = ("old_password","new_password","confirm_password") 
    
    def validate(self, attrs):
        usr = self.context['request'].user
        psswd = attrs.get("old_password")
        if not usr.check_password(psswd):
            raise serializers.ValidationError("chk old psswed")
            
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("chk new psswed")
        
        usr.set_password(attrs.get("new_password"))
        usr.save()
        return super().validate(attrs)

class google_serializer(serializers.Serializer):
    g_token = serializers.CharField(max_length=465)
    
    class Meta:
        fields =('g_token',)

    def validate_g_token(self,g_token):
        user_data = Google.validate(g_token)
        try:
            print(user_data)
            user_data['sub']
        except:
            raise serializers.ValidationError('invalid token no0 data')
        if user_data['aud'] != settings['GOOGLE_CLIENT_ID']:
            raise AuthenticationFailed('not recognized')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        return create_social_user(p=provider,u=name,u_id=user_id,e=email)
        