"""Analyse the clicks as per the encoding

This script allows the user to print to the console all columns in the
spreadsheet. It is assumed that the first row of the spreadsheet is the
location of the columns.

This tool accepts comma separated value files (.csv) as well as excel
(.xls, .xlsx) files.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * get_spreadsheet_cols - returns the column headers of the file
    * main - the main function of the script
"""

import pandas as pd
import json
import time
import configparser
import sys
import os

#sys.path.append(r'C:\Users\manoj\code\bitly')

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
    return short_url[-7:]   #could be more so use s[s.rfind('/')+1:len(s)]

def read_config():
    config = configparser.ConfigParser()

    config.read(r'C:\Users\manoj\code\bitly\myenv\config\config.ini')

    config_dict = config['BITLY']

    return config_dict



def read_datafiles(val):


    chunk_size = 50000

    file_path_decode = val.get('pathfile_decode','yyyy')
    file_path_encode = val.get('pathfile_encode','yyyy')

    


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
    # parse the column bitlink
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

    #groupby long_url and get the counts
    res1=res[['long_url']].value_counts().reset_index(name='counts')
    #convert the dataframe to list of dict 
    print([(dict(zip(res1.long_url, res1.counts)))])

    #filter only rows belonging to 2021
    df_2021 = res[(res['dt'] >= '2021-01-01') & (res['dt'] <= '2021-12-31')]
    res3 = df_2021[['long_url']].value_counts().reset_index(name='counts')

    print([(dict(zip(res3.long_url, res3.counts)))])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    config_dict = read_config()
    
    df_decode, df_encode = read_datafiles(config_dict)
    res=analyse_datafiles(df_decode, df_encode)
    display_results(res)




    print(f"\n\nThe process took {round(time.time()-start,2)} secs")

"""
readme.md

First Step to install and run this program.
git clone <url> (clone the repo in your desired folder
On windows :rightclick and select run powershell on the ps script you would have 
the ps script will install the dependencies and then copy the source code into the virtual env and run it and then deactivate it.
the output will be produced on the console and pause for a look.
"""
