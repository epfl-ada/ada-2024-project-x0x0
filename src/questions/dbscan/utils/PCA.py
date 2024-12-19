import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import RobustScaler



def plot_vars(US_knn_text):
    
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


    # Create a DataFrame of the PCA components
    # Each column represents a principal component and each row corresponds to the feature contribution to that component
    components_df = pd.DataFrame(pca.components_, columns=X_scaled.columns)
    
    plt.figure(figsize=(8, 6))
    sns.lineplot(x=range(1, len(pca.explained_variance_ratio_) + 1),
                y=pca.explained_variance_ratio_, marker='o')
    plt.title('Explained Variance by Each Principal Component')
    plt.xlabel('Principal Components')
    plt.ylabel('Explained Variance Ratio')
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.lineplot(x=range(1, len(pca.explained_variance_ratio_) + 1),
                y=np.cumsum(pca.explained_variance_ratio_), marker='o')
    plt.title('Cumulative Explained Variance')
    plt.xlabel('Principal Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.show()
    
    return X_pca_df, X_scaled




def PCA_visualise(X_scaled):
    
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
    
    return