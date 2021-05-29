from django.http.response import HttpResponse
from rooms.models import Room
from django.core import serializers

# Create your views here.
def list_rooms(request):
    rooms = serializers.serialize("json", Room.objects.all())
    response = HttpResponse(content=rooms)
    return response