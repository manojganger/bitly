import sys
sys.path.insert(1,r'C:\Users\manoj\code\bitly\myenv')

from ..main import parse_for_hash

def test_always_passes():
    assert True

def test_always_fails():
    assert True


def test_parse_for_hash():
    s='http://bit.ly/31Tt55y'
    as_per_current_extract_method=parse_for_hash(s)
    as_per_second_extract_method = s[s.rfind('/')+1:len(s)]

    assert as_per_current_extract_method==as_per_second_extract_method