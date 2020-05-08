import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def get_inertia(k, X_train):
    return KMeans(k).fit(X_train).inertia_

def plot_inertia(X_train):
    plt.figure(figsize=(13, 7))
    pd.Series({k: get_inertia(k, X_train) for k in range(2, 13)}).plot()
    plt.xlabel('k')
    plt.ylabel('inertia')
    plt.xticks(range(2, 13))
    plt.grid()

def build_and_predict_clusters(k, X_train, clusters_df, cluster_name):
    kmeans = KMeans(k).fit(X_train)
    clusters_df[cluster_name] = kmeans.labels_
    clusters_df[cluster_name] = 'cluster ' + clusters_df[cluster_name].astype(str)
    
    return kmeans, clusters_df