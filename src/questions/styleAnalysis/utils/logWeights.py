import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def log_top_styles(state_style_stats):
    
    min_ratings_threshold = state_style_stats['nb_ratings'].quantile(0.25) # threshold for minimum ratings
    state_style_stats_thresh = state_style_stats[state_style_stats['nb_ratings'] >= min_ratings_threshold]

    state_style_stats_thresh['weight'] = state_style_stats_thresh['average_rating'] * np.log1p(state_style_stats_thresh['nb_ratings'])
    state_style_stats_thresh['normalized_weight'] = state_style_stats_thresh['weight'] / state_style_stats_thresh.groupby('user_state')['weight'].transform('sum')

    # global popularity adjustment, account for overall beer style preferences like American IPA for example
    global_popularity = state_style_stats_thresh.groupby('style')['nb_ratings'].sum()
    global_popularity_normalized = global_popularity / global_popularity.max()
    state_style_stats_thresh['bias_adjusted_weight'] = state_style_stats_thresh['weight'] / state_style_stats_thresh['style'].map(global_popularity_normalized)
    
    # top beer style per state based on normalized weight
    top_style_per_state = state_style_stats_thresh.groupby('user_state').apply(lambda x: x.loc[x['normalized_weight'].idxmax()]).reset_index(drop=True)

    plt.figure(figsize=(18, 12))
    sns.barplot(data=top_style_per_state, x='user_state', y='normalized_weight', hue='style')
    
    plt.title("Top Beer Style with Highest Normalized Weight per State", fontsize=16)
    plt.xticks(rotation=90)
    plt.xlabel('State')
    plt.ylabel('Normalized Weight (Average Rating * Number of Ratings / State Total)')
    plt.legend(title='Beer Style', loc='upper left')
    plt.tight_layout()
    plt.show()
    
    return top_style_per_state