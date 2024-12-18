import pandas as pd
import numpy as np



def prep_data(US_ratings, neighbours_df):
    
    #neighbours_df["neighbours"] = neighbours_df["neighbours"].fillna("").apply(lambda x: x.split(";") if x else [])
    #these should be the same but check
    neighbours_df["neighbours"] = neighbours_df["neighbours"].fillna("").str.split(";")
    
    states = US_ratings['beer_state'].unique()

    all_ratings = {'region': [], 'rating': [], 'rating_type': [], 'user_state': []}
    
    ratings_df = make_ratings_df(states, all_ratings, US_ratings, neighbours_df)
    
    ratings_df = ratings_df[ratings_df['rating_type'] == 'In-Region']
    ratings_df = ratings_df.drop('rating_type', axis=1)
    
    ratings_df['rating_type'] = np.where(ratings_df['region'] == ratings_df['user_state'], 'In-State', 'Non-State')
    #avg_ratings = ratings_df.groupby(['region', 'rating_type'])['rating'].mean().unstack()
    #avg_ratings = avg_ratings.reset_index()
    
    print(ratings_df.head(2))
    
    return ratings_df
    
    
def gather_region_ratings(state, US_ratings, neighbours_df):
    neighbours = neighbours_df.loc[neighbours_df['state'] == state, 'neighbours'].values[0]
    
    region_states = [state] + neighbours    
    region_ratings = US_ratings[US_ratings['beer_state'].isin(region_states)]

    in_region_ratings = region_ratings[region_ratings['user_state'].isin(region_states)]
    not_in_region_ratings = region_ratings[~region_ratings['user_state'].isin(region_states)]
    
    return in_region_ratings, not_in_region_ratings


def make_ratings_df(states, all_ratings, US_ratings, neighbours_df):

    for state in states:
        in_region, non_region = gather_region_ratings(state, US_ratings, neighbours_df)

        region_name = f"{state}"
        
        # Add In-Region ratings to the dictionary
        all_ratings['region'].extend([region_name] * len(in_region))
        all_ratings['rating'].extend(in_region['rating'].tolist())
        all_ratings['rating_type'].extend(['In-Region'] * len(in_region))
        all_ratings['user_state'].extend(in_region['user_state'].tolist())
        
        # Add Non-Region ratings to the dictionary
        all_ratings['region'].extend([region_name] * len(non_region))
        all_ratings['rating'].extend(non_region['rating'].tolist())
        all_ratings['rating_type'].extend(['Non-Region'] * len(non_region))
        all_ratings['user_state'].extend(non_region['user_state'].tolist())

    ratings_df = pd.DataFrame(all_ratings)
    
    return ratings_df