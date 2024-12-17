import pandas as pd



def prep_data(US_knn_text):
    
    #we have more than enough data, so we can afford to just drop all instances of NaNs
    X_drop_na = US_knn_text.dropna() #still have 1.8 mill data points... largely enough

    X_drop = X_drop_na.drop(columns = ['beer_name', 'beer_id','brewery_name',
                                       'avg','user_state', 'beer_state', 'text'])
    y = X_drop['user_state']
    
    return X_drop, y
    
