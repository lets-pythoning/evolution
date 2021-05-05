from cards import *

def can_attack(hunter: Creature, aim: Creature) -> bool:
    disabled = [False] * len(aim.features)
    for index, aim_feature in enumerate(aim.features):
        if aim_feature.been_attack(hunter):
            disabled[index] = True

        flag_list = []
        hunter.features.sort(key=lambda card: card.index)
        for hunter_feature in hunter.features:
            flag_list.append(hunter_feature > aim_feature)

        if not any(flag_list):
            disabled[index] = True
            
    if hunter.size > aim.size and not (False in disabled):
        return True

    return False

def easy_debug(
    population_tuple: Tuple[int, int],
    size_tuple: Tuple[int, int],
    hunter_features: Tuple[str, ...],
    aim_features: Tuple[str, ...]
) -> bool:
    player = Player(id_=1)
    hunter = Creature(player=player)
    aim = Creature(player=player)
    
    player.creatures.extend([hunter, aim])
    
    for feature in hunter_features:
        feature = eval(feature + '(player=player)')
        hunter.add_feature(feature)
    
    for feature in aim_features:
        feature = eval(feature + '(player=player)')
        aim.add_feature(feature)
    
    hunter.population, aim.population = population_tuple[0], population_tuple[1]
    hunter.size, aim.size = size_tuple[0], size_tuple[1]
    
    player.announce()
    
    return can_attack(hunter, aim)

if __name__ == '__main__':
    print(easy_debug(
        (1, 1),
        (3, 2),
        ('Carnivorous', 'GroupHunting'),
        ('AdiposeTissue', )
    ))
