from bases import *
from io_utils import get_card

class Carnivorous(Card):

    def __init__(self, player: Player, point=(0, 5), index=1):
        super().__init__(player, point, index)
        self.name = 'Carnivorous'

    def on_place(self, creature: Creature):
        super().on_place(creature=creature)
        self.father.is_carnivorous = True

    def on_remove(self):
        self.father.is_carnivorous = False

class Intelligence(Card):

    def __init__(self, player: Player, point=(-1, 3), index=4):
        super().__init__(player, point, index)
        self.name = 'Intelligence'

    def __gt__(self, other: Card) -> bool:
        if not self.father.is_carnivorous:
            return False

        if self.root.cards != []:
            choice = input(
                'You have Intelligence. Do you want to use? ').lower()
            if choice in ('yes', 'y'):
                input('Intelligence used, keepout! ')

                card = get_card(self.root.cards)
                self.root.cards.remove(card)

                return True

            return False

        print('No card!')
        return False

class GroupHunting(Card):

    def __init__(self, player: Player, point=(-3, 2), index=1):
        super().__init__(player, point, index)
        self.name = 'GroupHunting'

    def __gt__(self, other: Card) -> bool:
        self.father.size += self.father.population
        return False
    
class Ambush(Card):
    
    def __init__(self, player: Player, point=(-3, 1), index=1):
        super().__init__(player, point, index)
        self.name = 'Ambush'
    
    def __gt__(self, other: Card) -> bool:
        if other.__class__.__name__ == 'WarningSignal':
            return True
        
        return False

class Cooperation(Card):

    def __init__(self, player: Player, point=(2, 5), index=2):
        super().__init__(player, point, index)
        self.name = 'Cooperation'

    def eat(self, food_num: int):
        right_neighbor = self.root.get_neighbors(self.father.id)['right']
        if right_neighbor and not right_neighbor.is_carnivorous:
            right_neighbor.food_num += 1

class AdiposeTissue(Card):

    def __init__(self, player: Player, point=(0, 4), index=4):
        super().__init__(player, point, index)
        self.name = 'AdiposeTissue'
        self.extra_food = 0

    def eat(self, food_num: int):
        if food_num + self.father.food_num > self.father.population:
            redundance = food_num + self.father.food_num - self.father.population
            if self.extra_food + redundance > self.father.size:
                self.extra_food = self.father.size
                self.father.is_full = True

                state['water_hole'] += self.extra_food + \
                    redundance - self.father.size

            else:
                self.extra_food += redundance

    def next_round(self):
        self.father.food_point = self.extra_food
        self.extra_food = 0
        
class LongNeck(Card):
    
    def __init__(self, player: Player, point=(5, 9), index=1):
        super().__init__(player, point, index)
        self.name = 'LongNeck'
    
    def announce(self):
        self.father.food_num += 1

class Symbiosis(Card):
    
    def __init__(self, player: Player, point=(2, 8), index=2):
        super().__init__(player, point, index)
        self.name = 'Symbiosis'
    
    def been_attack(self, hunter: Creature) -> bool:
        right_neighbor = self.root.get_neighbors(self.father.id_)['right']
        if right_neighbor:
            if right_neighbor.size > self.father.size:
                return False
        
        return True

class HardShell(Card):
    
    def __init__(self, player: Player, point=(-1, 8), index=2):
        super().__init__(player, point, index)
        self.name = 'HardShell'
    
    def been_attack(self, hunter: Creature) -> bool:
        self.father.size += 4
        return True

class Horn(Card):
    
    def __init__(self, player: Player, point=(1, 5), index=1):
        super().__init__(player, point, index)
        self.name = 'Horn'
    
    def been_attack(self, hunter: Creature) -> bool:
        hunter.population -= 1
        return True

class CaveDwelling(Card):
    
    def __init__(self, player: Player, point=(1, 5), index=1):
        super().__init__(player, point, index)
        self.name = 'CaveDwelling'
    
    def been_attack(self, hunter: Creature) -> bool:
        if self.father.food_num < self.father.population:
            return True

        return False

class Climb(Card):
    
    def __init__(self, player: Player, point=(1, 4), index=1):
        super().__init__(player, point, index)
        self.name = 'Climb'

    def been_attack(self, hunter: Creature) -> bool:
        return False

    def __gt__(self, other: Card) -> bool:
        if not self.father.is_carnivorous:
            return False

        if other.__class__.__name__ == self.__class__.__name__:
            return True
        
        return False

class WarningSignal(Card):
    
    def __init__(self, player: Player, point=None, index=1):
        super().__init__(player, point, index)
        self.name = 'WarningSignal'
    
    def been_attack(self, hunter: Creature) -> bool:
        return False

class Foraging(Card):
    
    def __init__(self, player: Player, point=(2, 7), index=3):
        super().__init__(player, point, index)
        self.name = 'Foraging'
    
    def eat(self, food_num: int):
        self.father.food_num += 1

class ClusterDefense(Card):
    
    def __init__(self, player: Player, point=(4, 7), index=1):
        super().__init__(player, point, index)
        self.name = 'ClusterDefense'
    
    def been_attack(self, hunter: Creature) -> bool:
        if hunter.population > self.father.population:
            return True

        return False
