from bases import Creature

def can_attack(hunter: Creature, aim: Creature) -> bool:
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
        if hunter.size >= aim.size:
            return True
    
    return False

if __name__ == '__main__':
    from cards import *
    
    player = Player(id_=1)
    wildcard = Card(player=player)
    player.cards.append(wildcard)

    hunter = Creature(id_=1, player=player)
    aim = Creature(id_=2, player=player)
    
    intelligence = Intelligence(player=player)
    carnivorous = Carnivorous(player=player)
    hunter.add_feature(intelligence)
    hunter.add_feature(carnivorous)
    
    climb = Climb(player=player)
    aim.add_feature(climb)
    
    player.announce()

    print(can_attack(hunter, aim))
