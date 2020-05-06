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
    # Saving the shape to calculate number of features/rows dropped
    shape_before = df.shape

    # Using the threshold to drop the features
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    
    # Using the threshold to drop the rows
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    
    # Saving the shape to calculate number of features/rows dropped
    shape_after = df.shape
    
    print(f'''
    Number of rows dropped:    {shape_before[0] - shape_after[0]}
    Number of columns dropped: {shape_before[1] - shape_after[1]}
    ''')

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
    
################################
#  Tools for Handling Dtypes   #
################################

def numeric_to_object(df, features):    
    features = ['fips', 
                'regionidcity', 
                'regionidcounty', 
                'regionidzip']
    
    for col in features:
        df[col] = df[col].astype('object')
    
    return df


def object_to_numeric(df, features):    
    for col in features:
        df[col] = df[col].astype('float')
    
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