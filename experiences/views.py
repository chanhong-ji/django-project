from bookings.models import Booking
from bookings.serializers import (
    CreateExperienceBookingSerializer,
    PrivateBookingSerializer,
    PublicBookingSerializer,
)
from categories.models import Category
from experiences.models import Experience, Perk
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
import rest_framework.status as status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from experiences.serializers import (
    ExperienceDetailSerializer,
    ExperienceListSerializer,
    PerkSerializer,
)
from django.conf import settings
from medias.serializers import PhotoSerializer, VideoSerializer
from reviews.serializers import ReviewSerializer


class ValidationExperience:
    def validate_perk(self, request):
        validated = []
        for perk_pk in request.data.get("perks", []):
            try:
                got = Perk.objects.get(pk=perk_pk)
                validated.append(got)
            except Perk.DoesNotExist:
                pass
        return validated

    def validate_category(self, request):
        category_pk = request.data.get("category")
        if not category_pk:
            raise ParseError("Category is required")
        try:
            return Category.objects.get(
                pk=category_pk, kind=Category.CategoryKindChoices.EXPERIENCES
            )
        except Category.DoesNotExist:
            raise ParseError("Category not found")


class CommonExperience(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound


# experiences/
# GET POST
class Experiences(APIView, ValidationExperience):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(
            experiences,
            many=True,
            context={"user": request.user},
        )
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            # validate category
            category = self.validate_category(request)

            # create experience
            experience = serializer.save(host=request.user, category=category)

            # add perks
            perks = self.validate_perk(request)
            for perk in perks:
                experience.perks.add(perk)

            serializer = ExperienceDetailSerializer(
                experience, context={"user": request.user}
            )
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


# experiences/:pk
# GET PUT DELETE
class ExperienceDetail(CommonExperience, ValidationExperience):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={"user": request.user},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk=pk)

        if experience.host != request.user:
            raise PermissionDenied

        serializer = ExperienceDetailSerializer(
            instance=experience,
            data=request.data,
            partial=True,
            context={"user": request.user},
        )
        if serializer.is_valid():
            if request.data.get("category"):
                category = self.validate_category(request)
                updated = serializer.save(category=category)
            if request.data.get("perks"):
                experience.perks.clear()
                perks = self.validate_perk(request)
                for perk in perks:
                    experience.perks.add(perk)

            updated = serializer.save()
            serializer = ExperienceDetailSerializer(
                updated,
                context={"user": request.user},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk=pk)
        if experience.host != request.user:
            raise PermissionDenied

        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# experiences/:pk/photos
# POST
class ExperiencePhotos(CommonExperience):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# experiences/:pk/video
# POST
class ExperienceVideo(CommonExperience):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save(experience=experience)  # 자동으로 onebyone 되는게 아닌가??
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# experiences/:pk/perks
# GET
class ExperiencePerks(CommonExperience):
    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = PerkSerializer(experience.perks, many=True)
        return Response(serializer.data)


# experiences/:pk/bookings
# GET POST
class ExperienceBookings(CommonExperience):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        bookings = experience.bookings.filter(
            experience__pk=pk,
            kind=Booking.BookingKindChoices.EXPERIENCE,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data,
            context={"experience": experience},
        )
        if serializer.is_valid():
            booking = serializer.save(
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                experience=experience,
            )
            serializer = PrivateBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# experiences/:pk/bookings/:pk
# GET DELETE
class ExperienceBookingDetail(CommonExperience):

    permission_classes = [IsAuthenticated]

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if request.user != booking.user:
            raise PermissionDenied
        serializer = PrivateBookingSerializer(booking)
        return Response(serializer.data)

    def delete(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if request.user != booking.user:
            raise PermissionDenied
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# experiences/:pk/reviews?page=<int>
# GET POST
class ExperienceReviews(CommonExperience):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        experience = self.get_object(pk)
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except:
            page = 1
        page = int(page)
        start = (page - 1) * settings.PAGE_SIZE
        end = start + settings.PAGE_SIZE
        reviews = experience.reviews.all()[start:end]
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        if experience.host == request.user:
            raise PermissionDenied("Owner can't remain reviews")
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                experience=experience,
            )
            return Response(ReviewSerializer(review).data)
        else:
            return Response(serializer.errors)


# experiences/perks
# GET POST
class Perks(APIView):
    def get_object(self):
        return Perk.objects.all()

    def get(self, request):
        serializer = PerkSerializer(self.get_object(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


# experiences/perks/:pk
# GET PUT DELETE
class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        return Response(PerkSerializer(perk).data)

    def put(self, request, pk):
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied
        perk = self.get_object(pk=pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated = serializer.save()
            return Response(PerkSerializer(updated).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied

        self.get_object(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
