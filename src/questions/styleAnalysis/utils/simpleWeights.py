import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt



def simple_top_style(state_style_stats):
    
    state_style_stats_weight = state_style_stats
    state_style_stats_weight['weight'] = state_style_stats['average_rating'] * state_style_stats['nb_ratings']

    # beer style with maximum weight per state
    top_style_per_state = state_style_stats_weight.groupby('user_state').apply(lambda x: x.loc[x['weight'].idxmax()]).reset_index(drop=True)

    plt.figure(figsize=(18, 12))
    sns.barplot(data=top_style_per_state, x='user_state', y='weight', hue='style')
    plt.title("Top Beer Style with Highest Weight per State", fontsize=16)
    plt.xticks(rotation=90)
    plt.xlabel('State')
    plt.ylabel('Weight (Average Rating * Number of Ratings)')
    plt.legend(title='Beer Style', loc='upper left')
    plt.show()

    return


def simple_2nd_top_style(state_style_stats):
    
    state_style_stats_weight = state_style_stats
    state_style_stats_weight['weight'] = state_style_stats['average_rating'] * state_style_stats['nb_ratings']
    
    # Second best weighted style per state
    top_2_styles_per_state = state_style_stats_weight.groupby('user_state').apply(lambda x: x.nlargest(2, 'weight')).reset_index(drop=True)

    second_best_styles = top_2_styles_per_state.groupby('user_state').nth(1).reset_index()

    plt.figure(figsize=(18, 12))
    sns.barplot(data=second_best_styles, x='user_state', y='weight', hue='style')
    plt.title("Second Best Beer Style by Weight per State", fontsize=16)
    plt.xticks(rotation=90)
    plt.xlabel('State')
    plt.ylabel('Weight (Average Rating * Number of Ratings)')
    plt.legend(title='Beer Style', loc='upper left')
    plt.tight_layout()
    plt.show()
    
    return