from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ChangePasswordView, GoogleSocialAuthView,VerifyEmail,PasswordTokenCheckAPI, SetNewPasswordAPIView, passwd_resetlink, signup,lgin,lgout
from rest_framework_simplejwt.views  import TokenRefreshView
from .token import MyTokenObtainPairView

urlpatterns = [
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('signup',signup.as_view(),name='signup'),
    path('login',lgin.as_view(),name='login'),
    path('logout',lgout.as_view(),name='logout'),
    path('token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('password-change',ChangePasswordView.as_view(),name='password-change'),
    path('password-reset-link',passwd_resetlink.as_view(),name='password-reset-link'),
    path('password-reset-link-ck/<uid>/<token>',PasswordTokenCheckAPI.as_view(),name='password-reset-link-ck'),
    path('password-reset-complete',SetNewPasswordAPIView.as_view(),name='password-rese-complete'),
    path('s-login',GoogleSocialAuthView.as_view(),name='s-login')


]
