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
def fill_nulls_with_median(df):
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


def scale_data(df):
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    numeric_columns = list(df.select_dtypes('number').columns)
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df

#####################################
#          Main Function            # 
#####################################

def split_scale_dataframes(train, test, validate):
    for df in [train, test, validate]:
        df.apply(split_data())
        df.apply(scale_data())
        
    return train, test, validate