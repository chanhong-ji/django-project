from datetime import timedelta
from django.utils.dateparse import parse_date
from django.conf import settings
from django.utils import timezone
from bookings.models import Booking
from medias.models import Photo
from rooms.models import Room, Amenity
from categories.models import Category
from bookings.serializers import CreateRoomBookingSerializer, PublicBookingSerializer
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from rooms.serializers import (
    AmenitySerializer,
    RoomDetailSerializer,
    RoomListSerializer,
)
from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(
                AmenitySerializer(new_amenity).data,
                status=status.HTTP_201_CREATED,
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

    def put(self, request, pk):
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied

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

        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied

        self.get_object(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        amenities = request.data.get("amenities", [])
        for amenity_pk in amenities:
            try:
                amenity = Amenity.objects.get(pk=amenity_pk)
                amenities_valid.append(amenity)
            except Amenity.DoesNotExist:
                pass

        return amenities_valid

    def photos_validate(self, request):
        photos = request.data.get("photos", [])
        photos_valid = []
        for photo_pk in photos:
            try:
                photo = Photo.objects.get(pk=photo_pk)
                photos_valid.append(photo)
            except Photo.DoesNotExist:
                pass

        return photos_valid


# rooms/
class Rooms(APIView, RoomCommon):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RoomDetailSerializer

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
            photos = self.photos_validate(request)
            room = serializer.save(
                owner=request.user,
                category=category,
                photos=photos,
            )

            amenities = self.amenities_validate(request)
            for amenity in amenities:
                room.amenities.add(amenity)

            room.save()
            serializer = RoomDetailSerializer(room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# rooms/:int
class RoomDetail(APIView, RoomCommon):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RoomDetailSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = RoomDetailSerializer(room, context={"request": request})

        bookings = PublicBookingSerializer(room.bookings, many=True).data
        booked = []
        check_in_dates = []
        for booking in bookings:
            booking = dict(booking)
            check_in = booking.get("check_in")
            check_out = booking.get("check_out")

            check_in = parse_date(check_in)
            check_out = parse_date(check_out)
            days = check_out - check_in

            for i in range(days.days):
                day = check_in + timedelta(days=i)
                if i == 0:
                    check_in_dates.append(day)
                else:
                    booked.append(day)

        data = serializer.data
        data["booked"] = booked
        data["check_in_disable"] = check_in_dates
        return Response(data)

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
        return Response(status=status.HTTP_204_NO_CONTENT)


# rooms/:int/reviews?page={}
class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page = int(page)
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        reviews = room.reviews.all()[start:end]
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk=pk)
        if room.owner == request.user:
            raise PermissionDenied("Owner can't rate")

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=room)
            return Response(ReviewSerializer(review).data)
        else:
            return Response(serializer.errors)


# rooms/:pk/photos
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


# rooms/:int/bookings
class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CreateRoomBookingSerializer

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_room(pk)
        bookings = room.bookings.filter(
            room__pk=pk,
            check_out__gte=timezone.localdate(timezone.now()),
            kind=Booking.BookingKindChoices.ROOM,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_room(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )
        if serializer.is_valid():
            room = serializer.save(
                user=request.user,
                room=room,
                kind=Booking.BookingKindChoices.ROOM,
            )
            return Response(PublicBookingSerializer(room).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# rooms/:int/bookings/check?check_in={}&check_out={}
class RoomBookingCheck(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")
        if not check_in or not check_out:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        exist = Booking.objects.filter(
            room=room,
            check_out__gt=check_in,
            check_in__lt=check_out,
        ).exists()
        return Response(True if not exist else False)
