import pandas as pd
import numpy as np


def weighted_ratings(US_ratings):
    #average ratings for each state when rating its own beer
    own_beer_ratings = US_ratings[US_ratings['user_state'] == US_ratings['beer_state']].groupby('beer_state')['avg'].mean()

    #total number of ratings per beer_state
    total_ratings_per_state = US_ratings.groupby('beer_state').size()

    #weighted average rating for each beer by other states
    other_state_ratings = US_ratings[US_ratings['user_state'] != US_ratings['beer_state']]
    other_state_avg_ratings = other_state_ratings.groupby('beer_state').apply(
        lambda group: np.average(group['rating'], weights=group['user_state'].map(total_ratings_per_state))
    )

    ratings_comparison = pd.DataFrame({
        'own_beer_avg': own_beer_ratings,
        'other_states_avg': other_state_avg_ratings
    })

    ratings_comparison['other_states_avg'] = ratings_comparison['other_states_avg'].fillna(0)
    
    return ratings_comparison