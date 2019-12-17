from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoModelPermissions

from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from api.models import Person, Movie
from api.serializers import PersonSerializer, MovieSerializer
from rest_framework import generics, views, status


# Create your views here.

class LoginView(views.APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user_id": user.id,
                "key": token.key
            })


# class CustomDjangoModelPermission(DjangoModelPermissions):

    # def __init__(self):
    #     self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

''' Generic view - get persons list and add person '''
# class PersonListView(generics.ListCreateAPIView):
#     queryset = Person.objects.all().order_by('id')
#     serializer_class = PersonSerializer
#     permission_classes = (CustomDjangoModelPermission, )

''' APIView - get persons list and add person '''


class PersonListView(views.APIView):
    permission_classes = (DjangoModelPermissions, )
    
    def get_queryset(self):
        return Person.objects.all().order_by('id')

    def get(self):
        persons = self.get_queryset()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

