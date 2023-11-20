"""
Analyse the clicks on the incoming datafiles for long url.

This script loads two files and join it together to get the long_url and the clicks against it.
Dups are checked and it gets warned in pytest. De-duping is not performed.

The two files are in json and csv format but are loaded into a pandas dataframe and then merged
on the hash value. The hash value is extracted and two different methods are used to ensure that
it alerts in case specs changes.

Analysis is performed on the merged dataframe.

The results are displayed on to the stdout.

"""

import time
import configparser
import pandas as pd

def parse_for_hash(short_url):
    """This method parse the hash value from the shortened url

        Parameters
        ----------
        short_url : str
            The short url which contains hash value. It is assumed that it would be 7 char long but
            if it changes, it would be detected by pytest

        Returns
        -------
        rightmost 7 chars of short_url
            
    """
    # could be different so use s[s.rfind('/')+1:len(s)]
    return short_url[-7:]

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
    chunk_size = int(val.get('read_chunksize', 10000))

    file_path_decode = val.get('pathfile_decode','data/decodes.json')
    file_path_encode = val.get('pathfile_encode','data/encodes.csv')

    data_list_decode = []
    data_list_encode = []

    with open(file_path_decode, 'r', encoding="utf-8") as file:
        for chunk in pd.read_json(file, lines=True, chunksize=chunk_size):
            data_list_decode.extend(chunk.to_dict(orient='records'))

    with open(file_path_encode, 'r', encoding="utf-8") as file:
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

def display_results(df_merged):
    """This method displays the output on console as per the format

            Parameters
            ----------
            df_merged  : DataFrame

            Returns
            -------
            None

    """

    #groupby long_url and get the counts
    df_clicks = df_merged[['long_url']].value_counts().reset_index(name='counts')

    #convert the dataframe to list of dict
    print([(dict(zip(df_clicks.long_url, df_clicks.counts)))])

    #filter only rows belonging to 2021
    df_2021 = df_merged[(df_merged['dt'] >= '2021-01-01') & (df_merged['dt'] <= '2021-12-31')]
    df_clicks_2021 = df_2021[['long_url']].value_counts().reset_index(name='counts')

    print([(dict(zip(df_clicks_2021.long_url, df_clicks_2021.counts)))])


if __name__ == '__main__':

    #time the whole process
    start = time.time()
    config_data = read_config()
    df_decode_data, df_encode_data = read_datafiles(config_data)
    df_merged_data = analyse_datafiles(df_decode_data, df_encode_data)
    display_results(df_merged_data)

    print(f"\n\nThe process took {round(time.time()-start,2)} secs")
