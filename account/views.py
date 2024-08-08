from django.utils.timezone import now, timedelta
import random
from django.conf import settings
from django.shortcuts import render
from rest_framework import status, generics,permissions
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView 
from rest_framework.response import Response
from .serializers import RegistrSerializer,LoginSerializer,UserUpdateSerializer,LogoutSerializer,ResetRequestSetNewPasswordSerializer,ChangePasswordSerializer,EmailVerificationSerializer,UserSerializer
from .models import User,OneTimePassword
from rest_framework.permissions import IsAuthenticated
from .utils import send_generated_otp_to_email
from django.core.mail import EmailMessage

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RegisterView(generics.GenericAPIView):
    serializer_class = RegistrSerializer

    def post(self, request, *args, **kwargs):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            if not User.objects.filter(email = user_data['email']).exists():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Your account registered successfully'
                }, status=status.HTTP_201_CREATED)
            else: 
                return Response({
                    'data': serializer.data,
                    'message': 'account with this email already exist'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
        
class LogoutApiView(GenericAPIView):
    serializer_class=LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PasswordResetRequestView(APIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Check if a recent password reset request exists
            if user.last_password_reset_request is not None and now() - user.last_password_reset_request < timedelta(minutes=1):
                return Response({"error": "Please wait 1 minute before attempting another password reset."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Generate OTP and send email
            otp = random.randint(100000, 999999)
            OneTimePassword.objects.update_or_create(user=user, defaults={'otp': otp})

            # Sending email
            subject = "One time passcode for Password Reset"
            email_body = f"Hi {user.email}, use this OTP to reset your password: {otp}"
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]
            email = EmailMessage(subject, email_body, from_email, to_email)
            email.send()

            # Update last password reset request time
            user.last_password_reset_request = now()
            user.save()

            return Response({"message": "OTP sent to your email for password reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with that email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class ResetRequestSetNewPasswordView(APIView):
    serializer_class = ResetRequestSetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        otp_record = OneTimePassword.objects.filter(otp=otp).first()

        if not otp_record or otp_record.user.last_login > otp_record.created_at:
            return Response({"error": "Invalid OTP or OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = otp_record.user
        user.set_password(new_password)
        user.save()

        otp_record.delete()  # Delete OTP record after successful password reset

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        user = request.user

        if not user.check_password(old_password):
            return Response({"old_password": "Old password is not correct."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            user.delete()
            return Response({"detail": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)