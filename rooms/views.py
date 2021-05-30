# from rest_framework.decorators import api_view
# from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer, WriteRoomSerializer

# @api_view(["GET", "POST"])
# def list_rooms(request):
#     if request.method == "GET":
#         rooms = Room.objects.all()
#         serialized_rooms = RoomSerializer(rooms, many=True).data
#         return Response(data=serialized_rooms)
#     elif request.method == "POST":
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)

#         serializer = WriteRoomSerializer(data=request.data)
#         if serializer.is_valid():
#             # create()나 update() 메소드를 직접 호출하면 안된다. 대신 save() 메소드를 호출하면 내부적으로 알아서 판단해 create또는 update를 호출한다.
#             room = serializer.save(user=request.user)
#             return Response(data=RoomSerializer(room).data, status=status.HTTP_200_OK)
#         else:
#             return Response(dara=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class RoomsView(APIView):

    def get(self, request):
        rooms = Room.objects.all()
        serialized_rooms = RoomSerializer(rooms, many=True).data
        return Response(data=serialized_rooms)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            # create()나 update() 메소드를 직접 호출하면 안된다. 대신 save() 메소드를 호출하면 내부적으로 알아서 판단해 create또는 update를 호출한다.
            room = serializer.save(user=request.user)
            return Response(data=RoomSerializer(room).data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomView(APIView):

    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pass

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)