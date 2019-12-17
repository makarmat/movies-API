from rest_framework import serializers
from api.models import Person, Movie


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    director = PersonSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = ['title', 'year', 'director']

