from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from bookings.models import Booking
from bookings.serializers import PrivateBookingSerializer


# bookings/
class BookingList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        return Response(PrivateBookingSerializer(bookings, many=True).data)


# bookings/:pk
class BookingDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise exceptions.NotFound

    def delete(self, request, pk):
        booking = self.get_object(pk)

        if booking.user != request.user:
            raise exceptions.PermissionDenied

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
