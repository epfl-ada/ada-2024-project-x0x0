import pandas as pd



def prep_data(US_knn_text : pd.DataFrame):
    
    df_drop = US_knn_text.dropna().reset_index()
    
    df_reduced = df_drop[['style', 'appearance', 'aroma', 'palate',
                             'taste', 'overall', 'avg', 'user_state']]
    
    states = df_reduced['user_state'].unique().tolist()
    states.sort()  #50 states
    
    styles = df_reduced['style'].unique().tolist()
    styles.sort() #103 styles
    
    df_total_clustering = make_feature_df(states, styles, df_reduced)
    
    return df_total_clustering, states
    
    
def calc_features(style, df, tot_number_reviews):
    
    avg_appearance = df['appearance'].mean()
    avg_aroma = df['aroma'].mean()
    avg_palate = df['palate'].mean()
    avg_taste = df['taste'].mean()
    avg_overall = df['overall'].mean()
    avg_rating = df['avg'].mean()
    std_rating = df['avg'].std()
    review_count = df.shape[0]  #normalize gives us percentage wise, which could be a good feature for style preference
    normalized_review_count = review_count / tot_number_reviews
    
    
    df = pd.DataFrame(columns=['avg_appearance', 'avg_aroma', 'avg_palate', 
                                        'avg_taste', 'avg_overall','avg_rating_per_style',
                                        'std_per_style', 'normalised_review_count'])
    
    df.loc[0] = [avg_appearance,avg_aroma,avg_palate,avg_taste,
                 avg_overall,avg_rating,std_rating,normalized_review_count]
    
    df = df.rename(columns=lambda col: style+'_'+col)
    
    return df


def make_feature_df(states, styles, df_reduced):
    
    df_total_clustering = pd.DataFrame()

    for state in states:
        df_state = df_reduced[df_reduced['user_state'] == state]
        
        df_clustering = pd.DataFrame(columns=['user_state'])
        df_clustering.loc[0, 'user_state'] = state

        tot_number_reviews = df_state.shape[0]

        for style in styles:
            df_style = df_state[df_state['style'] == style]
            
            df_features = calc_features(style, df_style, tot_number_reviews)
            
            df_clustering = pd.concat([df_clustering, df_features], axis=1)
        
        df_total_clustering = pd.concat([df_total_clustering, df_clustering], ignore_index=True)

    return df_total_clustering