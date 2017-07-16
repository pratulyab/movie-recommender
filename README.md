# Movie Recommender
### MovieLens Dataset
### Hosted At: http://movierecommender.pythonanywhere.com

### Recommendations:
- Movie-movie similarity using Pearson's correlation coefficient
- Popularity score
- Genre based recommendations (Simple dot product)

### Feedback: (An attempt)
- Storing the visits and outbounds for each movie.
- Improving recommendations based on user-activity
  - Page visits
  - Recommendations followed by a user (click)
- Penalizing the stale recommendations; in order to make way for new recommendations
- Achieving this by altering the popularity of movies
