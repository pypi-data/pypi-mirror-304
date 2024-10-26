from urllib.parse import unquote


def test_unquote(*save_codes):
    for code in save_codes:
        assert unquote(code["save_code"]) == code["save_code_unquoted"]
