from cookie_clicker_parser import parse


def test_code(*save_codes):
    for code in save_codes:
        assert parse(code["save_code"]) == code["save_code"]
