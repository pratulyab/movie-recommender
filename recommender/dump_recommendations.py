''' Script to dump recommendations as well as popularity score '''
import django, os
from movie_recommender import MOVIE_RECOMMENDATIONS_PKL, get_pickle, get_recommendations_for
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")
django.setup()
from movie.models import Genre, Movie
from decimal import Decimal
from django.conf import settings

PICKLE_DIR = '../pickles/'

def get_file_number(pickle_filename):
	return 
def dump():
	filename_str = MOVIE_RECOMMENDATIONS_PKL.split('/')[-1].split('.')[0].replace('%s','')
	recommendation_files = [filename for filename in os.listdir(PICKLE_DIR) if filename.startswith(filename_str)]
	recommendation_files = sorted(recommendation_files, key=lambda filename: int(filename.split('_')[-1].split('.')[0]))
	
	for filename in recommendation_files:
		recommendations_dict = get_pickle(PICKLE_DIR + filename)
		if recommendations_dict is None:
			print('Error Reading', filename)
			continue
		for movieID,recommendations in recommendations_dict.items():
			try:
				movie = Movie.objects.get(movielensID = movieID)
			except Movie.DoesNotExist:
				print("Movie with movielensID %d does not exist in DB" % (movieID))
				continue
			# Storing only 10 recommendations out of 20 in df
			recommended_movies = recommendations.sort_values(by='popularity', ascending=False)['movieId'].values[:10]
			recommended_movies = ','.join(map(str, recommended_movies)) # Storing recommendations as comma-separated movieIds
			# Popularity
			popularity = Decimal(settings.MOVIE_POPULARITY_DF.get_value(settings.MOVIE_POPULARITY_DF.loc[settings.MOVIE_POPULARITY_DF['movieId'] == movieID].index[0],'popularity'))
			popularity = round(popularity, 6) # Upto 6 places of decimal
			movie.recommendations = recommended_movies
			movie.popularity = popularity
			try:
				movie.save()
			except Exception as e:
				print(e)
				print('Error saving movie %d' % (movieId))

		print('-- DUMPED %s --' % (filename))

if __name__ == '__main__':
	dump()
	print('-- Somehow recommendations for movieId 1 didn\'t get pickled. Onto that ---')
	movie = Movie.objects.get(movielensID=1)
	recommendations_1 = get_recommendations_for(1)['movieId'].values[:10]
	recommendations_1 = ','.join(map(str, recommendations_1))
	popularity = Decimal(settings.MOVIE_POPULARITY_DF.get_value(settings.MOVIE_POPULARITY_DF.loc[settings.MOVIE_POPULARITY_DF['movieId'] == 1].index[0],'popularity'))
	popularity = round(popularity, 6) # Upto 6 places of decimal
	movie.recommendations = recommendations_1
	movie.popularity = popularity
	try:
		movie.save()
	except Exception as e:
		print(e)
		print('Error saving movie 1')
	
	print('-=-=-=-=-=-=-=-=-=-=-=- ALL SET -=-=-=-=-=-=-=-=-=-=-=-')
