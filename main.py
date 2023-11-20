"""
Analyse the clicks on the incoming datafiles for long url.

This script loads two files and join it together to get the long_url and the clicks against it.
Dups are checked and it gets warned in pytest. De-duping is not performed.

The two files are in json and csv format but are loaded into a pandas dataframe and then merged
on the hash value. The hash value is extracted and two different methods are used to ensure that it alerts in case specs changes.

Analysis is performed on the merged dataframe.

The results are displayed on to the stdout.

"""

import pandas as pd
import json
import time
import configparser
import sys
import os

def parse_for_hash(short_url):
    """This method parse the hash value from the shortened url

        Parameters
        ----------
        short_url : str
            The short url which contains hash value. It is assumed that it would be 7 char long but if it changes, it would be detected by pytest

        Returns
        -------
        rightmost 7 chars of short_url
            
    """
    return short_url[-7:]   #could be different so use s[s.rfind('/')+1:len(s)]

def read_config():
    """This method reads configuration setting in config/config.ini

        Parameters
        ----------
        None


        Returns
        -------
        dict of the parameters

    """
    config = configparser.ConfigParser()

    config.read(r'config\config.ini')

    config_dict = config['BITLY']

    return config_dict


def read_datafiles(val):
    """This method reads incoming datafiles (json and csv)

        Parameters
        ----------
        configuration parameters : dict


        Returns
        -------
        the two dataframes decode and encode (in that order): DataFrame

    """
    chunk_size = 50000

    file_path_decode = val.get('pathfile_decode','data/decodes.json')
    file_path_encode = val.get('pathfile_encode','data/encodes.csv')

    data_list_decode = []
    data_list_encode = []

    with open(file_path_decode, 'r') as file:
        for chunk in pd.read_json(file, lines=True, chunksize=chunk_size):
            data_list_decode.extend(chunk.to_dict(orient='records'))

    with open(file_path_encode, 'r') as file:
        for chunk in pd.read_csv(file,  chunksize=chunk_size):
            data_list_encode.extend(chunk.to_dict(orient='records'))

    # Create a DataFrame from the list of JSON data
    df_decode = pd.DataFrame(data_list_decode)
    df_encode = pd.DataFrame(data_list_encode)



    return df_decode, df_encode



    #dq check - make sure encode is unique
    #chk for dup in decode

    # 1 join and group by long_url and count the click on it.
    # 2 put having clause for 2021

def analyse_datafiles(df_decode, df_encode):
    """This method analyse the two dataframe for click counts

            Parameters
            ----------
            decode dataframe : DataFrame
            encode dataframe : DataFrame


            Returns
            -------
            merged dataframe: DataFrame

    """
    # parse the column bitlink and create a new column 'hash'
    df_decode['hash']=df_decode['bitlink'].apply(parse_for_hash)

    print(df_encode)


    print(df_decode.head())


    #join the df on hash and get the 
    res = pd.merge(df_decode,df_encode, on='hash', how='left')
    print(res[['bitlink', 'hash', 'long_url']])

    res['dt']=pd.to_datetime(res['timestamp'])
    print(res)

    return res

def display_results(res):
    """This method displays the output on console as per the format

            Parameters
            ----------
            df_merged  : DataFrame



            Returns
            -------
            None

    """

    #groupby long_url and get the counts
    res1=res[['long_url']].value_counts().reset_index(name='counts')
    #convert the dataframe to list of dict 
    print([(dict(zip(res1.long_url, res1.counts)))])

    #filter only rows belonging to 2021
    df_2021 = res[(res['dt'] >= '2021-01-01') & (res['dt'] <= '2021-12-31')]
    res3 = df_2021[['long_url']].value_counts().reset_index(name='counts')

    print([(dict(zip(res3.long_url, res3.counts)))])


if __name__ == '__main__':
    #time the whole process
    start = time.time()
    config_dict = read_config()
    df_decode, df_encode = read_datafiles(config_dict)
    df_merged = analyse_datafiles(df_decode, df_encode)
    display_results(df_merged)

    print(f"\n\nThe process took {round(time.time()-start,2)} secs")

