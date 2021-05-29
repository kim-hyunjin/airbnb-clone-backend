from rooms.models import Room
from rest_framework import serializers
from users.serializers import TinyUserSerializer

# ModelSerializer가 Meta에 명시한 모델을 보고, 명시한 필드를 serialize한다.
class RoomSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer()
    
    class Meta:
        model = Room
        fields = ("name", "price", "instant_book", "user")