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
sys.path.append(r'C:\Users\manoj\code\bitly')
def parse_for_hash(s):
    """Gets and prints the spreadsheet's header columns

        Parameters
        ----------
        file_loc : str
            The file location of the spreadsheet
        print_cols : bool, optional
            A flag used to print the columns to the console (default is
            False)

        Returns
        -------
        list
            a list of strings used that are the header columns
        """
    return s[-7:]   #could be more so use s[s.rfind('/')+1:len(s)]
def print_hi(name):
    config = configparser.ConfigParser()

    config.read(r'C:\Users\manoj\code\bitly\myenv\config\config.ini')

    val = config['BITLY']


    # print(os.getcwd())
    # print(os.path.abspath(__file__))
    #
    # os.chdir(r"C:\Users\manoj\code\bitly")
    #
    # print(os.getcwd())

    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    chunk_size = 50000
    #file_path_decode = r"C:\Users\manoj\code\bitly\myenv\data\decodes.json"
    #file_path_encode = r"C:\Users\manoj\code\bitly\myenv\data\encodes.csv"

    file_path_decode = val.get('pathfile_decode','yyyy')
    file_path_encode = val.get('pathfile_encode','yyyy')

    


    absolute_path = os.path.dirname(os.path.abspath(__file__))
    print(f"absolute path is = {absolute_path}")

    #file_path_decode = r'{}'.format(os.path.join(absolute_path, val.get('pathfile_decode','yyyy')))
    #file_path_encode = r'{}'.format(os.path.join(absolute_path, val.get('pathfile_encode','zzz')))
    
    print(f"full path is = {file_path_decode}")
    print(f"full path is = {file_path_encode}")

    print(val.get('pathfile_decode','yyyy'))

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


    # Display the DataFrame
    df_decode['hash']=df_decode['bitlink'].apply(parse_for_hash)

    print(df_encode)


    print(df_decode.head())

    res = pd.merge(df_decode,df_encode, on='hash', how='left')
    print(res[['bitlink', 'hash', 'long_url']])

    res['dt']=pd.to_datetime(res['timestamp'])
    print(res)


    res1=res[['long_url']].value_counts().reset_index(name='counts')

    print([(dict(zip(res1.long_url, res1.counts)))])

    res2=res[(res['dt'] >= '2021-01-01') & (res['dt'] <= '2021-12-31')]
    res3 = res2[['long_url']].value_counts().reset_index(name='counts')

    print([(dict(zip(res3.long_url, res3.counts)))])





    #dq check - make sure encode is unique
    #chk for dup in decode

    # 1 join and group by long_url and count the click on it.
    # 2 put having clause for 2021


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    print_hi('PyCharm')


    #read both the files and returns df

    #extract hash value.
    #mergre the two dataframe and return the result

    #filter the dataframe and return the results

    #do the print of that.



    print(time.time()-start)

"""
readme.md

First Step to install and run this program.
git clone <url> (clone the repo in your desired folder
On windows :rightclick and select run powershell on the ps script you would have 
the ps script will install the dependencies and then copy the source code into the virtual env and run it and then deactivate it.
the output will be produced on the console and pause for a look.
"""
