from categories.models import Category
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from rooms.models import Room, Amenity
from rooms.serializers import (
    AmenitySerializer,
    RoomDetailSerializer,
    RoomListSerializer,
)
from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.conf import settings


class Amenities(APIView):
    serializer_class = AmenitySerializer

    def get_object(self):
        try:
            return Amenity.objects.all()
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request):
        all_amenities = self.get_object()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(
                AmenitySerializer(new_amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    serializer_class = AmenitySerializer

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = AmenitySerializer(self.get_object(pk=pk))
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = AmenitySerializer(
            instance=self.get_object(pk=pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            fixed = serializer.save()
            return Response(AmenitySerializer(fixed).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk=pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomCommon:
    def category_validate(self, request):
        category_pk = request.data.get("category")
        if not category_pk:
            raise ParseError("Category is required")
        try:
            category = Category.objects.get(pk=category_pk)
            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("Category not found")
            return category
        except Category.DoesNotExist:
            raise ParseError(f"Category not found")

    def amenities_validate(self, request):
        amenities_valid = []
        amenities = request.data.get("amenities")
        for amenity_pk in amenities:
            try:
                amenity = Amenity.objects.get(pk=amenity_pk)
            except Amenity.DoesNotExist:
                # if amenity does not exist
                pass

            amenities_valid.append(amenity)
        return amenities_valid


class Rooms(APIView, RoomCommon):

    serializer_class = RoomDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomListSerializer(
            rooms,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category = self.category_validate(request)
            room = serializer.save(
                owner=request.user,
                category=category,
            )
            amenities = self.amenities_validate(request)
            for amenity in amenities:
                room.amenities.add(amenity)

            serializer = RoomDetailSerializer(room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomDetail(APIView, RoomCommon):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = Room.objects.get(pk=pk)
        if room.owner != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            if "category" in request.data:
                category = self.category_validate(request)
                room = serializer.save(category=category)

            if "amenities" in request.data:
                room.amenities.clear()
                amenities = self.amenities_validate(request)
                for amenity in amenities:
                    room.amenities.add(amenity)

            room = serializer.save()
            serializer = RoomDetailSerializer(room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk=pk)
        if room.owner != request.user:
            return PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        try:
            request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page = int(page)
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        reviews = room.reviews.all()[start:end]
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk=pk)
        if room.owner != request.user:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
