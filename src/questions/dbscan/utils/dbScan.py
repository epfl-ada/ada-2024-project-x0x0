import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN

from utils.prepData import prep_data



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

    cluster_labels_df = cluster_labels_df.merge(
        df[['user_id', 'user_state']].drop_duplicates(),
        on='user_id',
        how='left'
    )

    if 'beer_id' in df.columns:
        cluster_labels_df = cluster_labels_df.merge(
            df[['beer_id', 'beer_state']].drop_duplicates(),
            on='beer_id',
            how='left'
        )

    user_cluster_state_counts = cluster_labels_df.groupby(['cluster', 'user_state']).size().unstack(fill_value=0)

    if 'beer_state' in cluster_labels_df.columns:
        beer_cluster_state_counts = cluster_labels_df.groupby(['cluster', 'beer_state']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 6))
    sns.heatmap(user_cluster_state_counts, annot=False, fmt='d', cmap='Blues')
    plt.title('User Distribution by Cluster and State')
    plt.xlabel('user state')
    plt.ylabel('Cluster')
    plt.show()

    if 'beer_state' in cluster_labels_df.columns:
        plt.figure(figsize=(12, 6))
        sns.heatmap(beer_cluster_state_counts, annot=False, fmt='d', cmap='Greens')
        plt.title('Beer Distribution by Cluster and State')
        plt.xlabel('Beer State')
        plt.ylabel('Cluster')
        plt.show()
    
    return
