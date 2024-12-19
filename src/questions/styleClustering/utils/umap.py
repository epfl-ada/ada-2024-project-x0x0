import pandas as pd
import umap
from sklearn.cluster import DBSCAN
import os
import plotly.express as px


def perform_umap(df_total_clustering):

    df_total_clustering_cleaned = df_total_clustering.drop(columns=['user_state'])

    print(df_total_clustering_cleaned.shape)
    df_cleaned = df_total_clustering_cleaned.fillna(0)

    umap_3d = umap.UMAP(n_components=3, random_state=42)
    embedding_3d = umap_3d.fit_transform(df_cleaned)

    dbscan = DBSCAN(eps=0.65, min_samples=3)
    dbscan_labels = dbscan.fit_predict(embedding_3d)

    df_cleaned['Cluster'] = dbscan_labels
    df_cleaned['user_state'] = df_total_clustering['user_state']

    #Define a consistent color map for clusters
    cluster_color_map = {
        '0': '#5b8a72',  
        '1': '#4f0205',  
        '2': '#a46e51', 
        '3': '#6e6456', 
        '4': '#dd660d', 
        '5': '#3d5d44' 
    }
    df_cleaned['Cluster'] = df_cleaned['Cluster'].astype(str)

    # Plot the 3D UMAP with Plotly
    fig = px.scatter_3d(
        df_cleaned,
        x=embedding_3d[:, 0],
        y=embedding_3d[:, 1],
        z=embedding_3d[:, 2],
        title="DBSCAN Clustering on UMAP",
        labels={'Cluster': 'Cluster Label'},
        hover_data={'user_state': True, 'Cluster': True},  # Show state and cluster on hover
        color='Cluster',
        color_discrete_map=cluster_color_map
    )

    fig.show()
    directory = 'img/question4/'
    fig.write_html(os.path.join(directory, "dbscan_clustering_on_umap.html"))

    return df_cleaned

