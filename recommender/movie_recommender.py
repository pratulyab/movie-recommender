import numpy
import os
import pandas
import pickle

# Pickle File Names
MOVIE_GENRE_SEP_PKL = '../pickles/movie_genre_sep.pkl'
MOVIE_POPULARITY_PKL = '../pickles/movie_popularity.pkl'
MOVIE_RECOMMENDATIONS_PKL = '../pickles/movie_recommendations%s.pkl'
# # #

MOVIE_GENRE_SEP_DF = None # movieId + Separate Genres
MOVIE_RATINGS_DF = None # movieId + Rating Metrics (inc. popularity)

def pickle_this(obj, path):
	f = open(path, 'wb')
	try:
		pickler = pickle.Pickler(f)
		pickler.dump(obj)
		return obj
	except Exception as e:
		print(e)
		return None
	finally:
		f.close()

def get_pickle(path):
	if os.path.isfile(path):
		f = open(path, 'rb')
		try:
			print("Pickle found at %s" % path)
			return pickle.load(f)
		except:
			return None
		finally:
			f.close()

def get_or_create_pickle(pickle_path):
	pickled_obj = get_pickle(pickle_path)

	if pickled_obj is None:
		if pickle_path == MOVIE_GENRE_SEP_PKL:
		# # Movies + Separated Genres # #
			movies_dataset = open('../datasets/movies.csv')
			movies_df = pandas.read_csv(movies_dataset)
			movies_dataset.close()
			
			movies_df = pandas.concat([movies_df.drop(['genres', 'title'], axis=1), movies_df['genres'].str.get_dummies(sep='|')], axis=1)
			pickled_obj = pickle_this(movies_df, pickle_path)
		
		elif pickle_path == MOVIE_POPULARITY_PKL:
			ratings_dataset = open('../datasets/ratings.csv')
			ratings_df = pandas.read_csv(ratings_dataset)
			ratings_dataset.close()
			
			ratings_grouped = ratings_df.groupby('movieId')
			ratings_df = ratings_df.join(ratings_grouped['rating'].sum(), on='movieId', rsuffix='_sum')
			ratings_df = ratings_df.join(ratings_grouped['rating'].mean(), on='movieId', rsuffix='_mean')
			ratings_df = ratings_df.join(ratings_grouped['rating'].count(), on='movieId', rsuffix='_total')
			ratings_df = ratings_df.drop(['userId','rating','timestamp'], axis=1).drop_duplicates().reset_index(drop=True)
			ratings_df['rating_totaln'] = (ratings_df['rating_total'] - ratings_df['rating_total'].mean())/ratings_df['rating_total'].std() # Normalized
			ratings_df['rating_mean'] = ratings_df['rating_mean'] / 5
			ratings_df['popularity'] = ratings_df['rating_totaln'] * ratings_df['rating_mean']
			ratings_df = ratings_df.sort_values(by='movieId')
			pickled_obj = pickle_this(ratings_df, pickle_path)
	
	return pickled_obj

def genre_similarity(movie1, movie2):
	''' Calculates Pearson coefficient between two movies. Params: movieId1, movieId2 '''
	global MOVIE_GENRE_SEP_DF
	
	movie1 = MOVIE_GENRE_SEP_DF.loc[MOVIE_GENRE_SEP_DF['movieId'] == movie1]
	movie2 = MOVIE_GENRE_SEP_DF.loc[MOVIE_GENRE_SEP_DF['movieId'] == movie2]
	return numpy.corrcoef(movie1.values[0][1:], movie2.values[0][1:])[0,1]

def get_genre_recommendations(movie1, n=20):
	global MOVIE_GENRE_SEP_DF
	
	if MOVIE_GENRE_SEP_DF is None:
		MOVIE_GENRE_SEP_DF = get_or_create_pickle(MOVIE_GENRE_SEP_PKL)
	
	similarity = []
	for movie2 in MOVIE_GENRE_SEP_DF['movieId']:
		similarity.append(genre_similarity(movie1, movie2) if movie2 != movie1 else -1000)
	movie_rec_df = MOVIE_GENRE_SEP_DF.copy()
	movie_rec_df['similarity'] = similarity
	movie_rec_df = movie_rec_df.sort_values(by='similarity', ascending=False)
	return movie_rec_df[:n]

def get_recommendations_for(movie, n=10, popular=True):
	global MOVIE_RATINGS_DF

	if MOVIE_RATINGS_DF is None:
		MOVIE_RATINGS_DF = get_or_create_pickle(MOVIE_POPULARITY_PKL) # Popularity
	
	recommended_movies_df = get_genre_recommendations(movie, n*2)
	recommendations_popularity_df = MOVIE_RATINGS_DF[MOVIE_RATINGS_DF['movieId'].isin(recommended_movies_df['movieId'].values)]
	finalized_movies_df = recommended_movies_df.merge(recommendations_popularity_df, on='movieId', how='inner')
	if popular:
		finalized_movies_df = finalized_movies_df.sort_values(by='popularity', ascending=False)
	return finalized_movies_df[:n]

def movie_movie_sim():
	global MOVIE_GENRE_SEP_DF, MOVIE_RATINGS_DF
	
	movies_df = get_or_create_pickle(MOVIE_GENRE_SEP_PKL) # Separate Genres
	ratings_df = get_or_create_pickle(MOVIE_POPULARITY_PKL) # Popularity
	MOVIE_GENRE_SEP_DF = movies_df
	MOVIE_RATINGS_DF = ratings_df

	movie_recommendations_dict = {} # {movieId: recommendations_df}

	# PICKLING OPTIMIZATION
	max_created = 0
	filename_str = MOVIE_RECOMMENDATIONS_PKL.split('/')[-1].split('.')[0].replace('%s','')
	movie_recommendation_files = [filename for filename in os.listdir('pickles') if filename.startswith(filename_str)]
	max_created = max([int(filename.split('_')[-1].split('.')[0]) for filename in movie_recommendation_files] or [0])
	last_index = MOVIE_GENRE_SEP_DF['movieId'].count() - 1
	# # #
	for i,movie in enumerate(MOVIE_GENRE_SEP_DF['movieId']):
		if i <= max_created:
			continue
		movie_recommendations_dict[movie] = get_recommendations_for(movie)
		if i % 100 == 0 or i == last_index: # FILE_BLOCK_SIZE = 100
			suffix = '_%d' % i
			pickle_this(movie_recommendations_dict, MOVIE_RECOMMENDATIONS_PKL % suffix)
			print('-- DUMPED %s --' % (MOVIE_RECOMMENDATIONS_PKL % suffix))
			movie_recommendations_dict = dict()

# # # # # # #
if __name__ == '__main__':
	if not os.path.exists('pickles/'):
		os.makedirs('pickles')
	movie_movie_sim()
