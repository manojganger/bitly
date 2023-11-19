from ..main import parse_for_hash

def test_always_passes():
    assert True

def test_always_fails():
    assert True


def test_parse_for_hash():

    as_per_current_extract_method=parse_for_hash('http://bit.ly/31Tt55y')
    as_per_second_extract_method = s[s.rfind('/')+1:len(s)]

    assert as_per_current_extract_method==as_per_second_extract_method