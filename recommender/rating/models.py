from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from movie.models import Movie

# Create your models here.

class Rating(models.Model):
	score = models.FloatField(default=0.0,
			validators=[
				RegexValidator(
					regex = r'^\d\.{0,5}$',
					message = 'Score must in steps of 0.5',
					code = 'invalid_score'
				),
				MinValueValidator(0.0),
				MaxValueValidator(5.0)
			])
	movie = models.ForeignKey(Movie, related_name="ratings")

	class Meta:
		abstract = True

class DatasetRating(Rating):
	userID = models.PositiveIntegerField() # Integer for ease in list[indexing] purposes

	class Meta:
		unique_together = ['movie', 'userID']

'''
to be implemented
class UserRating(Rating):
	# User registered on platform
	class Meta:
		unique_together = []
'''
