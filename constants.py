from json import load

PLAYER_NUM = 2
SINGLE_CARD_NUM = 7
CARDS = [
    'GroupHunting', 'CaveDwelling', 'Climb', 'Intelligence',
    'Cooperation', 'Foraging', 'ClusterDefense', 'Symbiosis',
    'Carnivorous', 'AdiposeTissue', 'LongNeck', 'HardShell',
    'Horn',
]

CARD_NUM = len(CARDS) * SINGLE_CARD_NUM

IO_CHAR_LIMIT = 50

LANGUAGE_ROOT_PATH = 'language'
LANGUAGE = 'chinese'
LANGUAGE_PATH = rf'{LANGUAGE_ROOT_PATH}\{LANGUAGE.lower()}.json'

try:
    with open(LANGUAGE_PATH, 'r', encoding='utf-8') as file:
        LANGUAGE_DICT = load(file)
        assert isinstance(LANGUAGE_DICT, dict)

except AssertionError as e:
    raise TypeError(f'JSON file {LANGUAGE_PATH} is not a valid language file!') from e
except FileNotFoundError as e:
    raise FileNotFoundError(f'No file at {LANGUAGE_PATH}, check your PATH or LANGUAGE.') from e
except UnicodeError as e:
    raise UnicodeError('JSON file not encode by utf-8!') from e
