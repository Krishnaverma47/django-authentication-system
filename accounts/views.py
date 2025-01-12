from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import os

from accounts.email import SendEmail
from accounts.models import User
from accounts.serializer import GetRefreshTokenSerializer, UpdatePasswordSerializer, UserSerializer, UserLoginSerializer
from accounts.utils import format_response, generate_token, verify_token


class UserCreateListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer_class = UserSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            user_data = serializer.data
            user_id = user_data.get('id')
            token = generate_token(user_id)
            verification_link = f"http://localhost:8000/accounts/verify-email/?token={token}"
            subject = "🎉 Welcome to App Authenticator Byte! 🎉"
            context = {
                'user': user_data['username'],
                'verification_link': verification_link,
                'subject': subject
            }
            from_email = os.environ.get('EMAIL_HOST_USER')
            recipient_list = [user_data['email']]
            SendEmail.delay(subject, "user_registration.html", context, from_email, recipient_list)

            return format_response(
                message = "User has been created successfully. please verify your email.",
                data = user_data,
                status_code = status.HTTP_201_CREATED
            )
        except Exception as e:
            print(f"Getting error while creating user: {str(e)}")
            return format_response(
                message = "An error occurred while creating user.",
                error = str(e),
                status_code = status.HTTP_400_BAD_REQUEST
            )
    

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                data = serializer.data
                data['fullname'] = user.get_full_name()
                return format_response(
                    message = "User has been fetched successfully.",
                    data = data,
                    status_code = status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return format_response(
                    message = "User with this id not found.",
                    error = "User with this id not found.",
                    status_code = status.HTTP_400_BAD_REQUEST
                )
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            data = serializer.data
            for user, user_data in zip(users, data):
                user_data['fullname'] = user.get_full_name()
            return format_response(
                message = "Users list has been fetched successfully.",
                data = data,
                status_code = status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Getting error while fetching users list: {str(e)}")
            return format_response(
                message = "An error occurred while fetching users list.",
                error = str(e),
                status_code = status.HTTP_400_BAD_REQUEST
            )

class VerifyEmail(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            data = verify_token(token)
            if data is None:
                return format_response(
                    message = "Token is invalid or expired.",
                    error = "Token is invalid or expired.",
                    status_code = status.HTTP_400_BAD_REQUEST
                )
            print("Decoded data : ", data)
            user = User.objects.get(id=data['user_id'])
            if user.is_active:
                return format_response(
                    message = "This user account has been already verified.",
                    error = "This user account has been already verified.",
                    status_code = status.HTTP_200_OK
                )
            user.is_active = True
            user.save()
            return format_response(
                message = "User account has been verified successfully.",
                status_code = status.HTTP_200_OK
            )
        except User.DoesNotExist:
            raise ValidationError("User with this email not found.")
        except Exception as e:
            print(f"Getting error while verifying user. {str(e)}")
            raise ValidationError("An error occurred while verifying user.")
        
class ResendVerificationEmail(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return format_response(
                    message = "This user account has been already verified.",
                    error = "This user account has been already verified.",
                    status_code = status.HTTP_200_OK
                )
            token = generate_token(user.id)
            verification_link = f"http://localhost:8000/accounts/verify-email/?token={token}"
            subject = "🎉 Welcome to App Authenticator Byte! 🎉"
            context = {
                'user': user.username,
                'verification_link': verification_link,
                'subject': subject
            }
            from_email = os.environ.get('EMAIL_HOST_USER')
            recipient_list = [email]
            SendEmail.delay(subject, "user_registration.html", context, from_email, recipient_list)
            return format_response(
                message = "Verification email has been sent successfully. please check your email.",
                status_code = status.HTTP_200_OK
            )
        except User.DoesNotExist:
            raise ValidationError("User with this email not found.")
        except Exception as e:
            print(f"Getting error while sending verification email. {str(e)}")
            raise ValidationError("An error occurred while sending verification email.")
        
class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = serializer.validated_data.get('email')
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            return format_response(
                message = "User has been logged in successfully.",
                data = {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
                status_code = status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Getting error while login user. {str(e)}")
            raise ValidationError("An error occurred while login user.")
        
class GetAccessToken(APIView):
    def post(self, request, *args, **kwargs):

        serializer = GetRefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh = RefreshToken(serializer.validated_data.get('refresh_token'))
            return format_response(
                message = "Access token has been fetched successfully.",
                data = {
                    "access_token": str(refresh.access_token),
                },
                status_code = status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Getting error while fetching access token. {str(e)}")
            return format_response(
                message = "An error occurred while fetching access token.",
                error = "Token is invalid or expired.",
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
class UpdatePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer  = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        try:
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            if not user.check_password(old_password):
                return format_response(
                    message = "Plesae provide correct old password.",
                    error = "Please provide correct old password.",
                    status_code = status.HTTP_400_BAD_REQUEST
                )
            user.set_password(new_password)
            user.save()
            return format_response(
                message = "Password has been updated successfully.",
                status_code = status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Getting error while updating password. {str(e)}")
            return format_response(
                message = "An error occurred while updating password.",
                error = str(e),
                status_code = status.HTTP_400_BAD_REQUEST
            )

