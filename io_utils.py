from components import Player, Creature, Status
from constants import card_renderer
from constants import CARDS, CONSTANTS

def parser(inpution: str, player: Player) -> tuple:
    if len(inpution.split()):
        action, feature, creature = inpution.split
        if action in ['add', 'delete']:
            try:
                feature = card_renderer(feature)
                creature = player.creatures.creatures[player.creatures.creatures_by_id.index(int(creature))]
                
                assert feature in CARDS
                assert feature not in creature.features
            
            except:
                return ('not complete', )
            
            else:
                return (action, feature, creature)

def ask_for_deletion(creature: Creature):
    while True:
        print(f'Creature values: population = {creature.population} size = {creature.size}')
        reward = input('You delete a feature, what do you want to gain?\n> ')
        if reward == 'population':
            if creature.population < CONSTANTS['MAX_PS']:
                creature.population += 1
                print('Ok.')
                
                return None
            
            else:
                print('Population is maximum now.')
                continue
        
        elif reward == 'size':
            if creature.size < CONSTANTS['MAX_PS']:
                creature.size += 1
                print('Ok.')
                
                return None
            
            else:
                print('Size is maximum now.')
                continue
        
        elif reward == 'creature':
            creature_seq = creature.father
            
            print(f'Creatures: {str(creature_seq)}')
            index = input('Where do you want to place the new creature?\n(Enter index)> ')
            
            if index.isnumeric():
                index = int(index)
                
            else:
                print('Try to enter a number next time.')
                continue
            
            if index >= 1 and index <= len(creature_seq.creatures):
                creature = Creature(max(creature_seq.creatures_by_id) + 1, creature_seq)
                
                creature_seq.add_creature(creature, index - 1)
                creature.setup_neighbor()
                
                return None
                
            else:
                print('Index not valid')
                continue
        
        else:
            print('Not valid!')
            continue

def change_single_feature(player: Player, n: int):
    while True:
        try:
            action, feature, creature = parser(input(f'{n} > ').lower(), player)
            
        except ValueError:
            print('Sorry, not valid. Try again.')
            continue
        
        else:
            if action == 'add':
                feature.creature = creature
                assert creature.add_feature(feature)
            
            else:
                assert creature.delete_feature(feature)
                del feature
                ask_for_deletion(creature)
            
            return None

def change_creature_feature(player: Player):
    n = 1
    while player.cards > 1:
        change_single_feature(player, n)
        n += 1

def ask_food_card(player: Player) -> int:
    food_points_list = [card.food_point for card in player.cards]
    
    print(f'\nThese are your cards\' food point: {food_points_list}')
    print(f'These are your cards: {player.cards}')
    
    while True:
        index = input('Enter index for food card.\n> ')
        if index.isnumeric():
            index = int(index)
            if index >= 1 and index <= len(player.cards):
                return food_points_list[index - 1]
        
        print('Not valid food card index. Try again.')
        continue

def eat_output(output_list: list, player: Player, status: Status):
    while True:
        creatures_output = output_list
        print(f'{str(player)}\'s creatures: {creatures_output}')

        index = input('Enter index:\n> ')
        if index.isnumeric():
            index = int(index)

        else:
            print('Index invalid. Please try again')
            continue

        if index >= 1 and index <= len(player.creatures.creatures):
            if not output_list[index - 1].endwith(')'):
                creature = player.creatures.creatures[index]
                if creature.is_herbivore:
                    eat(status)
                else:
                    attack(status)
                
                return None

            else:
                print('Not allowed creature, please try again.')
                continue

        else:
            print('Index out of limit. Please try again')
            continue

def get_all_creatures(players: list) -> list:
    creatures = []
    for player in players:
        creatures += player.creatures.creatures
    
    return creatures

def is_eating_more(status: Status) -> bool:
    creatures = get_all_creatures(status.players)
    if status.water_hole:
        for creature in creatures:
            if not creature.is_herbivore:
                return True
        
        return None
        
    else:
        for creature in creatures:
            if creature.is_herbivore:
                return False
        
        return None

def attack(status: Status) -> int:
    pass

def eat(status: Status) -> int:
    pass

__all__ = ['change_creature_feature', 'ask_food_card', 'eat_output', 'get_all_creatures']
