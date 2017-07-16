# Modify this script to adapt to new separate considerations of popularity and similarity
# Reinforcement Learning - Run this weekly/bi-weekly
import math

def tweaked_sigmoid(x, delta_x):
    if x >= 1.0:
        x = 0.9999
    z = -math.log((1-x)/x)
    f = 1/(1 + (math.exp(-(delta_x + z))))
    return f

#tweaked_sigmoid(0.68, -0.02)


def is_substantial_visits(visits):
    # (is_substantial, redemption)
    if visits < 10:
        return (False, 100)
    elif visits >= 10 and visits < 100:
        return (True, 10)
    else:
        return (True, 1)

def feedback(visits, clicks, movies):
    substantial_visits, redemption = is_substantial_visits(visits)
    for movie in movies:
        movie_clicks = movie['clicks']
        try:
            improvement = movie_clicks / clicks
        except ZeroDivisionError:
            improvement = 0
        
        # Penalising each recommendation for the untransformed visit into a potential click
        # Redemption: subtracting individual's share to total clicks + considering the visits for redemption
        # Penalising each for its share among the len(movies) movies
        # visits >= clicks always
        # No need to penalize if visits are meager
        if clicks and substantial_visits:
            penalty = (clicks - movie_clicks)/(len(movies) * visits * redemption)
                                    # because min order of hundreths is desirable
        elif not clicks and substantial_visits:
            penalty = math.sqrt(visits)/1000 # Penalize more if more visits
        else:
            penalty = 0
        movie['similarity'] = tweaked_sigmoid(movie['similarity'], improvement - penalty)
    return movies

movies = [
    {'clicks': 100, 'similarity': 0.5},
    {'clicks': 39, 'similarity': 0.7},
    {'clicks': 10, 'similarity': 0.55},
    {'clicks': 7, 'similarity': 0.55},
    {'clicks': 0, 'similarity': 0.59},
]
print(feedback(10200, 156, movies))
