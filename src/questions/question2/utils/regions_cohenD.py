import pandas as pd
from src.questions.question2.utils.cohenD import cohen_d
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def regions_cohenD(df_neighbours, US_ratings, plot=True):
    cohen_results_by_region = {}
    
    for index, row in df_neighbours.iterrows():
        state = row['state']
        neighbours = row['neighbours']

        if neighbours:
            region_states = [state] + neighbours
        else:
            region_states = [state] #if a state doesn't have neighbours we consider it as a region (like Alaska and Hawaii)

        in_region_ratings = US_ratings[US_ratings['user_state'].isin(region_states)]['rating'] #take only the ratings of states inside the region
        out_of_region_ratings = US_ratings[~US_ratings['user_state'].isin(region_states)]['rating'] #take only the ratings of states outside the region

        if len(in_region_ratings) < 2 or len(out_of_region_ratings) < 2: #in order to do correctly the cohen test
            print("Warning nan")
            cohen_results_by_region[state] = np.nan
            continue

        d_value = cohen_d(in_region_ratings, out_of_region_ratings)
        cohen_results_by_region[state] = d_value

    #table to see the Cohen factor for each region
    cohen_by_region_df = pd.DataFrame.from_dict(cohen_results_by_region, orient='index', columns=['Cohen_d'])
    cohen_by_region_df.index.name = 'Center State of each Region'
    cohen_by_region_df = cohen_by_region_df.reset_index()
    cohen_by_region_df = cohen_by_region_df.sort_values(by='Cohen_d', ascending=False)

    if plot:
        plt.figure(figsize=(14, 8))
        sns.barplot(data=cohen_by_region_df, x='Center State of each Region', y='Cohen_d', palette='viridis')
        plt.title("Cohen's D for in-region ratings compared to out-of-region ratings for the region's users")
        plt.xlabel("Center State of each Region")
        plt.ylabel("Cohen's D value")
        plt.xticks(rotation=90)
        
        plt.axhline(y=0, color='black', linewidth=1)

        plt.axhline(y=0.2, color='#FFA07A', linestyle=':', linewidth=2, label='Small effect (d=0.2)')
        plt.axhline(y=-0.2, color='#FFA07A', linestyle=':', linewidth=2)
        plt.axhline(y=0.5, color='#FF8C00', linestyle=':', linewidth=2, label='Medium effect (d=0.5)')
        plt.axhline(y=-0.5, color='#FF8C00', linestyle=':', linewidth=2)

        plt.tight_layout()
        plt.show()
        
    return cohen_by_region_df

