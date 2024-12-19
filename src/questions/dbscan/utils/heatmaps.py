import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



def plot_heatmaps(X_pca_df, X_scaled, df):

    cluster_labels_df = X_scaled[['cluster']].reset_index(drop=True)
    #you can use this (down) when the itreative imputer is able to run
    #cluster_labels_df['user_id'] = df['user_id'].values
    #cluster_labels_df['beer_id'] = df['beer_id'].values
    cluster_labels_df['user_id'] = df.loc[X_pca_df.index, 'user_id'].values
    cluster_labels_df['beer_id'] = df.loc[X_pca_df.index, 'beer_id'].values


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