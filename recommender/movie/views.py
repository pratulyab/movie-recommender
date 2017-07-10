from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import F, Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
#from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from movie.forms import GenreForm
from movie.models import Movie

# Create your views here.

@require_GET
def landing(request):
	return render(request, 'landing.html', {'genre_form': GenreForm()})

@require_GET
def search(request):
	query = request.GET.get('query')
	if not query:
		if request.is_ajax():
			return JsonResponse(status=200, data={'success': False, 'message': "No results found."})
		else:
			return render(request, 'search_results.html', {})
	if request.is_ajax(): # Search bar
		# Show weighted searches
		total_results = 10
		movies = Movie.objects.filter(name__icontains = query).order_by('-mean_rating')[:total_results]
		result = []
		for movie in movies:
			result.append({'name': movie.__str__(), 'url': movie.get_absolute_url()})
		return JsonResponse(status=200, data={'success': True, 'result': result})
	else:
		# Show more relevant searches
		total_results = 20
		movie_startswith = Movie.objects.filter(name__istartswith = query).order_by('-mean_rating')[:int(total_results * 0.6)]
		remaining_results = total_results - movie_startswith.count()
		movie_contains = Movie.objects.filter(name__icontains = query).\
						 exclude(movielensID__in=[m['movielensID'] for m in movie_startswith.values('movielensID')]).\
						 order_by('-mean_rating')[:remaining_results]
		from itertools import chain
		movies = sorted(
				chain(list(movie_startswith), list(movie_contains)),
				key=lambda instance: instance.mean_rating,
				reverse=True)
		return render(request, 'search_results.html', {'movies': movies})

@require_GET
def movie(request, uuid):
	movie = get_object_or_404(Movie, pk=uuid)
	
	# Updating visit count
	Movie.objects.filter(pk=movie.pk).update(visits = F('visits') + 1)
	
	previous = request.GET.get('from') # uuid of movie the user came from, to this movie
	if previous:
		# Add movielensID of this movie to previous's outbound
		csv = str(movie.movielensID) + ','
		Movie.objects.filter(pk=previous).update(outbounds = F('outbounds') + csv)
	
	recommendations = movie.get_recommendations(5)
	return render(request, 'movie.html', {'movie': movie, 'recommendations': recommendations})

@require_POST
def genre_based_recommendations(request):
	f = GenreForm(request.POST)
	if f.is_valid():
#		recommended_movies = f.get_recommendations(7)
#		recommendations = []
#		for movie in recommended_movies:
#			recommendations.append({'name': movie.__str__(), 'url': movie.get_absolute_url()})	
		html = render(request, 'genre.html', {'recommendations': f.get_recommendations(7)}).content.decode('utf-8');
		return JsonResponse(status=200, data={'html': html})
	return JsonResponse(status=400, data={'error': 'Please choose a valid genre'})
