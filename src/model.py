import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#########################
#  Handleing Outliers   #
#########################

#--------------- Helper Functions ---------------#
def get_lower_outliers(s, k):
    """
    Parameters are the series and the k value.  Returns the lower outliers of either 0 or another
    number, indicating how far away from the lower bound (Q1) the observation is.
    """
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    lower_bound = q1 - (k * iqr)
    return s.apply(lambda x: max([x + lower_bound, 0]))

def get_upper_outliers(s, k):
    """
    Parameters are the series and the k value.  Returns the upper outliers of either 0 or another
    number, indicating how far away from the uppper bound (Q3) the observation is.
    """
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

#--------------- Fucntions to call to handle outliers ---------------#
def add_lower_outlier_columns(df):
    """
    Adds a df column to show the outliers
    """
    for col in df.select_dtypes("number"):
        df[col + "_outliers"] = get_lower_outliers(df[col], 1.5)
        
    return df

def add_upper_outlier_columns(df):
    """
    Adds a df column to show the outliers
    """
    for col in df.select_dtypes("number"):
        df[col + "_outliers"] = get_upper_outliers(df[col], 1.5)
        
    return df

#########################
#    KMeans Modeling    #
#########################

#--------------- Plotting and Determing K ---------------#
def get_inertia(k, X_train):
    return KMeans(k).fit(X_train).inertia_

def plot_inertia(X_train):
    plt.figure(figsize=(13, 7))
    pd.Series({k: get_inertia(k, X_train) for k in range(2, 13)}).plot()
    plt.xlabel('k')
    plt.ylabel('inertia')
    plt.xticks(range(2, 13))
    plt.grid()

#--------------- Creating Clusters ---------------#
def build_and_predict_clusters(k, X_train, clusters_df, cluster_name):
    kmeans = KMeans(k).fit(X_train)
    clusters_df[cluster_name] = kmeans.labels_
        
    return kmeans, clusters_df