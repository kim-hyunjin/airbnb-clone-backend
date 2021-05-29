from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Room
from .serializers import RoomSerializer, WriteRoomSerializer
from rest_framework import status

# class ListRoomsView(ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

# url로 넘어오는 pk를 사용해 알아서 Room을 찾아준다.
class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


# class ListRoomsView(APIView):
#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(data=serializer.data)

@api_view(["GET", "POST"])
def list_rooms(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serialized_rooms = RoomSerializer(rooms, many=True).data
        return Response(data=serialized_rooms)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            # create()나 update() 메소드를 직접 호출하면 안된다. 대신 save() 메소드를 호출하면 내부적으로 알아서 판단해 create또는 update를 호출한다.
            room = serializer.save(user=request.user)
            return Response(data=RoomSerializer(room).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            