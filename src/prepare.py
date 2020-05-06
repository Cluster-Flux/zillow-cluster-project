#############
#  Imports  #
#############

import pandas as pd

################################
#  Tools for Examing the Data  #
################################

def nulls_by_col(df):
    '''
    Takes in a dataframe.
    Returns a dataframe detailing the number of missing values per column.
    '''
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    pct_missing = num_missing / rows
    cols_missing = pd.DataFrame({'number_missing_rows': num_missing, 'percent_rows_missing': pct_missing})
    return cols_missing


def nulls_by_row(df):
    '''
    Takes in a dataframe.
    Returns a dataframe detailing the number of missing values per row.
    '''
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1)/df.shape[1]*100
    rows_missing = pd.DataFrame({'num_cols_missing': num_cols_missing, 
                                 'pct_cols_missing': pct_cols_missing}).reset_index().groupby(['num_cols_missing','pct_cols_missing']).count().rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing 


################################
#  Tools for Handling Nulls    #
################################

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    '''
    Drops rows by a percentage of missing values,
    drops columns by a percentage of missing values.
    '''
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def drop_columns(df):
    df.drop(columns=[
            'buildingqualitytypeid',     # Used to merge in SQL 
            'heatingorsystemtypeid',     # Used to merge in SQL
            'propertylandusetypeid',     # Used to merge in SQL
            'calculatedbathnbr',         # Too similiar to bathroomcnt
            'propertycountylandusecode', # We're already filtering for single unit residential
            'propertyzoningdesc',        # Doesn't provide anything useful, missing too many values
            'censustractandblock',       # Doesn't provide anything useful, missing too many values
            ], inplace=True)
    
    return df


def fill_with_median(df):
    features = ['taxvaluedollarcnt',
                'calculatedfinishedsquarefeet',
                'taxamount',
                'fullbathcnt',
                'lotsizesquarefeet',
                'structuretaxvaluedollarcnt',
                'finishedsquarefeet12']
    
    for f in features:
        df[f] = df[f].fillna(df[f].median)
        
    return df


def fill_nulls_with_mode(df):
    features = ['regionidzip',
                'regionidcity',
                'yearbuilt',
                'landtaxvaluedollarcnt']
    
    for f in features:
        df[f] = df[f].fillna(df[f].mode)
        
    return df
    
    
####################
#   Main Function  #
####################

def wrangle_zillow(df):
    # Handling columns and rows with too much missing values
    df = handle_missing_values(df)
    
    # Dropping features
    df = drop_columns(df)
    
    # Handling missing values by filling with the median 
    df = fill_with_median(df)
    
    # Handling missing values by filling with the mode
    df = fill_nulls_with_mode(df)
    
    return df


#####################################
#  Tools for Splitting and Scaling  #
#####################################

#--------------- Splitting ---------------#
def split_data(df):
    from sklearn.model_selection import train_test_split

    train, test     = train_test_split(df, random_state=123, train_size=.8)
    train, validate = train_test_split(df, random_state=123, train_size=.8) 
    
    return train, test, validate


#--------------- Scaling ---------------#
def numeric_to_object(df, features):    
    for col in features:
        df[col] = df[col].astype('object')
    
    return df

def scale_data(df):
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    numeric_columns = list(df.select_dtypes('number').columns)
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df