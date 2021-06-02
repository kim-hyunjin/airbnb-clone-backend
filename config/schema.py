import graphene
from rooms.models import Room
from graphene_django import DjangoObjectType

class RoomType(DjangoObjectType):
    class Meta:
        model = Room

class Query(graphene.ObjectType):
    hello = graphene.String()
    rooms = graphene.List(RoomType)

    def resolve_hello(self, info):
        return "Hello"

    def resolve_rooms(self, info):
        return Room.objects.all()

class Mutation():
    pass

schema = graphene.Schema(query=Query)