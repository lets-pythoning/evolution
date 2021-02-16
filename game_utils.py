from random import sample
from os import system
from time import sleep
from components import Player, Creature, Status
from io_utils import *
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

def send_cards(status: Status):
    clear(is_fresh=True, status=status)
    
    players = status.players
    for player in players:
        player.get_cards(status.deck)
        
        sleep(2)
        clear(is_fresh=True, status=status)

def secret_move(status: Status):
    food_point = 0
    players = status.players
    for player in players:
        print(f'{str(player)}\'s secret move, other players please leave the screen.')
        
        answer = ''
        while answer.lower == 'y' or answer.lower == 'yes':
            answer = input('Leaved? (Y/N)\n> ')
            sleep(2)
        
        print('Ok.')
        
        food_point += ask_food_card(player)
        change_creature_feature(player)
        
        clear()
    
    status.water_hole = status.water_hole + food_point if status.water_hole + food_point >= 0 else 0
    for player in players:
        player.announce()

def start_eat(status: Status):
    flag = is_eating_more(status)
    while flag != None:
        if flag == False:
            for player in status.players:
                if player.has_herbivore:
                    clear(is_fresh=True, status=status)

                    opt_list = []
                    for creature in player.creatures.creatures:
                        if creature.is_full:
                            opt_list.append(f'{str(creature)}(FULL)')
                        elif not creature.is_herbivore:
                            opt_list.append(f'{str(creature)}(DISABLED)')

                    eat_output(opt_list, player, status)

        else:
            for player in status.players:
                clear(is_fresh=True, status=status)

                opt_list = []
                for creature in player.creatures.creatures:
                    if creature.is_full:
                        opt_list.append(f'{str(creature)}(FULL)')
                    
                eat_output(opt_list, player, status)
        
        for player in status.players:
            flag, died_list = player.check_deletion
            if flag:
                for died_creature in died_list:
                    print(f'{str(player)}\'s {str(died_creature)} died.')
            
            player.check_herbivore
    
    print('All creatures ate.')
    for player in status.players:
        player.next_round()
    
    sleep(2)
    clear(is_fresh=True, status=status)

__all__ = ['clear', 'render_status', 'inform', 'command_pattern']
