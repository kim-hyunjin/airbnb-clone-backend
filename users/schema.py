import graphene
from .types import UserType
from .models import User
from .mutations import CreateAccountMutation, LoginMutation

class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

class Mutation(object):
    create_account = CreateAccountMutation.Field()
    login = LoginMutation.Field()