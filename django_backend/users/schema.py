import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "user_type")


class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    user_type = graphene.Int()
    

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)
    
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        profile_image = info.context.FILES.get('profile_image')  # Get the uploaded file
        user_instance = User(
            username=input.username,
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
            password=input.password,
            user_type=input.user_type
        )
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.username = input.username
            user_instance.first_name = input.first_name
            user_instance.last_name = input.last_name
            user_instance.email = input.email
            user_instance.password = input.password
            user_instance.user_type = input.user_type
            # user_instance.profile_image = input.profile_image
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, actor=None)

class AuthenticateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()

    @staticmethod
    def mutate(root, info, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            # TODO: Generate a token and return it
            token = "your_generated_token"
            return AuthenticateUser(token=token)
        else:
            raise Exception('Invalid username or password')
        
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    authenticate_user = AuthenticateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)