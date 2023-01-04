import email
from pprint import pprint
from random import randint
from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.models import User
import users.serializers as UserSerializers
from django.contrib.auth import logout, login, authenticate
from config.variables import variables
import requests


# users/
# POST
class Users(APIView):

    serializer_class = UserSerializers.CreateUserSerializer

    def post(self, request):
        serializer = UserSerializers.CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get("password"))
            user.save()
            serializer = UserSerializers.PrivateUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors)


# users/me
# GET PUT
class Me(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializers.PrivateUserSerializer

    def get(self, request):
        serializer = UserSerializers.PrivateUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializers.PrivateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = UserSerializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# users/<str:username>
# GET
class UserDetail(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializers.PublicUserSerializer(user)
        return Response(serializer.data)


# users/change-password
# PUT
class ChangePassword(APIView):

    serializer_class = UserSerializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        old_password = request.data.get("old_password")
        user = request.user
        if not user.check_password(old_password):
            return Response("Password wrong", status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(request.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# users/login
# POST
class Login(APIView):

    serializer_class = UserSerializers.LoginSerializer

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound({"message": "User Doesn't exist"})

    def post(self, request):
        serializer = UserSerializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            self.get_object(request.data.get("username"))
            user = authenticate(
                request,
                username=serializer.data.get("username"),
                password=serializer.data.get("password"),
            )
            if user:
                login(request, user)
                return Response({"message": "welcome"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Password wrong"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# users/logout
# POST
class Logout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "bye"}, status=status.HTTP_202_ACCEPTED)


class CommonFn:
    def get_unique_username(self, username):
        key = username
        while True:
            if User.objects.filter(username=username).exists():
                username = key + str(randint(100000, 999999))
            else:
                return username


# users/github
# POST
class GithubLogin(APIView, CommonFn):
    def post(self, request):
        try:
            # Get token

            code = request.data.get("code")
            host = "https://github.com/login/oauth/access_token"
            data = requests.post(
                host,
                data={
                    "client_id": variables["github"]["client_id"],
                    "client_secret": variables["github"]["client_secret"],
                    "code": code,
                },
                headers={"Accept": "application/json"},
            ).json()

            # Get user information
            user_info = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {data.get('access_token')}",
                    "Accept": "application/json",
                },
            ).json()

            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {data.get('access_token')}",
                    "Accept": "application/json",
                },
            ).json()

            verified_email = [
                email for email in user_emails if email.get("verified") == True
            ][0]

            # Signup & Login

            try:
                # Login
                user = User.objects.get(email=verified_email.get("email"))
                if user.social == User.SocialChoices.GH:
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
                elif user.social == User.SocialChoices.KA:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={"message": "You already have an Kakao account"},
                    )
                else:
                    user.set_unusable_password()
                    user.social = User.SocialChoices.GH
                    user.save()
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)

            except User.DoesNotExist:
                # Sign up
                user = User.objects.create(
                    email=verified_email.get("email"),
                    username=self.get_unique_username(user_info.get("name")),
                    avatar=user_info.get("avatar_url"),
                    social=User.SocialChoices.GH,
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            pprint(e)
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"message": "unexpected error"}
            )


# users/kakao
# POST
class KakaoLogin(APIView, CommonFn):
    def post(self, request):
        try:
            # Get token

            code = request.data.get("code")
            data = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                params={
                    "client_id": variables["kakao"]["client_id"],
                    "client_secret": variables["kakao"]["client_secret"],
                    "redirect_uri": variables["kakao"]["redirect_url"],
                    "code": code,
                    "grant_type": "authorization_code",
                },
            ).json()

            # Get user information

            data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                    "Authorization": f"Bearer {data.get('access_token')}",
                },
            ).json()

            user_info = data.get("kakao_account")
            user_profile = user_info.get("profile")
            email = user_info.get("email")

            # Signup & Login

            try:
                # Login
                user = User.objects.get(email=email)
                if user.social == User.SocialChoices.KA:
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
                elif user.social == User.SocialChoices.GH:
                    return Response(
                        data={"message": "You already have an Github account"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    user.set_unusable_password()
                    user.social = User.SocialChoices.KA
                    user.save()
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)

            except User.DoesNotExist:
                # Sign up
                user = User.objects.create(
                    email=email,
                    username=self.get_unique_username(user_profile.get("nickname")),
                    gender=user_info.get("gender"),
                    avatar=user_profile.get("profile_image_url"),
                    social=User.SocialChoices.KA,
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            pprint(e)
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"message": "unexpected error"}
            )
