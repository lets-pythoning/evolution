from cards import *
from errors import Dead
from constants import *
from io_utils import get_food_card, fresh
from random import shuffle

def _render_card(name: str) -> object:
    try:
        obj = exec(name)
    except NameError as e:
        raise NameError(f'No card named {name}.') from e

    return obj

def render_state(state: dict) -> dict:
    state['water_hole'] = 0
    state['players'] = [Player(id_=id_) for id_ in range(1, PLAYER_NUM + 1)]
    
    deck = []
    for card in CARDS:
        for _ in range(SINGLE_CARD_NUM):
            card_obj = _render_card(card)
            deck.append(card_obj)
    
    shuffle(deck)
    state['deck'] = deck
    
    return state

def announce():
    food_cards = get_food_card()
    for card in food_cards:
        state['water_hole'] += card.point
        del card
    
    if state['water_hole'] < 0:
        state['water_hole'] = 0
    
    players = state['players']
    for player in players:
        player.announce()
    
    fresh()

def next_round():
    players = state['players']
    for player in players:
        player.announce()
    
    fresh()
