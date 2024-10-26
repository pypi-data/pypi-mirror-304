from cookie_clicker_parser.parser import decode_64


def test_b64_decode(*save_codes):
    for code in save_codes:
        assert decode_64(code["save_code_unquoted"]) == code["save_code_b64_decoded"]