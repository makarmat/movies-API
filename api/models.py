from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    @property
    def person_name(self):
        return '{} {}'.format(self.name, self.last_name)

    def __str__(self):
        return self.person_name


class Movie(models.Model):
    title = models.CharField(max_length=64)
    year = models.IntegerField()
    director = models.ForeignKey(Person, related_name='movie_director', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
