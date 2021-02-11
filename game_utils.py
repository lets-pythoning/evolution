from random import sample
from os import system
from components import *
from constants import CONSTANTS, CARDS
from game_saver import save_game, read_game

def clear(is_fresh=False, status=None):
    system('cls')
    if is_fresh:
        inform(status)

def render_status() -> Status:
    player_num = CONSTANTS['PLAYER_NUM']
    cards_num = CONSTANTS['CARDS_NUM']
    
    player_list = []
    for i in range(player_num):
        player = Player(i + 1)
        player.add_creature(Creature(id=1, creature_seq=player.creatures))
        
        player_list.append(player)

    status = Status(player_list)
    status.deck.add_cards(sample(CARDS, cards_num))
    
    return status

def command_pattern(status: Status) -> bool:
    command = input('Enter command pattern (enter help for more information):\n> ').lower()
    if command == 'help':
        print('Commands:\n')
        print('Enter "C" for continue game.')
        print('Enter "SAQ" for "save and quit".')
        print('Enter "Q" for quit the game.')
        print('Enter "RAR" for "reset and read".')
        print('Enter "SAR" for "save and read".')
        print('\nNow try again.')

        clear(is_fresh=True, status=status)
        command_pattern(status)

    elif command == 'C':
        return False
    
    elif command == 'SAQ':
        save_game(status)
        return True

    elif command == 'Q':
        return True
    
    elif command == 'RAR':
        path = input('Enter file path:\n> ')
        status.read(read_game(path))
        
        return False
    
    elif command == 'SAR':
        save_game(status)
        
        path = input('Enter file path:\n> ')
        status.read(read_game(path))
        
        return False

def inform(status: Status):
    for player in status.players:
        creatures = player.creatures.creatures
        cards = player.cards
        print(f'{str(player)} has: \n{len(creatures)} creatures\n{len(cards)} cards\n')
        
        for creature in creatures:
            print(f'{str(player)}\'s {str(creature)}:', *(creature.features), '\n')
        
        if player.is_first:
            print(f'And this player is first.\n{"-" * 10}\n')

__all__ = ['clear', 'render_status', 'inform', 'command_pattern']
