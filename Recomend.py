import pandas as pd
import numpy as nm
from collections import OrderedDict

print ("Lets do this")

movies_df = pd.read_csv('/home/prafful/Desktop/ml-latest-small/movies.csv', header=None, names=['movie_id', 'movie_title', 'movie_genre'])
movies_df = pd.concat([movies_df, movies_df.movie_genre.str.get_dummies(sep='|')], axis=1)  
'''
print("Enter the movie name")
movie_name=raw_input()
#print (movies_df.iloc[1426][1])
for x in range(0,9000):
	if (movie_name==movies_df.iloc[x][1]):
		print (movies_df.loc[x])
'''
class Genre:
	def  __init__(movie,gen,points):
		movie.gen = gen
		movie.points = points
		
	def d(movie):
		print (movie.gen,movie.points)

print ("Enter 3 Genres")
genre_1=raw_input()
genre_2=raw_input()
genre_3=raw_input()

x=Genre(genre_1,5)
y=Genre(genre_2,3)
z=Genre(genre_3,2)

movie_categories = movies_df.columns[3:]  
p=[]
for i in movie_categories:
	if(x.gen==i):
		p.append(x.points)
	elif(y.gen==i):
		p.append(y.points)
	elif(z.gen==i):
		p.append(z.points)
	else:
		p.append(0)
print (p)

def dot_product(vector_1, vector_2):  
    return sum([ i*j for i,j in zip(vector_1, vector_2)])

def get_movie_score(movie_features, p):  
    return dot_product(movie_features, p)
	
def get_movie_recommendations(p, n_recommendations):  
    #we add a column to the movies_df dataset with the calculated score for each movie for the given user
    movies_df['score'] = movies_df[movie_categories].apply(get_movie_score, 
                                                           args=([p]), axis=1)
    print( movies_df.sort_values(by=['score'], ascending=False)['movie_title'][:n_recommendations])

get_movie_recommendations(p, 10)  
