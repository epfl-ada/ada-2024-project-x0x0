import pandas as pd

from utils.styleHeatmap import number_of_ratings_heatmap, ratings_heatmap
from utils.simpleWeights import simple_top_style, simple_2nd_top_style
from utils.logWeights import log_top_styles
from utils.drawMap import draw_map


def analyseStyles(state_style_stats):
    
    number_of_ratings_heatmap(state_style_stats)
    ratings_heatmap(state_style_stats)

    simple_top_style(state_style_stats)
    simple_2nd_top_style(state_style_stats)
    top_style_per_state = log_top_styles(state_style_stats)
    
    draw_map(top_style_per_state)
    
    return



if __name__ == "__main__":  
    US_ratings = pd.read_csv('USData/BA_US_states_all.csv')
    print(US_ratings.shape)
    unique_styles = US_ratings['style'].unique()
    print("Number of unique styles :", len(unique_styles))

    state_style_stats = US_ratings.groupby(['user_state', 'style']).agg(average_rating=('rating', 'mean'),nb_ratings=('rating', 'size')).reset_index() #calculating the number of ratings and average ratings per state per beer style
    state_style_stats.head(2)
    
    analyseStyles(state_style_stats)