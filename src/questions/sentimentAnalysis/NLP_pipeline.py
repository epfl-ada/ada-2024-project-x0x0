from utils.sentimentAnalysis import sentiment_analysis_results
from utils.NLP_chi_test import NLP_chi_test, plot_chi_results, plot_stacked_sentiments
from utils.NLP_cohenD import NLP_cohen_D_all_states
import pandas as pd
import numpy as np
import os
import gzip
import pickle

def NLP_pipeline(US_ratings):
    
    print("Running... takes 2 hours ish")
    
    df_reduced = US_ratings[['text','user_state','beer_state']]
    states = df_reduced['user_state'].unique().tolist()
    states.sort()
    
    for state in states:
        print(state)
        _, _ = sentiment_analysis_results(state, df_reduced)

    return

def NLP_results_analysis(US_ratings):
    
    df_reduced = US_ratings[['text','user_state','beer_state']]
    states = df_reduced['user_state'].unique().tolist()
    states.sort()
    
    significance = pd.DataFrame(columns=['state', 'chi2', 'p_value', 'cramers_v'])
    local_percents = pd.DataFrame(columns=['state', 'sentences', 'percentage', 'Local/Nonlocal'])
    nonlocal_percents = pd.DataFrame(columns=['state', 'sentences', 'percentage'])
    
    for state in states:
        df = pd.read_csv('NLP_results/'+state+'_sentimentAnalysis.csv')
        df_local = df[df['Local/Nonlocal'] == 'Local']
        df_nonlocal = df[df['Local/Nonlocal'] == 'Nonlocal']
        
        chi2, p , cramers_v = NLP_chi_test(df_local, df_nonlocal, state)
        significance.loc[len(significance)] = [state, chi2, p, cramers_v]
        
        df_local = df_local[df_local['sentences']!='total']
        df_nonlocal = df_nonlocal[df_nonlocal['sentences']!='total']
        df_local = df_local[['sentences', 'percentage', 'Local/Nonlocal']]
        df_nonlocal = df_nonlocal[['sentences', 'percentage', 'Local/Nonlocal']]
        df_local.insert(0, 'state', state) #insert so i can put it on the left
        df_nonlocal.insert(0, 'state', state)
        
        local_percents = pd.concat([local_percents, df_local], ignore_index=True)
        nonlocal_percents = pd.concat([nonlocal_percents, df_nonlocal], ignore_index=True)
        
    plot_stacked_sentiments(local_percents, nonlocal_percents)
    plot_chi_results(significance)
    NLP_cohen_D_all_states(states)

    return

if __name__ == "__main__":   
    print("Importing...")
    BA_US_knn_text = pd.read_csv('knnData/BA_US_knn_text.csv')
    #NLP_pipeline(BA_US_knn_text)
    NLP_results_analysis
