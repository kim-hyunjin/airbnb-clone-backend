from rooms.models import Room
from rooms.serializers import RoomSerializer
from users.models import User
from users.serializers import ReadUserSerializer, WriteUserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response()


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, request):
        pk = request.data.get("pk", None)
        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = request.user
            room = Room.objects.get(pk=pk)
            if room in user.favs.all():
                user.favs.remove(room)
            else:
                user.favs.add(room)
            return Response()
        except Room.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

