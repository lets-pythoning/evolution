def card_renderer(name: str) -> object:
    name = name.capitalize()
    exec(f'from cards import {name}')

    return eval(f'{name}()')

CONSTANTS = {
    'CARDS_NUM':10,
    'FEATURE_MAX':3,
    'SINGLE_CARD_LIMIT':2,
    'LOWER_LINE_OF_CARDS':3,
    'PLAYER_NUM':2,
    'MAX_PS':6
}

CARDS_SET = {
    'need_neighbor':['协作', '警报信号', '共生'],
    'need_carnivore':['集群狩猎', '伏击'],
    'need_herbivore':['觅食', '长颈']
}

_CARDS = [
    '协作', '食腐', '警报信号', '共生', '集群狩猎', '伏击',
    '长颈', '觅食', '食肉', '脂肪组织', '多产', '智力'
]

CARDS = [card_renderer(card) for card in _CARDS]

__all__ = ['CONSTANTS', 'CARDS_SET', 'CARDS', 'card_renderer']
