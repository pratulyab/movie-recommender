from django.core.urlresolvers import reverse
from django.core.validators import validate_comma_separated_integer_list, MinValueValidator, MaxValueValidator
from django.db import models
from decimal import Decimal
import re
import uuid

# Adapting to Movielens Dataset

class Genre(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name


class Movie(models.Model):

# Details
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	year = models.CharField(max_length=4, blank=True)

# Dataset IDs
	imdbID = models.CharField(max_length=10) # Intenet Movie Database
	tmdbID = models.CharField(max_length=10) # The Movie Database # Inconsistency in dataset. Therefore, multiple NaNs. Removed unique constraint
	movielensID = models.PositiveIntegerField(unique=True)  # Movielens ID or dataset's movieId # Integer for ease in list[indexing] purposes

# M2Ms
	genres = models.ManyToManyField(Genre, related_name="movies")
	''' Not using M2M Field because free servers are slow while dumping data.'''
#	recommendations = models.ManyToManyField("self", related_name="recommended_for", symmetrical=False, blank=True) # To store a few handy
#	''' symm is false because a cult movie may be recommended for a mediocre considering popularity, but reverse may or may not '''
	recommendations = models.TextField(validators=[validate_comma_separated_integer_list], blank=True) # Store movielensID

# Stats
#	mean_rating = models.DecimalField('Average Rating', max_digits=8, decimal_places=7, default=Decimal(0),\
#				validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(5))])
	popularity = models.DecimalField('Popularity', max_digits=8, decimal_places=6, default=Decimal(0))
	total_visits = models.PositiveIntegerField(default=0) # Updated when feedback script is run
	visits = models.PositiveIntegerField(default=0) # Page visits - Cleared when feedback script is run - Updated on every visit
	outbounds = models.TextField(validators=[validate_comma_separated_integer_list], blank=True)
	''' outbounds field stores movielensID of movies that users followed from this movie's recommendations '''

	def imdb_url(self):
		return "https://www.imdb.com/title/tt%s/" % (self.imdbID)
	
	def tmdb_url(self):
		return "https://www.themoviedb.org/movie/%s" % (self.tmdbID)

	def movielens_url(self):
		return "https://movielens.org/movies/%s" % (self.movielensID)

	def get_absolute_url(self):
		return reverse('movie', kwargs={'uuid': str(self.uuid)})

	def get_recommendations(self, n=5):
		recommendations = Movie.objects.filter(movielensID__in=self.recommendations.split(',')).order_by('-popularity')[:n]
		return recommendations

	def display_name(self):
		return self.__str__()

	def __str__(self):
		return ("{} ({})".format(self.name, self.year) if self.year else self.name)

	class Meta:
		unique_together = ['name', 'year']
