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

def get_card(cards: list) -> Card:
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

def get_food_card() -> list:
    cards = []
    for player in players:
        card = get_card(player.cards)
        cards.append(card)

    return cards

def fresh():
    system('cls')

    for player in players:
        print(str(player))
        for creature in player.creatures:
            print(f' - {str(creature)}: {[str(feature) for feature in creature.features]}')

        print(f' - {[str(card) for card in player.cards]}')

    print(f'water hole: {water_hole}')
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
    food_cards = get_food_card()
    for card in food_cards:
        water_hole += card.point
        del card
    
    if water_hole < 0:
        water_hole = 0

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
        while True:
            index = input('Which creature do you want to let it eat?\n> ')
            creature_not_full = [creature for creature in player.creatures if not creature.is_full]
            try:
                if index.lower() != 'skip':
                    index = int(index)
                    creature = creature_not_full[index - 1]
                    
                    if not creature.is_carnivorous:
                        assert water_hole
                
                else:
                    return
                
                break
            
            except IndexError:
                print('Creature index out of range. Try again.')
            except ValueError:
                print('Try to input an integer. Please try again.')
            except AssertionError:
                print('Water hole is empty. Choose another one or skip.')
        
        if creature.is_carnivorous:
            attack(creature)
        else:
            creature.eat(1)

def add_card(player: Player):
    print(f'Your hand cards: {[str(card) for card in player.cards]}')
    
    while True:
        index = input('Which creature?\n> ')
        try:
            index = int(index)
            creature = player.creatures[index - 1]
        
        except IndexError:
            print('Creature index out of range. Try again.')
        except ValueError:
            print('Try to input an integer. Please try again.')
    
    print(f'{str(creature)}\' features: {[str(feature) for feature in creature.hidden_features + creature.features]}')
    
    card = get_card(player.cards)
    creature.add_feature(card)
