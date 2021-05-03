from os import system
from random import shuffle
from time import sleep

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

shuffle(deck)

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
            
            break

        except IndexError:
            print('Creature index out of range. Try again.')
        except ValueError:
            print('Try to input an integer. Please try again.')
    
    return creature

def fresh():
    system('cls')

    for player in players:
        print(str(player))
        for creature in player.creatures:
            print(
                f' - {str(creature)}: {[str(feature) for feature in creature.features]} {creature.food_num} food {creature.population} population {creature.size} size')

        print(f' - cards: {len(player.cards)}')
        print(f' - point: {player.point}')

    print(f'water hole: {water_hole_control()}')
    print(f'deck: {len(deck)}\n')
    
def _get_food_card() -> list:
    cards = []
    for player in players:
        print(f'{str(player)}, choose a food card.')
        
        card = _get_card(player.cards)
        cards.append(card)
        
        fresh()

    return cards

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
        if hunter.population > aim.population:
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
    
    sleep(2)
    fresh()

def next_round():
    for player in players:
        player.next_round()
        if player.creatures == []:
            creature = Creature(player=player)
            player.creatures.append(creature)
    
    sleep(2)
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

    fresh()
    print(f'You want to attack{str(player)}.')
        
    creature = _get_creature(player.creatures)
    
    if _can_attack(hunter, creature):
        creature.population -= 1
        hunter.eat(creature.size)
    
    else:
        print('Sorry, you can\'t attack it.')
        sleep(1)

def eat(player: Player):
    fresh()
    print(f'{str(player)}, you have got creature that not full:\n{[str(creature) for creature in player.creatures if not creature.is_full]}')

    creature_not_full = [creature for creature in player.creatures if not creature.is_full]
    creature = _get_creature(creature_not_full)

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
    
    if len(player.cards) > 1:
        creature = _get_creature(player.creatures)
        
        print(f'{str(creature)}\'s features: {[str(feature) for feature in creature.hidden_features + creature.features]}')
        
        card = _get_card(player.cards)
        try:
            creature.add_feature(card)
            player.cards.remove(card)
        
        except (IndexError, ValueError) as e:
            print(e)
            sleep(2)
    
    else:
        print('Sorry, you have to stop.')
        sleep(2)

def delete_card(player: Player):
    fresh()

    creature = _get_creature(player.creatures)
    if creature.features:
        print(f'{str(creature)}\'s features: {[str(feature) for feature in creature.features]}')
        
        card = _get_card(creature.features)
        creature.delete_feature(card)
        
        while True:
            choice = input('What do you want to gain?\n> ').lower()
            if ('population'.startswith(choice) or choice in ('+p', '++')) and creature.population != 6:
                creature.population += 1
                break
                
            if ('size'.startswith(choice) or choice in ('+s', '++')) and creature.size != 6:
                creature.size += 1
                break
            
            if choice in ('add creature', 'ac', '+c', '++', 'add', 'a', 'ad'):
                position = input('Which side?\n>')
                if 'left'.startswith(position):
                    player.creatures.insert(0, Creature(player=player))
                    break

                player.creatures.append(Creature(player=player))
                break
                
            print('What?')
    
    else:
        print('Sorry, your creature has no feature.')
        sleep(2)

def private_move():
    fresh()
    
    for player in players:
        input(f'{str(player)}\'s private move.')
        
        answer = ''
        while True:
            fresh()
            answer = input('What do you want to do?\n> ').lower()
            
            if answer in ('del', 'd', 'delete', '-'):
                delete_card(player)
            elif answer in ('add', 'a', '+'):
                add_card(player)
            elif answer in ('q', 'quit'):
                break

        fresh()

def eat_together() -> bool:
    result = False
    for player in players:
        fresh()
        
        if not any(not creature.is_full for creature in player.creatures):
            continue
            
        choice = input(f'{str(player)}, do you want to eat?\n> ').lower()
        if choice in ('yes', 'y'):
            flag = any((not creature.is_full) for creature in player.creatures) and water_hole_control()
            if flag:
                result = True
                eat(player)
                
            else:
                print('Sorry. Your creatures are already full.')
    
    return result

def check_winner():
    for player in players:
        for creature in player.creatures:
            player.point += creature.population
            player.point += len(creature.features)
    
    print('# ' + '-' * 10 + ' #')
    print('# ' + str(max(players, key=lambda player: player.point)).center(10) + ' #')
    print('# ' + '-' * 10 + ' #')

if __name__ == '__main__':
    print('''
This is game_utils.py, not the entrance of Evolution.
Run file enter.py instead.
        ''')
