import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import LogNorm



def number_of_ratings_heatmap(state_style_stats):

    state_style_nb_ratings_table = state_style_stats.pivot_table(index='user_state', columns='style', values='nb_ratings', fill_value=0)

    plt.figure(figsize=(18, 12))
    #logscale to see better
    sns.heatmap(state_style_nb_ratings_table, cmap='BuGn', annot=False, norm=LogNorm(), cbar_kws={'label': 'Number of Ratings in log scale'})
    
    plt.xlabel('Beer Style')
    plt.ylabel('State')
    plt.title('Number of Ratings per Beer Style by State')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    return


def ratings_heatmap(state_style_stats):
    # table with all average beer ratings per style for each state
    state_style_average_rating_table = state_style_stats.pivot_table(index='user_state', columns='style', values='average_rating')

    # heatmap to vizualise preferences in beer style per state
    plt.figure(figsize=(25, 12))
    sns.heatmap(state_style_average_rating_table, annot=False, cmap='coolwarm', fmt='.2f', cbar_kws={'label': 'Average rating'})
    
    plt.xticks(rotation=90)
    plt.title('Preferences in Beer Style per State')
    plt.tight_layout()
    plt.show()
    
    return

