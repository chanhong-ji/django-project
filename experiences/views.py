from experiences.models import Perk
from experiences.serializers import PerkSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


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


class PerkDetail(APIView):
    serializer_class = PerkSerializer

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
        return Response(status=HTTP_204_NO_CONTENT)
