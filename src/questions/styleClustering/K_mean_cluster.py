import pandas as pd

from utils.prepData import prep_data
from utils.PCA import perform_PCA
from utils.cluster import perform_clustering

def run_clustering(US_knn_text):
    
    df_total_clustering, states = prep_data(US_knn_text)
    
    df_pca = perform_PCA(df_total_clustering, var_threshold=0.95)
    
    perform_clustering(df_pca, states)
    
    return
    
    
    
if __name__ == "__main__":   
    BA_US_knn_text = pd.read_csv('knnData/BA_US_knn_text.csv')