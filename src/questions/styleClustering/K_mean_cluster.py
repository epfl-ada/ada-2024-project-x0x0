import pandas as pd

from src.questions.styleClustering.utils.prepData import prep_data
from src.questions.styleClustering.utils.PCA import perform_PCA
from src.questions.styleClustering.utils.cluster import perform_clustering
from src.questions.styleClustering.utils.umap import perform_umap
from src.questions.styleClustering.utils.umapMap import draw_umap_map



def run_clustering(US_knn_text):
    
    df_total_clustering, states = prep_data(US_knn_text)
    
    df_pca = perform_PCA(df_total_clustering, var_threshold=0.95)
    
    perform_clustering(df_pca, states)
    
    return
    
def umap_clustering(US_knn_text):
    
    df_total_clustering, states = prep_data(US_knn_text)
    
    df_cleaned = perform_umap(df_total_clustering)
    
    draw_umap_map(df_cleaned)
    
    return
    
if __name__ == "__main__":   
    BA_US_knn_text = pd.read_csv('knnData/BA_US_knn_text.csv')