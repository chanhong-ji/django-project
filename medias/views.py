from medias.serializers import PhotoSerializer
from .models import Photo
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config.variables import variables
import requests

# medias/photos
class Photo(APIView):
    def post(self, request):
        urls = request.data.get("urls")
        data = [{"file": url} for url in urls]
        serializer = PhotoSerializer(data=data, many=True)
        if serializer.is_valid():
            photos = serializer.save()
            thumb_photo = photos[0]
            thumb_photo.thumb = True
            thumb_photo.save()
            photos = PhotoSerializer(photos, many=True).data
            return Response([dict(photo).get("pk") for photo in photos])
        else:
            return Response(serializer.errors)


# medias/photos/:int
class PhotoDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk=pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied

        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)


# medias/photos/get-urls
class PhotoUrls(APIView):
    def post(self, request):
        host = f"https://api.cloudflare.com/client/v4/accounts/{variables['cf']['client_id']}/images/v2/direct_upload"
        urls = []
        for _ in range(5):
            data = requests.post(
                host,
                headers={"Authorization": f"Bearer {variables['cf']['client_token']}"},
            ).json()
            url_id = data.get("result").get("id")
            upload_url = data.get("result").get("uploadURL")

            urls.append((url_id, upload_url))
        return Response(urls)
