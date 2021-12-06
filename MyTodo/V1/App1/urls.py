from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ChangePasswordView, GoogleSocialAuthView,VerifyEmail,PasswordTokenCheckAPI, SetNewPasswordAPIView, passwd_resetlink, signup,lgin,lgout #,MyTokenObtainPairView,VerifyEmail
from rest_framework_simplejwt.views  import TokenRefreshView,TokenObtainPairView
from .token import MyTokenObtainPairView

urlpatterns = [
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('signup',signup.as_view(),name='signup'),
    path('login',lgin.as_view(),name='login'),
    path('logout',lgout.as_view(),name='logout'),
    path('token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('password-change',ChangePasswordView.as_view(),name='password-change'),
    #path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password-reset-link',passwd_resetlink.as_view(),name='password-reset-link'),
    path('password-reset-link-ck/<uid>/<token>',PasswordTokenCheckAPI.as_view(),name='password-reset-link-ck'),
    path('password-reset-complete',SetNewPasswordAPIView.as_view(),name='password-rese-complete'),
    path('s-login',GoogleSocialAuthView.as_view(),name='s-login')


]
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4MzgzNzI3LCJpYXQiOjE2MzgzODM0MjcsImp0aSI6IjZhNDg1NThiZDE3ZTRjMjU4MTQzNGIwNzE1MWExY2Y3IiwidXNlcl9pZCI6MTMsIm5hbWUiOiJub2ZvdW5kIn0.jL1UzIbkyPNKArrD7_OMhtjAYKbZeipYa7pYInSkqvQ
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzODQ2OTgyNywiaWF0IjoxNjM4MzgzNDI3LCJqdGkiOiJjNDlkN2IyYmU3ZGU0Y2Q5ODc5YjFkMjJiOTAwZTVjZSIsInVzZXJfaWQiOjEzLCJuYW1lIjoibm9mb3VuZCJ9.SsY_cDSqxQkFekGWB0mD6Fm-CiOY7l1pksqVpXjLzJg