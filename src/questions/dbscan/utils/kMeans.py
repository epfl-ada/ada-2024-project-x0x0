import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler

from utils.prepData import prep_data



def k_means(US_data):
    
    x,y = prep_data(US_data)
    
    scaler = RobustScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(x), columns=x.columns)
    
    elbow(X_scaled)
    
    return


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