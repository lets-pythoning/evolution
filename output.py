from time import sleep
from random import sample
from utils import ORDERS, Player, Creature

def _paser(inpution: str) -> tuple:
    if inpution[-1].isdigit() and inpution[-2] == '到':
        if inpution[:2] == '增加':
            return True, 'add', inpution[2:-2], int(inpution[-1])
        elif inpution[:2] == '移除':
            return True, 'delete', inpution[2:-2], int(inpution[-1])
        else:
            return False, 
    
    else:
        return False, 

def ask_add_character(player: Player) -> None:
    print(f'{str(player)}\'s secret move. Other player please leave the screen.')
    sleep(2)
    print(f'Your cards:\n{", ".join(player.cards)}')

    n = 1
    while True:
        answer = input(f'{n} ')
        if answer == 'ok':
            return None
        if 2 >= len(player.cards):
            return None
        
        while True:
            result = _paser(answer)
            if result[0] == True:
                if result[1] == 'add':
                    if result[2] in player.cards:
                        try:
                            player.creatures_list[player.get_creatures().index(result[3])].add(result[2])
                            player.cards.remove(result[2])
                            break
                        
                        except:pass
                
                else:
                    if player.get_creatures().count(result[3]):
                        creature = player.creatures_list[player.get_creatures().index(result[3])]
                        if result[2] in creature.get_characters():
                            try:
                                creature.delete(result[2])
                                break
                                
                            except:pass

            answer = input(f'{n} ')
                            
        n += 1

def ask_food_card(player: Player) -> int:
    food_points = sample(range(-3, 9), len(player.cards))
    
    print('Now please show a food card.')
    print(f'Food points:\n{food_points}')
    
    while True:
        answer = input('\nEnter index:\n> ')
        index = int(answer) if answer.isdigit() else -1
        if len(player.cards) >= index > 0:
            return food_points[index - 1]

def output_info(deck: list, pond: int, players: list) -> None:
    for player in players:
        print(f'{str(player)} has {len(player.creatures_list)} creatures.')
        for creature in player.creatures_list:
            print(f'{str(creature)}: {", ".join(creature.characters)}')
            print(f'population - {creature.get_info()[0]} size - {creature.get_info()[1]}')
        
        print(f'And {len(player.cards)} cards')
    
    print(f'There are still {len(deck)} cards in deck.')
    print(f'And there are also {pond} food in water hole.')
    print('Fine.')
