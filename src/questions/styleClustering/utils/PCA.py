import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



def prep_PCA_data(df_total_clustering):
    df_cleaned_drop = df_total_clustering.drop(columns='user_state', axis=1)
    
    #sometimes we get NaN values when we have 0 reviews for a style
    #we don't want to fill with 0s because that can mess up the analysis
    #so the best we can do is fill with the mean to preserve the size of the df
    df_cleaned = df_cleaned_drop.fillna(df_cleaned_drop.mean())
    print(df_cleaned.shape)
    df_cleaned = df_cleaned.dropna(axis=1) #for some reason theres one row in RB thats NaNs, so we drop it
    print(df_cleaned.shape)
    return df_cleaned


def perform_PCA(df_total_clustering, var_threshold, plot=True):
    
    df_cleaned = prep_PCA_data(df_total_clustering)
    
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_cleaned) #PCA likes std data
    
    pca = PCA()
    pca.fit(df_scaled)
    
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = explained_variance.cumsum()
    
    if plot:
        plt.figure(figsize=(10, 6))

        plt.subplot(1, 2, 1)
        plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='-', color='b')
        plt.title('Explained Variance of Each Principal Component')
        plt.xlabel('Principal Component')
        plt.ylabel('Explained Variance')
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='-', color='g')
        plt.title('Cumulative Explained Variance')
        plt.xlabel('Number of Principal Components')
        plt.ylabel('Cumulative Variance Explained')
        plt.grid(True)

        plt.tight_layout()
        plt.show()
        
    n_components = next(i for i, cum_var in enumerate(cumulative_variance) if cum_var >= var_threshold) + 1
    #n_components_90 = next(i for i, cum_var in enumerate(cumulative_variance) if cum_var >= 0.9) + 1

    pca = PCA(n_components=n_components)
    df_pca = pca.fit_transform(df_scaled)
    
    # Create a DataFrame for feature importance in the principal components
    feature_names = df_cleaned.columns
    pc_feature_importance = pd.DataFrame(
        pca.components_.T,
        index=feature_names,
        columns=[f'PC{i+1}' for i in range(n_components)]
    )

    # Create a dictionary to store sorted features for each principal component
    sorted_importance = {}
    for pc in pc_feature_importance.columns:
        sorted_importance[pc] = pc_feature_importance[pc].abs().sort_values(ascending=False)

    # Print the sorted importance directly
    for pc, importance in sorted_importance.items():
        print(f"Top features for {pc}:")
        print(importance)
        print()
    
    return df_pca
