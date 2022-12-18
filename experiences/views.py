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
from rest_framework.permissions import IsAuthenticated
from experiences.serializers import ExperienceSerializer, PerkSerializer


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
    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            # validate category
            category = self.validate_category(request)

            # create experience
            experience = serializer.save(host=request.user, category=category)

            # add perks
            perks = self.validate_perk(request)
            for perk in perks:
                experience.perks.add(perk)

            serializer = ExperienceSerializer(experience)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# experiences/:pk
# GET PUT DELETE
class ExperienceDetail(CommonExperience, ValidationExperience):
    def get(self, request, pk):
        experience = self.get_object(pk=pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk=pk)

        if experience.host != request.user:
            raise PermissionDenied

        serializer = ExperienceSerializer(
            instance=experience,
            data=request.data,
            partial=True,
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
            serializer = ExperienceSerializer(updated)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk=pk)
        if experience.host != request.user:
            raise PermissionDenied

        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


# experiences/perks
class Perks(APIView):
    serializer_class = PerkSerializer

    def get_object(self):
        return Perk.objects.all()

    def get(self, request):
        serializer = PerkSerializer(self.get_object(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


# experiences/perks/:pk
class PerkDetail(APIView):
    serializer_class = Perk

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(PerkSerializer(self.get_object(pk=pk)).data)

    def put(self, request, pk):
        perk = self.get_object(pk=pk)
        serializer = PerkSerializer(
            instance=perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated = serializer.save()
            return Response(PerkSerializer(updated).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
