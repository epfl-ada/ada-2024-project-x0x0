import pandas as pd

def add_country(df_loc, df_no_loc, identifier):
    df_ratings_loc = df_no_loc.merge(df_loc[[identifier, 'location']], on=identifier, how='left')
    
    return df_ratings_loc

def main(data_path):
    ## Define the dtypes of the csv files
    dtype_BAs_beers = {
        'beer_id': 'int64',
        'beer_name': 'string',
        'brewery_id': 'int64',
        'brewery_name': 'string',
        'style': 'string',
        'nbr_ratings': 'int64',
        'avg': 'float64',
    }

    dtype_BAs_breweries = {
        'id': 'int64',
        'location': 'string',
        'name': 'string',
        'nbr_beers': 'int64'
    }

    dtype_BAs_ratings = {
        'beer_name': 'string',
        'beer_id': 'int64',
        'brewery_name': 'string',
        'brewery_id': 'int64',
        'style': 'string',
        'user_id': 'string',    # This is 'user_name' + '.' + 'int64', I put it as a string as it would be easier to modify
        'appearance': 'float64',
        'aroma': 'float64',
        'palate': 'float64',
        'taste': 'float64',
        'overall': 'float64',
        'rating': 'float64',
    }

    dtype_BAs_users = {
        'nbr_ratings': 'int64',
        'user_id': 'string',    # This is 'user_name' + '.' + 'int64', I put it as a string as it would be easier to modify
        'location': 'string'
    }

    dtype_RBs_beers = {
        'beer_id': 'int64',
        'beer_name': 'string',
        'brewery_id': 'int64',
        'brewery_name': 'string',
        'style': 'string',
        'nbr_ratings': 'int64',
        'avg': 'float64',
    }

    dtype_RBs_breweries = {
        'id': 'int64',
        'location': 'string',
        'name': 'string',
        'nbr_beers': 'int64'
    }

    dtype_RBs_ratings = {
        'beer_name': 'string',
        'beer_id': 'int64',
        'brewery_name': 'string',
        'brewery_id': 'int64',
        'style': 'string',
        'user_id': 'string',    # This is 'user_name' + '.' + 'int64', I put it as a string as it would be easier to modify
        'appearance': 'float64',
        'aroma': 'float64',
        'palate': 'float64',
        'taste': 'float64',
        'overall': 'float64',
        'rating': 'float64',
    }

    dtype_RBs_users = {
        'nbr_ratings': 'int64',
        'user_id': 'string',    # This is 'user_name' + '.' + 'int64', I put it as a string as it would be easier to modify
        'location': 'string'
    }


    ## Load all the data
    BAs_beers = pd.read_csv(data_path + 'BA_beers_small.csv', dtype=dtype_BAs_beers)
    BAs_breweries = pd.read_csv(data_path + 'BA_breweries_small.csv', dtype=dtype_BAs_breweries)
    BAs_ratings = pd.read_csv(data_path + 'BA_ratings_small.csv', dtype=dtype_BAs_ratings)
    BAs_users = pd.read_csv(data_path + 'BA_users_small.csv', dtype=dtype_BAs_users)

    RBs_beers = pd.read_csv(data_path + 'RB_beers_small.csv', dtype=dtype_RBs_beers)
    RBs_breweries = pd.read_csv(data_path + 'RB_breweries_small.csv', dtype=dtype_RBs_breweries)
    RBs_ratings = pd.read_csv(data_path + 'RB_ratings_small.csv', dtype=dtype_RBs_ratings)
    RBs_users = pd.read_csv(data_path + 'RB_users_small.csv', dtype=dtype_RBs_users)

    BAs_breweries = BAs_breweries.rename(columns={'id': 'brewery_id'}) # Change the name of the breweries id so that it can be associated to the beers
    RBs_breweries = RBs_breweries.rename(columns={'id': 'brewery_id'}) # Change the name of the breweries id so that it can be associated to the beers

    ## Add locations to countries and beers
    BAs_beers_loc = add_country(df_loc=BAs_breweries, df_no_loc=BAs_beers, identifier='brewery_id') # Add location to each beer
    BAs_ratings_loc = add_country(df_loc=BAs_users, df_no_loc=BAs_ratings, identifier='user_id') # Add location to each rating

    RBs_beers_loc = add_country(df_loc=RBs_breweries, df_no_loc=RBs_beers, identifier='brewery_id') # Add location to each beer
    RBs_ratings_loc = add_country(df_loc=RBs_users, df_no_loc=RBs_ratings, identifier='user_id') # Add location to each rating


    ## Next modify the the location names to avoid confusion between beer_location and rating_location
    BAs_beers_loc = BAs_beers_loc.rename(columns={'location': 'beer_location'})
    BAs_ratings_loc = BAs_ratings_loc.rename(columns={'location': 'user_location'})

    RBs_beers_loc = RBs_beers_loc.rename(columns={'location': 'beer_location'})
    RBs_ratings_loc = RBs_ratings_loc.rename(columns={'location': 'user_location'})


    ## The next step is to merge these two per beer_id so that they can be associated for the rating difference. Un-comment to use.
    BAs_ratbeer = BAs_ratings_loc.merge(BAs_beers_loc[['beer_id', 'avg', 'beer_location']], on='beer_id', how='left')
    RBs_ratbeer = RBs_ratings_loc.merge(RBs_beers_loc[['beer_id', 'avg', 'beer_location']], on='beer_id', how='left')
    return BAs_beers_loc, BAs_ratings_loc, RBs_beers_loc, RBs_ratings_loc, BAs_ratbeer, RBs_ratbeer