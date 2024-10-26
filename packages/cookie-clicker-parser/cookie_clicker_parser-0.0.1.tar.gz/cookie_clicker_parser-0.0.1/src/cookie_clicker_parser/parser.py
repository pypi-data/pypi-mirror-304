from section_parsers import run_detail_data, preference_names, misc_game_data_data
from urllib.parse import unquote
import base64
import json


def parse(save_code: str) -> object:
    plain_code: str = decode_64(unquote(save_code))
    sections = list(filter(None, plain_code.split("|")))
    print(sections)

    game = {}
    game["version"] = sections[0]

    run_details = sections[1].split(";")
    load_section(game, run_details, "run_details", run_detail_data())

    preferences = list(sections[2])
    load_section(game, preferences, "preferences", preference_names())

    misc_game_data = sections[3].split(";")
    load_section(game, misc_game_data, "misc_game_data", misc_game_data_data())
    
    return game

def get_seed(save_code: str) -> str:
    return parse(save_code)["run_details"]["seed"]

def load_section(game: object, section: list, section_name: str, section_data: object) -> None:
    section = list(filter(lambda s: s != "", section))
    if len(section_data) < len(section):
        raise ValueError(f"Too many entries in section {section_name}({len(section)}) ({len(section_data)} supported). Package might be out of date")
    game[section_name] = {}
    for x, value in enumerate(section):
        key = list(section_data)[x]
        game[section_name][key] = parse_value(value, *section_data[key])

def parse_value(value: str, *parsers):
    for parser in parsers:
        value = parser(value)
    return value

def decode_64(save_code: str) -> str:
    save_code: str = save_code.removesuffix("!END!")
    save_bytes: bytes = base64.b64decode(save_code)
    return save_bytes.decode("utf-8")

if __name__ == "__main__":
    with open("tests/save_codes.json") as save_codes_file:
        save_codes = json.load(save_codes_file)
    print(json.dumps(parse(save_codes[0]["save_code"]), indent=4))
