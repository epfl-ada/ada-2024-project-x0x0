import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px


def perform_clustering(df_pca, states):
    
    kmeans = KMeans(n_clusters=4, random_state=42) #we choose 5 clusters
    df_pca_clusters = kmeans.fit_predict(df_pca)
    
    #crush into 3D for visualisation
    pca_3d = PCA(n_components=3)
    df_pca_3d = pca_3d.fit_transform(df_pca) 

    # Step 2: Create a DataFrame with the PCA components, clusters, and state labels
    df_pca_3d_df = pd.DataFrame(df_pca_3d, columns=['PC1', 'PC2', 'PC3'])
    df_pca_3d_df['Cluster'] = df_pca_clusters  # Add the cluster labels to the DataFrame
    df_pca_3d_df['State'] = states

    # Step 3: Create an interactive 3D scatter plot using Plotly
    fig = px.scatter_3d(df_pca_3d_df, x='PC1', y='PC2', z='PC3', color='Cluster', 
                        title="3D PCA with Clusters", 
                        labels={'State': 'State'},
                        hover_data={'State': True, 'PC1': False, 'PC2': False, 'PC3': False, 'Cluster': False}) 

    # Show the plot
    fig.show()
    
    states_in_clusters = df_pca_3d_df.groupby('Cluster')['State'].apply(list)

    # Print the states in each cluster
    for cluster, states in states_in_clusters.items():
        print(f"Cluster {cluster}: {states}")

    return