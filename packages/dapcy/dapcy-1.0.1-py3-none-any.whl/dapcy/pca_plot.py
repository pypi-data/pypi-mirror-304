import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder, normalize

def plot_pca(X, y, title='PCA Projection', n_components=2, n_svd_components=10):
    """
    This function performs Truncated SVD on the dataset, normalizes the data,
    and plots the result in 2D.
    """
    # Encode labels to ensure they are in a suitable format for coloring
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    labels = label_encoder.classes_

    # Normalize the input data
    X_scaled = normalize(X, norm="l2", axis=1)

    # Perform Truncated SVD with specified number of components
    svd = TruncatedSVD(n_components=n_svd_components)
    X_reduced = svd.fit_transform(X_scaled)

    # Prepare DataFrame for Seaborn plotting
    df = pd.DataFrame(X_reduced, columns=[f'Component {i+1}' for i in range(n_svd_components)])
    df['Class'] = label_encoder.inverse_transform(y_encoded)

    # Calculate explained variance for the first two components
    explained_variance = svd.explained_variance_ratio_
    component_1_var = explained_variance[0] * 100
    component_2_var = explained_variance[1] * 100

    # Plotting the 2D projection using Seaborn
    plt.figure(figsize=(8, 6))
    scatter = sns.scatterplot(data=df, x='Component 1', y='Component 2', hue='Class',
                              palette='Spectral', s=60, edgecolor='k', legend='full')

    scatter.legend(loc='upper right', ncol=2, title="Class", bbox_to_anchor=(1.5, 1))
    plt.title(title)
    
    #plt.xlabel(f'Component 1 ({component_1_var:.2f}% Variance)')
    #plt.ylabel(f'Component 2 ({component_2_var:.2f}% Variance)')
    
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True)
    plt.show()
    
def plot_cumulative_variance(X, title ='Cumulative Variance Explained by Principal Components', n_components=10):
    """
    This function plots the number of principal components retained vs. cumulative variance explained.
    """
    svd = TruncatedSVD(n_components=n_components)
    svd.fit(X)
    cumulative_variance = svd.explained_variance_ratio_.cumsum()
    
    total_variance = cumulative_variance[-1] * 100 

    # Prepare DataFrame for Seaborn plotting
    df_variance = pd.DataFrame({
        'Number of Principal Components': range(1, n_components + 1),
        'Cumulative Variance Explained': cumulative_variance
    })

    # Plotting using Seaborn
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=df_variance, x='Number of Principal Components', y='Cumulative Variance Explained', marker='o')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Variance Explained')
    plt.title(f"{title} (Total Variance: {total_variance:.2f}%)")
    plt.grid(True)
    plt.show()

