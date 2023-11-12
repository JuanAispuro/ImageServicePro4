from django.db import models
from django.contrib.auth.models import User




class Artist(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    born_date = models.CharField(max_length=200)


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Style(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Period(models.Model):
    name = models.CharField(max_length=200, unique=True)



class Artwork(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Artist, on_delete=models.RESTRICT)
    path = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    date = models.CharField(max_length=200, null=True)
    style = models.ForeignKey(Style, null=True, on_delete=models.RESTRICT)
    period = models.ForeignKey(Period, null=True, on_delete=models.RESTRICT)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.RESTRICT)
    image_url = models.URLField()


class savedArtworks(models.Model):
    userfK = models.ForeignKey(User, on_delete=models.CASCADE)
    artworkfK = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    favorited = models.BooleanField(default=False)
    
