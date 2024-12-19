import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines


def plot_reviews(breweries, BA_merged):

    BA_merged_cleaned = BA_merged.dropna(subset=['user_location', 'beer_location'])

    #Local reviews (reviews written by people from one country reviewing beers from that same location)
    local_ratings = BA_merged_cleaned[BA_merged_cleaned['user_location'] == BA_merged_cleaned['beer_location']].groupby('beer_location').size().reset_index(name='local_ratings')

    #Non-local reviews (reviews written by people for beers from other location)
    non_local_ratings = BA_merged_cleaned[BA_merged_cleaned['user_location'] != BA_merged_cleaned['beer_location']].groupby('beer_location').size().reset_index(name='non_local_ratings')

    country_stats = breweries.groupby('location').agg(
        total_breweries=('id', 'nunique'), 
        total_beers=('nbr_beers', 'sum') 
    ).reset_index()

    country_data = pd.merge(country_stats, local_ratings, left_on='location', right_on='beer_location', how='left')
    country_data = pd.merge(country_data, non_local_ratings, left_on='location', right_on='beer_location', how='left')

    #no reviews is NaN, 0 is better for plotting
    country_data[['local_ratings', 'non_local_ratings']] = country_data[['local_ratings', 'non_local_ratings']].fillna(0)

    country_data = country_data.sort_values(by='local_ratings', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 8))

    #Identify states that are in the US
    highlighted = country_data['location'].str.startswith('United States')

    #Plot for countries that are NOT 'United States' in blue
    scatter = ax.scatter(
        country_data.loc[~highlighted, 'local_ratings'],
        country_data.loc[~highlighted, 'non_local_ratings'],
        s=country_data.loc[~highlighted, 'total_beers'] * 0.1,
        color='#dd660d', 
        alpha=0.6,
        edgecolor='black',
        label='Other Countries'
    )

    #Plot for US states in red
    scatter_us = ax.scatter(
        country_data.loc[highlighted, 'local_ratings'],
        country_data.loc[highlighted, 'non_local_ratings'],
        s=country_data.loc[highlighted, 'total_beers'] * 0.1,
        color='#5b8a72',
        alpha=0.6,
        edgecolor='black',
        label='United States'
    )

    legend_size = 10  # This size is arbitrary but ensures uniformity
    legend_scatter_other = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='#dd660d', markersize=legend_size, label='Other Countries', markeredgewidth=2)
    legend_scatter_us = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='#5b8a72', markersize=legend_size, label='United States', markeredgewidth=2)


    # Set plot labels and title
    ax.set_xlabel('Local Ratings')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylabel('Non-Local Ratings')
    ax.set_title('Local vs Non-Local Ratings by Country (Size Proportional to total number of beers produced by each state/country)')
    ax.grid(True, linestyle='--', alpha=0.7)
    #ax.legend(loc='upper left')
    ax.legend(handles=[legend_scatter_other, legend_scatter_us], loc='upper left')

    plt.tight_layout()
    
    plt.show()
    
    return