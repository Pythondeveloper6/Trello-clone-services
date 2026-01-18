import logging

from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile , UserVerification
from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    UserProfileSerializer,
    UserRegisterationSerializer,
    UserSerializer,
)
from .tasks import send_verification_email
from utils.generate_unique_number import generate_verification_code

# create logger
logger = logging.getLogger(__name__)


class UserRegisterationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterationSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # send welcome email
            # send_welcome_email.delay({"email": user.email, "username": user.username})
            #
            # send verification email
            code = generate_verification_code()
            UserVerification.objects.create(user=user,code=code)
            send_verification_email.delay(user.id,code)

            # create jwt tokens for user
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            logger.info("User Logged in successfully")

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )

        logger.error(f"Login Failed - serializer error : {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get(self, request):
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile).data
            return Response(serializer)

        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            serializer = UserProfileSerializer(profile).data
            return Response(serializer)

    def put(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated Successfully", "profile": serializer.data}
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()

        # filter : email
        print(f"----> {self.request}")
        email = self.request.query_params.get("email")
        print(email)
        if email:
            queryset = queryset.filter(email__icontains=email)

        # filter : username
        username = self.request.query_params.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
            verification = user.verification
            print(verification)

            if verification.code == code :
                # save user as is_verified
                user.is_verified = True
                user.save()

                # cleanup verification code
                verification.delete()

                # return
                return Response({"message":"your account was verified successfully"})

            else:
                return Response({"error":"you code is invalid or expired"} , status=400)

        except User.DoesNotExist:
            return Response({"error":"this user does not exist"},status=400)

        except UserVerification.DoesNotExist:
            return Response({"error":"no verification found for this user"},status=400)

        except Exception as e:
            print(f"----> {e}")
            return Response({"error":"Error happend try again later "},status=400)
