''' Script to dump movielens dataset to database '''

import pandas as pd
import os, sys, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recommender.settings")
django.setup()
from movie.models import Genre, Movie
from rating.models import DatasetRating
from decimal import Decimal

DATASET_DIR = '/Users/Pratulya/Desktop/tcs/ml-latest-small/'

print('--------------- READING DATASETS ----------------')

movies_df = pd.read_csv(DATASET_DIR + 'movies.csv')
ratings_df = pd.read_csv(DATASET_DIR + 'ratings.csv')
links_df = pd.read_csv(DATASET_DIR + 'links.csv', dtype={'imdbId': object, 'tmdbId': object}) # To preserve imdbId prefixed zeroes
#tags_df = pd.read_csv(DATASET_DIR + 'tags.csv')

print('--------------- STARTING TO DUMP ----------------')

genres = movies_df['genres'].str.get_dummies(sep='|').columns
for genre in genres:
	Genre.objects.get_or_create(name=genre)
genres_q = Genre.objects.all()

print('--------------- DUMPED GENRES ----------------')

# Changing data types to preserve tmdbId from changing to float
links_df['tmdbId'].fillna(0, inplace=True)
links_df['tmdbId'] = links_df['tmdbId'].astype(object)


# Merging movies and links
merged_df = movies_df.copy()#.drop(['genres'], axis=1)
merged_df['genres'] = merged_df['genres'].str.split('|')
merged_df = merged_df.merge(links_df, on='movieId', how='inner')


# Merging with ratings
merged_df = merged_df.merge(ratings_df, on='movieId', how='inner')
merged_df = merged_df.drop(['timestamp'], axis=1)

merged_grouped = merged_df.groupby('movieId')

print('--------------- GO GRAB A SNACK ----------------')

# Create objects
for index in merged_grouped.indices:
	try:
		group = merged_grouped.get_group(index)
		movielensID = int(group['movieId'].values[0])
		name = str(group['title'].values[0])
		imdbID = str(group['imdbId'].values[0])
		tmdbID = str(group['tmdbId'].values[0])
		genres = group['genres'][group.first_valid_index()] # To get list; otherwise group['genres'] is pd.Series
		mean_rating = float(group['rating'].mean())
	# Creating movie
		movie = Movie.objects.create(name=name, imdbID=imdbID, tmdbID=tmdbID, movielensID=movielensID, mean_rating=Decimal(mean_rating))
	# # #
	# Adding genres
		for genre in genres:
			movie.genres.add(genres_q.get(name=genre))
	# # #
	
# Creating Ratings
		ratings = group['rating'].values
		user_ids = group['userId'].values
		try:
			for i in range(len(ratings)):
				DatasetRating.objects.create(score=ratings[i], userID=user_ids[i], movie=movie)
		except Exception as e:
			print(e)
			print(group['title'].values[0])
# # #
	except Exception as e:
		print(e)
		print(group['title'].values[0])

print('--------------- DUMPED ----------------')
print('%d Movies' % (Movie.objects.count()))
print('%d Genres' % (Genre.objects.count()))
print('%d Dataset Ratings' % (DatasetRating.objects.count()))
