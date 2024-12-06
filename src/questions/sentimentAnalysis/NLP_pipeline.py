from utils.prepNLP import prepare_state_data, create_nlp_doc
from utils.sentimentAnalysis import sentiment_analysis, sentiment_analysis_stats
import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np
import os


def sentiment_analysis_results(state = str, baseData  = pd.DataFrame, save_dfs = True, plots = False):
    print("Running...")
    #formatting our df based on input state
    df_local, df_nonlocal = prepare_state_data(state, baseData)
    
    #turning text into spacy objects, this can take a while...
    docs_local = create_nlp_doc(df_local)
    docs_nonlocal = create_nlp_doc(df_nonlocal)
    
    #turning into sentences and analysing postive/negative sentiment
    #use plots = True if you want to see some plots
    sentences_local = sentiment_analysis(docs_local, state)
    sentences_nonlocal = sentiment_analysis(docs_nonlocal, state)
    
    #basic stats based on the analysis
    df_stats_local = sentiment_analysis_stats(sentences_local)
    df_stats_nonlocal = sentiment_analysis_stats(sentences_nonlocal)
    
    if save_dfs:  #these dfs took a lot of computation to get! Lets save them!
        df_save_local = df_stats_local
        df_save_local['Local/Nonlocal'] = 'Local'
        df_save_local['user_state_NLP'] = state
        
        df_save_nonlocal = df_stats_nonlocal
        df_save_nonlocal['Local/Nonlocal'] = 'Nonlocal'
        df_save_nonlocal['user_state_NLP'] = state
        
        df_combined = pd.concat([df_save_local, df_save_nonlocal], ignore_index=True)
        #'src/questions/sentimentAnalysis/NLP_results/' if running the py file directly
        path = 'NLP_results/'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        path = path + state + '_sentimentAnalysis.csv'
        df_combined.to_csv(path, index=False)
        print("Saved!")
    
    return df_stats_local, df_stats_nonlocal
    
#seperating this function so i can run it just based off of saved csv data
def NLP_chi_test(df_stats_local, df_stats_nonlocal):
    
    #should i just make it output np arrays in the first place...?
    local_counts = df_stats_local[df_stats_local['sentences'] != 'total']['count'].values
    nonlocal_counts = df_stats_nonlocal[df_stats_nonlocal['sentences'] != 'total']['count'].values
    contingency_table = np.array([local_counts, nonlocal_counts])
    
    #chi-square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    print(f"Chi-Square Statistic: {chi2}")
    print(f"P-value: {p}")
    if p < 0.05:
        print("The populations are significantly different.")
    else:
        print("No significant difference between the populations.")


if __name__ == "__main__":   
    print("Importing...")
    BA_US_knn_text = pd.read_csv('knnData/BA_US_knn_text.csv')
    df_reduced = BA_US_knn_text[['text','user_state','beer_state']]
    df_local, df_nonlocal = sentiment_analysis_results('Hawaii', df_reduced)
    NLP_chi_test(df_local, df_nonlocal)
