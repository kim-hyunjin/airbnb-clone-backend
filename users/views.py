from jwt import encode
from django.contrib.auth import authenticate
from django.conf import settings
from rooms.models import Room
from rooms.serializers import RoomSerializer
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_user = serializer.save()
        return Response(UserSerializer(new_user).data)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response()


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


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    encoded_jwt = encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
    return Response(data={"token": encoded_jwt})