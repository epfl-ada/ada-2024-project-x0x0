import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu


def plot_avg_and_D(US_ratings):
    
    states = US_ratings['user_state'].unique()

    bias_results = []
    
    for state in states:
        state_avg, other_states_avg, p_value = calculate_bias(state, US_ratings)
        bias_results.append({
            'state': state,
            'state_avg': state_avg,
            'other_states_avg': other_states_avg,
            'p_value': p_value,
            'rating_difference': state_avg - other_states_avg
        })


    bias_df = pd.DataFrame(bias_results)

    bias_df['significant'] = bias_df['p_value'] < 0.05


    bias_df = bias_df.sort_values(by=['rating_difference', 'significant'], ascending=False)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='rating_difference', y='state', data=bias_df, palette='coolwarm', hue='significant')

    plt.xlabel('Rating Difference (State vs Other States)')
    plt.ylabel('State')
    plt.title('States Ranked by Bias Towards Their Own Beer')
    plt.tight_layout()

    plt.show()
    
    return
    
    
def calculate_bias(state, US_ratings):

    state_ratings = US_ratings[(US_ratings['user_state'] == state) & (US_ratings['beer_state'] == state)]['rating']
    other_states_ratings = US_ratings[(US_ratings['user_state'] != state) & (US_ratings['beer_state'] == state)]['rating']
    
    state_avg = state_ratings.mean()
    other_states_avg = other_states_ratings.mean()
    
    stat, p_value = mannwhitneyu(state_ratings, other_states_ratings, alternative='two-sided')
    
    return state_avg, other_states_avg, p_value


