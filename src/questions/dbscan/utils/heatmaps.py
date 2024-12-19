import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import RobustScaler

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import seaborn as sns
import plotly.express as px
from matplotlib.colors import to_hex


def plot_heatmaps(US_knn_text):
    
    columns_to_drop = ['beer_name', 'beer_id','brewery_name','avg','user_state', 'beer_state', 'text']

    # Drop the specified columns as well as dropping ratings with no text reviews
    X_drop_na = US_knn_text.dropna()
    X_drop = X_drop_na.drop(columns=columns_to_drop)
    y = US_knn_text['user_state']
    
    X = X_drop
    #one hot encode beer style
    #frequency encode brewery_id and user_id

    X = pd.get_dummies(X, columns=['style'], prefix=['style'])
    user_frequency = X['user_id'].value_counts() / len(X)  # Frequency of each user_id

    #Map each user_id to its frequency
    X['user_id_encoded'] = X['user_id'].map(user_frequency)
    brewery_frequency = X['brewery_id'].value_counts() / len(X)  # Frequency of each brewery_id

    #Map each brewery_id to its frequency
    X['brewery_id_encoded'] = X['brewery_id'].map(brewery_frequency)
    X = X.drop(columns=['user_id', 'brewery_id'])

    #label encoding target variable
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    features_to_remove = ['aroma', 'palate', 'overall']
    X = X.drop(columns=features_to_remove)
    
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    X_scaled = X_scaled.dropna()
    
    pca = PCA(n_components=0.95)
    X_pca = pca.fit_transform(X_scaled)
    X_pca_df = pd.DataFrame(X_pca)

    X_scaled.columns = X_scaled.columns.astype(str)
    kmeans = KMeans(n_clusters=6, n_init=50, random_state=42)
    cluster_labels_kmeans = kmeans.fit_predict(X_scaled)
    X_scaled['cluster_Kmeans'] = cluster_labels_kmeans

    X_scaled.columns = X_scaled.columns.astype(str)
    dbscan = DBSCAN(eps=1.0, min_samples=5, n_jobs=-1)
    cluster_labels_DBSCAN = dbscan.fit_predict(X_scaled)
    X_scaled['cluster_DBSCAN'] = cluster_labels_DBSCAN

    cluster_labels_df = X_scaled[['cluster']].reset_index(drop=True)
    #you can use this (down) when the itreative imputer is able to run
    #cluster_labels_df['user_id'] = df['user_id'].values
    #cluster_labels_df['beer_id'] = df['beer_id'].values
    cluster_labels_df['user_id'] = US_knn_text.loc[X_pca_df.index, 'user_id'].values
    cluster_labels_df['beer_id'] = US_knn_text.loc[X_pca_df.index, 'beer_id'].values


    cluster_labels_df = cluster_labels_df.merge(
        US_knn_text[['user_id', 'user_state']].drop_duplicates(),
        on='user_id',
        how='left'
    )

    if 'beer_id' in US_knn_text.columns:
        cluster_labels_df = cluster_labels_df.merge(
            US_knn_text[['beer_id', 'beer_state']].drop_duplicates(),
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
    
    
    features = X_scaled.drop(columns=['cluster_Kmeans', 'cluster_DBSCAN'])
    pca = PCA(n_components=2, random_state=42)
    principal_components = pca.fit_transform(features)
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

    # KMeans PCA Visualization
    pca_df['Cluster'] = X_scaled['cluster_Kmeans']
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='PC1', y='PC2', hue='Cluster', palette='viridis', data=pca_df, alpha=0.6)
    plt.title('Clusters Visualized with PCA (KMeans)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster')
    plt.show()

    # DBSCAN PCA Visualization
    pca_df['Cluster'] = X_scaled['cluster_DBSCAN']
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='PC1', y='PC2', hue='Cluster', palette='tab10', data=pca_df, alpha=0.6, legend = False)
    plt.title('Clusters Visualized with PCA (DBSCAN)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster')
    plt.show()
    
    pio.renderers.default = 'notebook_connected'

    # Load and prepare the us_map as before
    us_map = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")
    us_map.rename(columns={'name': 'state'}, inplace=True)
    us_map['state'] = us_map['state'].str.lower().str.strip()
    us_map = us_map.to_crs(epsg=4326)  # Ensure correct coordinate system

    #======================================
    # FUNCTION TO GET TOP 10 STATES PER CLUSTER
    #======================================
    def get_top_10_states(cluster_column):
        user_cluster_state_counts_t = cluster_labels_df.groupby([cluster_column, 'user_state']).size().unstack(fill_value=0).T
        state_totals = user_cluster_state_counts_t.sum(axis=1)
        normalized_cluster_data = user_cluster_state_counts_t.div(state_totals, axis=0)

        top_10_states_dict = {}
        for cluster_label, cluster_data in normalized_cluster_data.items():
            top_states = cluster_data.nlargest(10).index.tolist()
            top_10_states_dict[cluster_label] = top_states
        return top_10_states_dict

    top_10_states_kmeans = get_top_10_states('cluster_Kmeans')
    top_10_states_kmeans_lower = {
        c_label: [state.lower() for state in states]
        for c_label, states in top_10_states_kmeans.items()
    }

    top_10_states_dbscan = get_top_10_states('cluster_DBSCAN')
    top_10_states_dbscan_lower = {
        c_label: [state.lower() for state in states]
        for c_label, states in top_10_states_dbscan.items()
    }

    #======================================
    # FUNCTION TO PREPARE DATA FOR PLOTTING
    #======================================
    def prepare_plot_data(top_10_dict_lower, us_map):
        all_top_states_map = {}
        for c_label, states in top_10_dict_lower.items():
            for s in states:
                if s not in all_top_states_map:
                    all_top_states_map[s] = c_label

        plot_gdf = us_map.copy()
        plot_gdf['cluster'] = plot_gdf['state'].apply(lambda x: all_top_states_map.get(x, -1))

        unique_clusters = sorted([c for c in plot_gdf['cluster'].unique() if c != -1])
        n_clusters = len(unique_clusters)

        cluster_map = {cl: i+1 for i, cl in enumerate(unique_clusters)}
        cluster_map[-1] = 0
        plot_gdf['cluster_idx'] = plot_gdf['cluster'].map(cluster_map)
        return plot_gdf, n_clusters

    def plot_with_insets(plot_gdf, n_clusters, title):
        if 'cluster_idx' not in plot_gdf.columns:
            raise KeyError("The 'cluster_idx' column is missing from the GeoDataFrame. Ensure the data preparation step is correct.")

        colors = ['white'] + [to_hex(c) for c in sns.color_palette('husl', n_clusters)]

        color_mapping = {idx: colors[idx] for idx in range(n_clusters + 1)}

        plot_gdf['color'] = plot_gdf['cluster_idx'].map(color_mapping)

        print(plot_gdf[['state', 'cluster_idx', 'color']].head())

        mainland = plot_gdf[~plot_gdf['state'].isin(['alaska', 'hawaii'])]
        alaska = plot_gdf[plot_gdf['state'] == 'alaska'].copy()
        hawaii = plot_gdf[plot_gdf['state'] == 'hawaii'].copy()

        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        mainland.plot(color=mainland['color'], edgecolor='black', ax=ax)
        ax.set_title(title, fontsize=16)
        ax.axis('off')

        if not alaska.empty:
            alaska['geometry'] = alaska['geometry'].scale(0.35, 0.35, origin=(0, 0)).translate(xoff=-35, yoff=-15)

            alaska_ax = fig.add_axes([0.1, 0.1, 0.25, 0.25])  # [x, y, width, height]
            alaska.plot(color=alaska['color'], edgecolor='black', ax=alaska_ax)
            alaska_ax.set_title("Alaska", fontsize=10)
            alaska_ax.axis('off')

        if not hawaii.empty:
            hawaii['geometry'] = hawaii['geometry'].scale(0.7, 0.7, origin=(0, 0)).translate(xoff=50, yoff=-20)

            hawaii_ax = fig.add_axes([0.3, 0.05, 0.2, 0.2])  # [x, y, width, height]
            hawaii.plot(color=hawaii['color'], edgecolor='black', ax=hawaii_ax)
            hawaii_ax.set_title("Hawaii", fontsize=10)
            hawaii_ax.axis('off')

        plt.show()
        
    #======================================
    # FUNCTION TO PLOT USING PLOTLY
    #======================================
    def plot_static_map(plot_gdf, n_clusters, title):
        colors = ['white'] + [to_hex(c) for c in sns.color_palette('husl', n_clusters)]

        color_mapping = {idx: colors[idx] for idx in range(n_clusters + 1)}

        plot_gdf['color'] = plot_gdf['cluster_idx'].map(color_mapping)

        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        plot_gdf.plot(color=plot_gdf['color'], edgecolor='black', ax=ax)
        ax.set_title(title, fontsize=16)
        ax.axis('off')  # Remove axes for a clean map
        plt.show()

    #======================================
    # CREATE A SINGLE MAP FOR ALL KMEANS and DBSCAN CLUSTERS
    #======================================
    plot_gdf, n_clusters = prepare_plot_data(top_10_states_kmeans_lower, us_map)
    plot_with_insets(plot_gdf, n_clusters, "Top 10 States for All KMeans Clusters on One Map")

    # Prepare plot data for DBSCAN
    plot_gdf, n_clusters = prepare_plot_data(top_10_states_dbscan_lower, us_map)
    plot_with_insets(plot_gdf, n_clusters, "Top 10 States for All DBSCAN Clusters on One Map")
    
    return