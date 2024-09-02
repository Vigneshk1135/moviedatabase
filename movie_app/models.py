from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()  #
    actors = models.CharField(max_length=200)
    release_date = models.DateTimeField()
    youtube_link = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')  # Foreign key to UserProfile
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')  # Foreign key to Movie
    rating = models.PositiveIntegerField()
    review = models.TextField()

    def __str__(self):
        return f'Review by {self.user.username} for {self.movie.name}'
