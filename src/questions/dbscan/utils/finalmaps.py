import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
import plotly.express as px
import geopandas as gpd
import ipywidgets as widgets
from IPython.display import display
import plotly.io as pio
from matplotlib.colors import to_hex



def KNN_plots(df, X_pca_df):

    scaler = RobustScaler()
    
    X_scaled = pd.DataFrame(scaler.fit_transform(X_pca_df), columns=X_pca_df.columns)


    #======================================
    #K MEANS CLUSTERING
    #======================================
    optimal_k = 6
    X_scaled.columns = X_scaled.columns.astype(str)
    kmeans = KMeans(n_clusters=optimal_k, n_init=50, random_state=42)
    cluster_labels_kmeans = kmeans.fit_predict(X_scaled)
    X_scaled['cluster_Kmeans'] = cluster_labels_kmeans

    print("Starting dbscan")
    #======================================
    #DBSCAN
    #======================================
    X_scaled.columns = X_scaled.columns.astype(str)
    dbscan = DBSCAN(eps=1.0, min_samples=5, n_jobs=-1)
    cluster_labels_DBSCAN = dbscan.fit_predict(X_scaled)
    X_scaled['cluster_DBSCAN'] = cluster_labels_DBSCAN

    print("Finished dbscan")

    cluster_labels_df = X_scaled[['cluster_Kmeans', 'cluster_DBSCAN']].reset_index(drop=True)
    cluster_labels_df['user_id'] = df.loc[X_pca_df.index, 'user_id'].values
    cluster_labels_df['beer_id'] = df.loc[X_pca_df.index, 'beer_id'].values

    cluster_labels_df = cluster_labels_df.merge(df[['user_id', 'user_state']].drop_duplicates(), on='user_id', how='left')
    if 'beer_id' in df.columns:
        cluster_labels_df = cluster_labels_df.merge(df[['beer_id', 'beer_state']].drop_duplicates(), on='beer_id', how='left')


    def plot_heatmap(cluster_column, title, cmap):
        user_cluster_state_counts = cluster_labels_df.groupby([cluster_column, 'user_state']).size().unstack(fill_value=0)
        plt.figure(figsize=(12, 6))
        sns.heatmap(user_cluster_state_counts, annot=False, fmt='d', cmap=cmap)
        plt.title(title)
        plt.xlabel('User State')
        plt.ylabel('Cluster')
        plt.show()

    plot_heatmap('cluster_Kmeans', 'User Distribution by KMeans Cluster and State', 'Blues')

    plot_heatmap('cluster_DBSCAN', 'User Distribution by DBSCAN Cluster and State', 'Greens')


    #======================================
    # PCA VISUALIZATION FOR BOTH CLUSTERS
    #======================================
    features = X_scaled.drop(columns=['cluster_Kmeans', 'cluster_DBSCAN'])
    pca = PCA(n_components=2, random_state=42)
    principal_components = pca.fit_transform(features)
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

    pca_df['Cluster'] = X_scaled['cluster_Kmeans']
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='PC1', y='PC2', hue='Cluster', palette='viridis', data=pca_df, alpha=0.6)
    plt.title('Clusters Visualized with PCA (KMeans)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster')
    plt.show()

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
    # CREATE A SINGLE MAP FOR ALL KMEANS and DBSCAN CLUSTERS
    #======================================
    plot_gdf, n_clusters = prepare_plot_data(top_10_states_kmeans_lower, us_map)
    plot_with_insets(plot_gdf, n_clusters, "Top 10 States for All KMeans Clusters on One Map")

    # Prepare plot data for DBSCAN
    plot_gdf, n_clusters = prepare_plot_data(top_10_states_dbscan_lower, us_map)
    plot_with_insets(plot_gdf, n_clusters, "Top 10 States for All DBSCAN Clusters on One Map")

    return



def clustering_and_visualization(df, X_pca_df, k_range=range(3, 11)):
    """
    Perform clustering with KMeans, and visualize the results using interactive maps for each k.
    
    Args:
        df (pd.DataFrame): Original dataset with user and beer data.
        X_pca_df (pd.DataFrame): Scaled feature set for clustering.
        k_range (range): Range of 'k' values for KMeans to try.
    """
    # Prepare the map
    us_map = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")
    us_map.rename(columns={'name': 'state'}, inplace=True)
    us_map['state'] = us_map['state'].str.lower().str.strip()
    us_map = us_map.to_crs(epsg=4326)  # Ensure correct coordinate system
    
    # Scale data
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_pca_df), columns=X_pca_df.columns)
    
    # Initialize variables
    top_states_k = []
    top_features_k = {}
    state_cluster_fractions = {}
    
    # Perform clustering for each k in the specified range
    for k in k_range:
        X_scaled_copy = X_scaled.copy()
        X_scaled_copy.columns = X_scaled_copy.columns.astype(str)
        kmeans = KMeans(n_clusters=k, n_init=50, random_state=42)
        cluster_labels_kmeans = kmeans.fit_predict(X_scaled_copy)
        X_scaled_copy['cluster_Kmeans'] = cluster_labels_kmeans
        
        cluster_labels_df = pd.DataFrame({'cluster_Kmeans': cluster_labels_kmeans})
        cluster_labels_df['user_id'] = df.loc[X_pca_df.index, 'user_id'].values
        cluster_labels_df['beer_id'] = df.loc[X_pca_df.index, 'beer_id'].values

        cluster_labels_df = cluster_labels_df.merge(df[['user_id', 'user_state']].drop_duplicates(), on='user_id', how='left')
        if 'beer_id' in df.columns:
            cluster_labels_df = cluster_labels_df.merge(df[['beer_id', 'beer_state']].drop_duplicates(), on='beer_id', how='left')

        user_cluster_state_counts = cluster_labels_df.groupby(['cluster_Kmeans', 'user_state']).size().unstack(fill_value=0)
        user_cluster_state_counts_t = cluster_labels_df.groupby(['cluster_Kmeans', 'user_state']).size().unstack(fill_value=0).T
        state_totals = user_cluster_state_counts_t.sum(axis=1)
        normalized_cluster_data = user_cluster_state_counts_t.div(state_totals, axis=0)
        state_cluster_fractions[k] = normalized_cluster_data.copy()

        for cluster_label, cluster_data in normalized_cluster_data.items():
            top_states = cluster_data.nlargest(10).index
            top_states_k.append((k, cluster_label, list(top_states)))

        # Extract top features for each cluster
        cluster_centers = kmeans.cluster_centers_
        feature_names = X_scaled_copy.columns
        top_features_per_cluster = {}
        for cluster_num in range(k):
            centroid = cluster_centers[cluster_num]
            top_n = 5  
            top_feature_indices = np.argsort(np.abs(centroid))[::-1][:top_n]
            top_feature_names = [feature_names[i] for i in top_feature_indices]
            top_features_per_cluster[cluster_num] = top_feature_names
        top_features_k[k] = top_features_per_cluster

    # Restructure top_states_k
    top_states_dict = {}
    for k, cluster_label, states in top_states_k:
        if k not in top_states_dict:
            top_states_dict[k] = {}
        top_states_dict[k][cluster_label] = [state.lower() for state in states]
    
    # Define the Color Palette
    color_palette = ['#dd660d', '#4f0205', '#a46e51', '#6e6456', '#5b8a72', '#3d5d44',  '#ff920d', '#7a5429', '#5f3f36', '#d1a85c', '#8f6b3e', '#a7b35c', '#be9c69']
    max_clusters = max(len(clusters) for clusters in top_states_dict.values())
    if max_clusters > len(color_palette):
        additional_colors = px.colors.qualitative.Alphabet
        color_palette += additional_colors[:max_clusters - len(color_palette)]

    # Create interactive widgets
    output = widgets.Output()
    k_slider = widgets.IntSlider(
        value=3, min=3, max=10, step=1, description='k:', continuous_update=False
    )

    # Define the Update Function
    def update_map(k):
        with output:
            output.clear_output(wait=True)
            
            cluster_to_states = top_states_dict.get(k, {})
            sorted_clusters = sorted(cluster_to_states.keys())
            
            color_discrete_map = {}
            for i, cluster in enumerate(sorted_clusters):
                color_discrete_map[f'Cluster {cluster}'] = color_palette[i % len(color_palette)]
            color_discrete_map['No Cluster'] = 'white'

            us_map['cluster'] = 'No Cluster'
            for cluster, states in cluster_to_states.items():
                us_map.loc[us_map['state'].isin(states), 'cluster'] = f'Cluster {cluster}'
            
            us_map['state_cap'] = us_map['state'].str.title()
            us_map['name'] = us_map['state_cap']
            
            # Adding percentages
            fractions_df = state_cluster_fractions[k].copy()
            if isinstance(fractions_df.columns, pd.MultiIndex):
                fractions_df.columns = fractions_df.columns.droplevel(0)
            fractions_df = fractions_df.reset_index()
            fractions_df['user_state_cap'] = fractions_df['user_state'].str.title()
            cluster_cols = [c for c in fractions_df.columns if c not in ['user_state', 'user_state_cap']]
            for c in cluster_cols:
                fractions_df[c] = fractions_df[c] * 100.0  
            
            renamed_cols = {c: f"Cluster {c} (%)" for c in cluster_cols}
            fractions_df.rename(columns=renamed_cols, inplace=True)
            merged = us_map.merge(fractions_df, left_on='state_cap', right_on='user_state_cap', how='left')
            hover_data = {col: ':.2f' for col in renamed_cols.values()}
            
            fig = px.choropleth(
                merged,
                geojson=merged.__geo_interface__,
                locations='name',
                color='cluster',
                hover_name='name',
                hover_data=hover_data,
                scope="usa",
                color_discrete_map=color_discrete_map,
                featureidkey="properties.name"
            )

            fig.update_geos(
                scope="usa", 
                center=dict(lat=37.0902, lon=-95.7129),  
                projection_scale=1.0,  
                visible=False
            )

            fig.update_layout(
                margin={"r":0,"t":30,"l":0,"b":0},
                legend_title="Clusters",
                title_text=f"Top 10 States per Cluster for k={k}",
                title_x=0.5
            )
            
            fig.show()

    # Link the slider to the update function
    def on_k_change(change):
        if change['name'] == 'value':
            update_map(change['new'])

    k_slider.observe(on_k_change, names='value')

    # Display widgets and initial map
    display(k_slider, output)
    update_map(k_slider.value)
    
    return
