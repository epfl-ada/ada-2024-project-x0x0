import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler

from utils.prepData import prep_data
from utils.plots import plot_distributions, plot_dbscan_2D_pca, states_in_clusters
from utils.map import draw_map


def k_means(X_scaled):
    
    optimal_k = 5
    kmeans = KMeans(n_clusters=optimal_k, n_init=50, random_state=42)
    cluster_labels = kmeans.fit_predict(X_scaled)
    X_scaled['cluster'] = cluster_labels
    
    return X_scaled, cluster_labels


def elbow(X_scaled):
    
    inertia = []
    K_range = range(2, 15)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(8, 4))
    plt.plot(K_range, inertia, 'bx-')
    plt.xlabel('Number of clusters K')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K')
    plt.show()
    
    return


def k_means_pipeline(US_data):
    
    x,y = prep_data(US_data)
    
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(x), columns=x.columns)
    
    X_scaled_plus, cluster_labels = k_means(X_scaled)
    
    #elbow(X_scaled)
    
    user_cluster_state_counts_t = plot_distributions(US_data, X_scaled_plus)
    
    normalized_cluster_data = states_in_clusters(user_cluster_state_counts_t)
    
    plot_dbscan_2D_pca(X_scaled_plus, cluster_labels)
    
    draw_map(normalized_cluster_data)
    
    