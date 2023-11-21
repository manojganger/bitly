import pytest
import configparser
from ..main import parse_for_hash
import os
import pandas as pd

@pytest.fixture
def t_read_config():
    config = configparser.ConfigParser()
    print(f"pwd={os.getcwd()}")
    config.read(r'config\config.ini')
    config_dict = config['BITLY']

    return config_dict


def test_read_config(t_read_config):
    assert t_read_config.get('pathfile_decode', '') == r'data\decodes.json'

def test_read_datafiles(t_read_config):
    file_path_encode = t_read_config.get('pathfile_encode', '')

    with open(os.path.join("",file_path_encode), 'r', encoding="utf-8") as file:
        df = pd.read_csv(file)

    assert df['hash'].duplicated().any() == False


def test_parse_for_hash():
    s='http://bit.ly/31Tt55y'
    as_per_current_extract_method=parse_for_hash(s)
    as_per_second_extract_method = s[s.rfind('/')+1:len(s)]

    assert as_per_current_extract_method==as_per_second_extract_method