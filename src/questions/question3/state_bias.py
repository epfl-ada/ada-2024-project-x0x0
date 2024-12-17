import pandas as pd

from utils.weighted_ratings import weighted_ratings
from utils.state_scatter import state_scatter_plot
from utils.state_cohenD import state_cohen_D, state_distribution


def state_bias(US_ratings):
    
    ratings_comparison = weighted_ratings(US_ratings)

    state_scatter_plot(ratings_comparison)

    df_cohenD = state_cohen_D(US_ratings)

    state_distribution(df_cohenD, US_ratings)
    

if __name__ == "__main__":  
    US_ratings = pd.read_csv('USData/BA_US_states_all.csv')
    state_bias(US_ratings)