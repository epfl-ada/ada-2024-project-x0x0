import pandas as pd

from utils.prepData import prep_data
from utils.basicPlots import region_avg_scatter, region_avg_violin, plot_cohenD
from utils.buildGroups import build_groups
from utils.map import draw_map



def regional_analysis(US_ratings, neighbours_df, plot = False):
    
    ratings_df = prep_data(US_ratings, neighbours_df)
    
    #region_avg_scatter(ratings_df)
    #region_avg_violin(ratings_df)
    
    final_cohen_df = plot_cohenD(ratings_df, plot)
    
    state_groups = build_groups(final_cohen_df)
    
    draw_map(state_groups, final_cohen_df)
    
    state_groups_df = pd.DataFrame(state_groups)

    return state_groups_df
    
    
    
if __name__ == "__main__":  
    
    US_ratings = pd.read_csv('USData/BA_US_states_all.csv')

    #csv file containing all the states and their neighbouring states
    #empty list for states that have no neighbours (e.g Alazka, Hawaii)
    neighbours_df = pd.read_csv('additionalData/bordering_states.csv', dtype={'state':'string', 
                                                                            'neighbours': 'string'})
    
    regional_analysis(US_ratings, neighbours_df)