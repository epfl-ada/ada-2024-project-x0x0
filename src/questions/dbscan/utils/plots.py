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



def plot_distributions(US_data, X_scaled):
    
    pca = PCA(n_components=0.95)  #keep 95% of variance
    X_pca = pca.fit_transform(X_scaled)
    X_pca_df = pd.DataFrame(X_pca)
    
    cluster_labels_df = X_scaled[['cluster']].reset_index(drop=True)
    cluster_labels_df['user_id'] = US_data.loc[X_pca_df.index, 'user_id'].values
    cluster_labels_df['beer_id'] = US_data.loc[X_pca_df.index, 'beer_id'].values


    cluster_labels_df = cluster_labels_df.merge(
        US_data[['user_id', 'user_state']].drop_duplicates(),
        on='user_id',
        how='left'
    )

    if 'beer_id' in US_data.columns:
        cluster_labels_df = cluster_labels_df.merge(
            US_data[['beer_id', 'beer_state']].drop_duplicates(),
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
        
    return user_cluster_state_counts.T


def states_in_clusters(user_cluster_state_counts_t):
    
    #where is user_cluster_state_counts_t coming from?
    state_totals = user_cluster_state_counts_t.sum(axis=1)

    normalized_cluster_data = user_cluster_state_counts_t.div(state_totals, axis=0)

    for cluster_label, cluster_data in normalized_cluster_data.items():
        top_states = cluster_data.nlargest(10).index
        print(f"Cluster {cluster_label}: {', '.join(top_states)}")
        
    return normalized_cluster_data


def plot_dbscan_2D_pca(X_scaled, cluster_labels): #cluster labels from dbscan
    
    features = X_scaled.drop('cluster', axis=1)

    pca = PCA(n_components=2, random_state=42)
    principal_components = pca.fit_transform(features)

    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    pca_df['Cluster'] = cluster_labels #ill just keep it like this for now
    #ill ask them how the want to run the wwhole file to see how i integrate all the functions together

    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='PC1', y='PC2',
        hue='Cluster',
        palette='viridis',
        data=pca_df,
        alpha=0.6
    )
    
    plt.title('Clusters Visualized with PCA')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster')
    plt.show()
    explained_variance = pca.explained_variance_ratio_
    print(f'Explained Variance by PC1: {explained_variance[0]:.2f}')
    print(f'Explained Variance by PC2: {explained_variance[1]:.2f}')
    
    return