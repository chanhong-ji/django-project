from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import User
import users.serializers as UserSerializers
from django.contrib.auth import logout, login, authenticate


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

    def post(self, request):
        serializer = UserSerializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                email=serializer.data.get("email"),
                password=serializer.data.get("password"),
            )
            if user:
                login(request, user)
                return Response({"message": "welcome"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
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
