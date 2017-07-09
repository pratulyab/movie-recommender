from django.core.validators import validate_comma_separated_integer_list, MinValueValidator, MaxValueValidator
from django.db import models
from decimal import Decimal
import uuid

# Adapting to Movielens Dataset

class Genre(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name


class Movie(models.Model):

# Details
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200, unique=True) # Unable to store utf-8 charset names
	# https://stackoverflow.com/questions/2108824/mysql-incorrect-string-value-error-when-save-unicode-string-in-django

	year = models.CharField(max_length=4, blank=True)

# Dataset IDs
	imdbID = models.CharField(max_length=10, unique=True) # Intenet Movie Database
	tmdbID = models.CharField(max_length=10) # The Movie Database # Inconsistency in dataset. Therefore, multiple NaNs. Removed unique constraint
	movielensID = models.PositiveIntegerField(unique=True)  # Movielens ID or dataset's movieId # Integer for ease in list[indexing] purposes

# Genres
	genres = models.ManyToManyField(Genre, related_name="movies")

# Stats
	mean_rating = models.DecimalField('Average Rating', max_digits=8, decimal_places=7, default=Decimal(0),\
				validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(5))])
	visits = models.PositiveIntegerField(default=0) # Page visits
	outbounds = models.TextField(validators=[validate_comma_separated_integer_list], blank=True)
	''' outbounds field stores movielensID of movies that users followed from this movie's recommendations '''

	def imdb_url(self):
		return "https://www.imdb.com/title/tt%s/" % (self.imdbID)
	
	def tmdb_url(self):
		return "https://www.themoviedb.org/movie/%s" % (self.tmdbID)

	def movielens_url(self):
		return "https://movielens.org/movies/%s" % (self.movielensID)

	def __str__(self):
		return self.name.title()
