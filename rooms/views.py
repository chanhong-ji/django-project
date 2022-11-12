from django.shortcuts import render
from rooms.models import Amenity
from rooms.serializers import AmenitySerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT


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
