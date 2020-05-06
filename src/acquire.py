import src.env

from os.path import isfile
import pandas as pd

def query_sql():
    # Query for mySQL
    query = '''
    SELECT prop.*, 
           pred1.logerror, 
           pred1.transactiondate, 
           air.airconditioningdesc, 
           arch.architecturalstyledesc, 
           build.buildingclassdesc, 
           heat.heatingorsystemdesc, 
           landuse.propertylandusedesc, 
           story.storydesc, 
           construct.typeconstructiondesc 
    FROM   properties_2017 prop 
           LEFT JOIN predictions_2017 pred1 USING (parcelid) 
           INNER JOIN (SELECT parcelid, 
                              logerror, 
                              Max(transactiondate) maxtransactiondate 
                       FROM predictions_2017 
                       GROUP BY parcelid, 
                                logerror) pred2 
                       ON pred1.parcelid = pred2.parcelid 
                            AND pred1.transactiondate = pred2.maxtransactiondate 
           LEFT JOIN airconditioningtype air USING (airconditioningtypeid) 
           LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid) 
           LEFT JOIN buildingclasstype build USING (buildingclasstypeid) 
           LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid) 
           LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid) 
           LEFT JOIN storytype story USING (storytypeid) 
           LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid) 
    WHERE  prop.latitude IS NOT NULL 
        AND prop.longitude IS NOT NULL
    '''

    # Generate the url needed for pandas to query the sql database
    zillow_url = f'mysql+pymysql://{src.env.user}:{src.env.password}@{src.env.host}/zillow'

    return pd.read_sql(query, zillow_url)

def get_zillow_data():
    '''
    Takes in nothing.
    Returns a DF cotaining the zillow data pulled from mySQL
    '''
    if isfile('data/raw/zillow_unprocessed.csv'):
        df = query_sql()
        print('CSV previously generated at `data/raw/zillow_unprocessed.csv`. Reading in that csv as a DataFrame')
    else:
        df = query_sql()
        df.to_csv('data/raw/zillow_unprocessed.csv')
        print('CSV generated at `data/raw/zillow_unprocessed.csv`. Returning data as a DataFrame.')
        
    return df