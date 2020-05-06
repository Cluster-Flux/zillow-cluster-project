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
def scale_data(df):
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    numeric_columns = list(df.select_dtypes('number').columns)
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df