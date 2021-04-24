from os import system
from random import shuffle

from cards import *
from constants import *
from errors import Dead

# ---------------- #
#  Lower Function  #
# ---------------- #

def _render_card(name: str) -> object:
    try:
        obj = eval(name + '("in deck")')
    except NameError as e:
        raise NameError(f'No card named {name}.') from e

    return obj

deck = [_render_card(name) for name in CARDS * 3]
players = [Player(id_=id_) for id_ in range(1, PLAYER_NUM + 1)]

def _get_card(cards: list) -> Card:
    print([str(card) for card in cards], '\n')

    while True:
        index = input('Input card index: ')
        try:
            index = int(index)
            card = cards[index - 1]

            return card

        except IndexError:
            print('Index out of range, choose again.')
        except ValueError:
            print('Index not an integer, choose again.')

def _get_creature(creatures: list) -> Creature:
    while True:
        index = input('Which creature?\n> ')
        try:
            index = int(index)
            creature = creatures[index - 1]

        except IndexError:
            print('Creature index out of range. Try again.')
        except ValueError:
            print('Try to input an integer. Please try again.')
    
    return creature

def _get_food_card() -> list:
    cards = []
    for player in players:
        card = _get_card(player.cards)
        cards.append(card)

    return cards

def fresh():
    system('cls')

    for player in players:
        print(str(player))
        for creature in player.creatures:
            print(f' - {str(creature)}: {[str(feature) for feature in creature.features]}')

        print(f' - {[str(card) for card in player.cards]}')

    print(f'water hole: {water_hole_control(0)}')
    print(f'deck: {len(deck)}')

def _can_attack(hunter: Creature, aim: Creature) -> bool:
    for aim_card in aim.features:
        if aim_card.been_attack(hunter):
            continue

        flag_list = []
        hunter.features.sort(key=lambda card: card.index)
        for hunter_card in hunter.features:
            flag_list.append(hunter_card > aim_card)

        if not any(flag_list):
            break

    else:
        return True

    return False

# ---------------- #
#  Upper Function  #
# ---------------- #

def announce():
    food_cards = _get_food_card()
    for card in food_cards:
        water_hole_control(card.point)
        del card

    for player in players:
        player.announce()
    
    fresh()

def next_round():
    for player in players:
        player.announce()
    
    fresh()
    
def attack(hunter: Creature):
    while True:
        fresh()
        player_index = input('Input the player\'s index you\'d want to attack:\n> ')
        try:
            player = players[int(player_index) - 1]
            break
        
        except IndexError:
            print('Player index out of range. Try again.')
        except ValueError:
            print('Try to input an integer. Please try again.')
    
    while True:
        fresh()
        print(f'You want to attack{str(player)}. He has got creature:\n{[str(creature) for creature in player.creatures]}')
        
        creature_index = input('Input creature\'s index:\n> ')
        try:
            creature = player.creatures[int(creature_index) - 1]
            break
            
        except IndexError:
            print('Creature index out of range. Try again.')
        except ValueError:
            print('Try to input an integer. Please try again.')
    
    if _can_attack(hunter, creature):
        creature.population -= 1
        hunter.eat(creature.size)

def eat(player: Player):
    fresh()
    print(f'{str(player)}, you have got creature that not full:\n{[str(creature) for creature in player.creatures if not creature.is_full]}')
    
    choice = input('Do you want to eat?\n> ')
    if choice.lower() in ('yes', 'y'):
        index = input('Do you want to skip?\n> ')
        creature_not_full = [creature for creature in player.creatures if not creature.is_full]
        if index.lower() != 'skip':
            creature = _get_creature(creature_not_full)
        
        else:
            return

    if creature.is_carnivorous:
        attack(creature)
    else:
        creature.eat(1)

def is_deck() -> bool:
    if deck:
        return True
    
    return False

def split_cards():
    global deck
    
    for player in players:
        card_num = 3 + len(player.creatures)
        if len(deck) >= card_num:
            cards = deck[-card_num:]
            deck = deck[:-card_num]
        
        else:
            cards = deck
            deck = []
            
        for card in cards:
            card.root = player
            card.father = player
            
            player.cards.append(card)

def add_card(player: Player):
    fresh()
    print(f'Your hand cards: {[str(card) for card in player.cards]}')
    
    creature = _get_creature(player.creatures)
    
    print(f'{str(creature)}\' features: {[str(feature) for feature in creature.hidden_features + creature.features]}')
    
    card = _get_card(player.cards)
    creature.add_feature(card)

def delete_card(player: Player):
    fresh()

    creature = _get_creature(player.creatures)
    
    print(f'{str(creature)}\' features: {[str(feature) for feature in creature.hidden_features + creature.features]}')
    
    card = _get_card(creature.hidden_features + creature.features)
    creature.delete_feature(card)

def private_move():
    for player in players:
        input(f'{str(player)}\' private move.')
        
        answer = ''
        while answer not in ('q', 'quit'):
            answer = input(f'What do you want to do?\n> ').lower()
            
            if answer in ('del', 'd', 'delete', '-'):
                delete_card(player)
            elif answer in ('add', 'a', '+'):
                add_card(player)
            else:
                print('What?')

def eat_together() -> bool:
    result = False
    for player in players:
        fresh()
        
        choice = input('Do you want to eat?\n> ').lower()
        if choice in ('yes', 'y'):
            flag = any([creature.is_full for creature in player.creatures])
            if flag:
                result = True
            else:
                print('Sorry. Your creature are already full.')
    
    return result
