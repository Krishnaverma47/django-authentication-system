from django.urls import path
from accounts.views import UserCreateListAPIView, VerifyEmail, ResendVerificationEmail, UserLoginAPIView, GetAccessToken, UpdatePasswordAPIView

urlpatterns = [
    path('registration/', UserCreateListAPIView.as_view(), name='user_registration'),
    path('users-list/', UserCreateListAPIView.as_view(), name='user_list'),
    path('verify-email/<token>/', VerifyEmail.as_view(), name='verify_email'),
    path('resend-verification-email/', ResendVerificationEmail.as_view(), name='resend_verification_email'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('get-access-token/', GetAccessToken.as_view(), name='get_access_token'),
    path('update-password/', UpdatePasswordAPIView.as_view(), name='update_password'),

]