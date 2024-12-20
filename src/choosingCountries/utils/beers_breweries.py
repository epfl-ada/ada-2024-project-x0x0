import matplotlib.pyplot as plt
import pandas as pd


def plot_beer_breweries_distribution(breweries: pd.DataFrame):
    
    country_stats = breweries.groupby('location').agg(
        total_breweries=('id', 'nunique'),
        total_beers=('nbr_beers', 'sum')
    ).reset_index().sort_values(by='total_beers', ascending=False)

    fig, ax1 = plt.subplots(figsize=(8, 5))

    #total beers
    ax1.bar(country_stats['location'], country_stats['total_beers'], 
            color=['green' if country.startswith('United States,') else 'blue' for country in country_stats['location']],
            label='Total Beers')

    #total breweries (twin axis)
    ax2 = ax1.twinx()
    ax2.plot(country_stats['location'], country_stats['total_breweries'], color='orange', label='Total Breweries')

    ax1.set_ylabel('Total Beers')
    ax2.set_ylabel('Total Breweries')

    fig.legend(bbox_to_anchor=(0.9, 0.9), frameon=False)
    plt.title('Total Number of Beers and Breweries per Location')
    plt.xticks([])
    plt.tight_layout()
    plt.show()
        
    return