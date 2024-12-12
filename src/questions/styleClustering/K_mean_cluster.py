import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from src.questions.styleClustering.utils.prepData import prep_data
from src.questions.styleClustering.utils.PCA import perform_PCA

def run_clustering(US_knn_text):
    
    df_total_clustering, states = prep_data(US_knn_text)
    
    df_pca = perform_PCA(df_total_clustering, var_threshold=0.95)
    
    
    
    
    return
    
    
    
if __name__ == "__main__":   
    pass