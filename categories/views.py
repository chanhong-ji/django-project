from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT

# categories/room
class CategoriesRoom(APIView):
    serializer_class = CategorySerializer

    def get_object(self):
        return Category.objects.filter(kind=Category.CategoryKindChoices.ROOMS)

    def get(self, request):
        serializer = CategorySerializer(self.get_object(), many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            raise PermissionError
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save(kind=Category.CategoryKindChoices.ROOMS)
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(status=404, data=serializer.errors)


# categories/experience
class CategoriesExperience(APIView):
    serializer_class = CategorySerializer

    def get_object(self):
        return Category.objects.filter(kind=Category.CategoryKindChoices.EXPERIENCES)

    def get(self, request):
        serializer = CategorySerializer(self.get_object(), many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            raise PermissionError
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save(
                kind=Category.CategoryKindChoices.EXPERIENCES
            )
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(status=404, data=serializer.errors)


class CategoryDetail(APIView):
    def get_obejct(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_obejct(pk))
        return Response(data=serializer.data)

    def post(self, request, pk):
        serializer = CategorySerializer(
            self.get_obejct(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            fixed = serializer.save()
            return Response(CategorySerializer(fixed).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_obejct(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
