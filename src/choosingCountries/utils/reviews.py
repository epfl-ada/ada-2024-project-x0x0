import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_reviews(breweries, BA_merged):

    BA_merged_cleaned = BA_merged.dropna(subset=['user_location', 'beer_location'])

    #Local reviews (reviews written by people from one country reviewing beers from that same location)
    local_reviews = BA_merged_cleaned[BA_merged_cleaned['user_location'] == BA_merged_cleaned['beer_location']].groupby('beer_location').size().reset_index(name='local_reviews')

    #Non-local reviews (reviews written by people for beers from other location)
    non_local_reviews = BA_merged_cleaned[BA_merged_cleaned['user_location'] != BA_merged_cleaned['beer_location']].groupby('beer_location').size().reset_index(name='non_local_reviews')

    country_stats = breweries.groupby('location').agg(
        total_breweries=('id', 'nunique'), 
        total_beers=('nbr_beers', 'sum') 
    ).reset_index()

    country_data = pd.merge(country_stats, local_reviews, left_on='location', right_on='beer_location', how='left')
    country_data = pd.merge(country_data, non_local_reviews, left_on='location', right_on='beer_location', how='left')

    #no reviews is NaN, 0 is better for plotting
    country_data[['local_reviews', 'non_local_reviews']] = country_data[['local_reviews', 'non_local_reviews']].fillna(0)

    country_data = country_data.sort_values(by='local_reviews', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 8))

    #Identify states that are in the US
    highlighted = country_data['location'].str.startswith('United States')

    #Plot for countries that are NOT 'United States' in blue
    scatter = ax.scatter(
        country_data.loc[~highlighted, 'local_reviews'],
        country_data.loc[~highlighted, 'non_local_reviews'],
        s=country_data.loc[~highlighted, 'total_beers'] * 0.1,
        color='blue', 
        alpha=0.6,
        edgecolor='black',
        label='Other Countries'
    )

    #Plot for US states in red
    scatter_us = ax.scatter(
        country_data.loc[highlighted, 'local_reviews'],
        country_data.loc[highlighted, 'non_local_reviews'],
        s=country_data.loc[highlighted, 'total_beers'] * 0.1,
        color='red',
        alpha=0.6,
        edgecolor='black',
        label='United States'
    )

    # Set plot labels and title
    ax.set_xlabel('Local Reviews')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylabel('Non-Local Reviews')
    ax.set_title('Local vs Non-Local Reviews by Country (Size Proportional to total number of beers produced by each state/country)')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper left')
    plt.tight_layout()
    
    plt.show()
    
    return