from django.conf import settings
from movie.models import Genre

movies_df = settings.MOVIE_GENRE_SEP_DF.copy()

weights = {}

def dot_product(vector_1, vector_2):  
	return sum([ i*j for i,j in zip(vector_1, vector_2)])

def get_movie_score(movie_features, p):  
	return dot_product(movie_features, p)
	
def get_movie_recommendations(genresQ, n_recommendations):
	for i,weight in enumerate([5,3,2]):
		try:
			weights[genresQ[i].name] = weight
		except IndexError:
			pass

	movie_categories = movies_df.columns[1:]
	all_weights = []
	for category in movie_categories:
		genre = genresQ.filter(name__exact=category)
		if genre.exists():
			all_weights.append(weights[genre[0].name])
		else:
			all_weights.append(0)

    #we add a column to the movies_df dataset with the calculated score for each movie for the given user
	movies_df['score'] = movies_df[movie_categories].apply(get_movie_score, args=([all_weights]), axis=1)
	return movies_df.sort_values(by=['score'], ascending=False)['movieId'].values[:n_recommendations]
