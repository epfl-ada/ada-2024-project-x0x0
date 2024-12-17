import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import seaborn as sns

from utils.prepData import prep_data
from utils.plots import plot_dbscan_2D_pca, plot_distributions, states_in_clusters



def epsilon_test(US_data):
    
    x,y = prep_data(US_data)
    
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(x), columns=x.columns)
    
    X_subset = X_scaled.sample(frac=0.1, random_state=42)  # Use 10% of the data

    neighbors = NearestNeighbors(n_neighbors=10)
    neighbors_fit = neighbors.fit(X_subset)
    distances, indices = neighbors_fit.kneighbors(X_subset)

    distances = np.sort(distances[:, -1])
    
    plt.plot(distances)
    plt.title("Optimal Epsilon Plot")
    plt.xlabel("Points")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.show()
    
    return


def dbscan(US_data):
    
    x,y = prep_data(US_data)
    
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(x), columns=x.columns)
    
    dbscan = DBSCAN(eps=1.5, min_samples=5, n_jobs=-1)  
    cluster_labels = dbscan.fit_predict(X_scaled)
    X_scaled['cluster'] = cluster_labels

    return  X_scaled, cluster_labels


def dbscan_pipeline(US_data):
    
    x,y = prep_data(US_data)
    
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(x), columns=x.columns)
    
    X_scaled_plus, cluster_labels = dbscan(X_scaled)
    
    #elbow(X_scaled)
    
    user_cluster_state_counts_t = plot_distributions(US_data, X_scaled_plus)
    
    states_in_clusters(user_cluster_state_counts_t)
    
    plot_dbscan_2D_pca(X_scaled_plus, cluster_labels)
