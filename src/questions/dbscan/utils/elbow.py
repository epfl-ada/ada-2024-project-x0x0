import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler



def elbow_epsilon(X_pca_df):
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_pca_df), columns=X_pca_df.columns)

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

    #DBSCAN
    X_subset = X_scaled.sample(frac=0.1, random_state=42)  # Use 10% of the data

    from sklearn.neighbors import NearestNeighbors

    neighbors = NearestNeighbors(n_neighbors=10)
    neighbors_fit = neighbors.fit(X_subset)
    distances, indices = neighbors_fit.kneighbors(X_subset)

    distances = np.sort(distances[:, -1])
    plt.plot(distances)
    plt.title("Optimal Epsilon Plot")
    plt.xlabel("Points")
    plt.ylabel("Distance")
    plt.show()
    
    return