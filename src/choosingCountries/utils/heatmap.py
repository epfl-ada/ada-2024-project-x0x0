import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def heatmap_avg_ratings(US_ratings):
    
    state_ratings = US_ratings.groupby(['user_state', 'beer_state'])['avg'].mean().reset_index()

    #create matrix which gives the avg rating of each beers of state to user of state combination pair
    state_ratings_matrix = state_ratings.pivot_table(index='user_state', columns='beer_state', values='avg', fill_value=0)

    plt.figure(figsize=(10, 10))

    sns.heatmap(state_ratings_matrix, annot=False, fmt=".2f", cmap='viridis', linewidths=0.5, cbar_kws={'label': 'Average Rating'}, square=True)

    plt.title('Average Ratings of Beers by Users from Different US States', fontsize=16)
    plt.xlabel('Beer State', fontsize=12)
    plt.ylabel('User State', fontsize=12)
    plt.tight_layout()
    
    plt.show()
    
    return
    
