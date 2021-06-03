import graphene
from .types import UserType
from .models import User
from .mutations import CreateAccountMutation, LoginMutation, ToggleFavsMutation, EditProfileMutation

class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return info.context.user
        else:
            raise Exception("You need to be logged in")

class Mutation(object):
    create_account = CreateAccountMutation.Field()
    login = LoginMutation.Field()
    toggle_favs = ToggleFavsMutation.Field()
    edit_profile = EditProfileMutation.Field()