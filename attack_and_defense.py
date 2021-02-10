from utils import ORDERS, Player, Creature
from evolution import clear

def intelligence(player: Player, num_of_dchar) -> int:
    pass

def attack(player: Player, players: list, creature: Creature) -> tuple:
    players_id = [player.get_id() for player in players]
    
    print(f'Okay, {str(player)}. You are going to attack someone.')
    
    while True:
        player_id, creature_id = input(f'Enter player id then creature id (#player_id#creature_id):\n> ').split('#')
        
        if player_id.isdigit() and creature_id.isdigit():
            player_id = int(player_id)
            creature_id = int(creature_id)
        
    if player_id in players and player_id != player.get_id():
        aim_player = players[players_id.index(player_id)]
        aim_creature = aim_player.creatures_list[aim_player.get_creatures.index(creature_id)]
        characters = aim_player.get_characters()

        attacker_char = creature.get_characters()

        defense_char = []
        for char in characters:
            if char in ORDERS['been_eating']:
                defense_char.append(char)
        
        attacker_size = sum(creature.get_info()[:2]) if '集群狩猎' in attacker_char else creature.get_info()[1]
        defender_size = aim_creature.get_info[1] if '硬壳' not in defense_char else aim_creature.get_info[1] + 4
        if attacker_size > defender_size:      
            if '智力' in attacker_char:
                choice = input('You have 智力, do you want to use it?\n> ').lower()
                if choice == 'yes' or choice == 'y':
                    for i in range(intelligence(player, len(defense_char))):
                        defense_char.pop()
            
            if '攀爬' in defense_char and '攀爬' in attacker_char:
                print('You have 攀爬! Yeh! The aim\'s 攀爬 is useless now!')
                defense_char.remove('攀爬')
            
            if not defense_char:
                print(f'Attacked {str(aim_creature)}!')
                aim_creature.update_info(attr='population', is_add=False)
                
                return True, aim_creature.get_info[1]

        else:
            print('Oh, no! Your size is too low!')
            print(f'Your size: {attacker_size}')
            print(f'Your aim\'s size: {defender_size}')
            
            return False, 
        
def ask_eat(players: list, water_hole: int, deck: list) -> int:
    attack_num = 0
    for player in players:
        for creature in player.creatures_list:
            while True:
                clear(deck=deck, pond=water_hole, players=players)
                choices = input('Eat more?\n> ').lower()
                if choices == 'yes' or choices == 'y':
                    try:
                        if creature.get_info()[2]:
                            attack_result = attack(player, players, creature)
                            if attack_result[0]:
                                creature.eat(attack_result[1])
                        
                        elif water_hole:
                            water_hole -= 1
                            creature.eat()
                    
                    except:
                        break

                else:
                    break
    
    return attack_num
