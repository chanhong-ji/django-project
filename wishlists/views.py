from experiences.models import Experience
from rooms.models import Room
from .models import Wishlist
from wishlists.serializers import WishlistSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            wishlists,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serializer.errors)


class WishlistCommon(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound("Wishlist not found")


class WishlistDetail(WishlistCommon):
    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            wishlist = serializer.save()
            return Response(WishlistSerializer(wishlist).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)


# wishlists/:pk/rooms/:room_pk
class WishlistRoomToggle(WishlistCommon):
    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound("Room not found")

    def put(self, request, pk, room_pk):
        room = self.get_room(room_pk)
        wishlist = self.get_object(pk, request.user)
        if wishlist.rooms.filter(pk=room_pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_200_OK)


# wishlists/:pk/experiences/:experience_pk
class WishlistExperienceToggle(WishlistCommon):
    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def put(self, request, pk, experience_pk):
        experience = self.get_experience(experience_pk)
        wishlists = self.get_object(pk, request.user)
        if wishlists.experiences.filter(pk=experience_pk).exists():
            wishlists.experiences.remove(experience)
        else:
            wishlists.experiences.add(experience)

        return Response(status=HTTP_200_OK)
