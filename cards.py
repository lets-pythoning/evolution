from bases import *

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
            choice = input(f'The aim has {str(other)}, do you want to use Intelligence? ').lower()
            if choice in ('yes', 'y'):
                input('Intelligence used, keepout! ')
                
                cards = self.root.cards
                print([str(card) for card in cards], '\n')

                while True:
                    index = input('Input card index: ')
                    try:
                        index = int(index)
                        card = cards[index - 1]
                        break

                    except IndexError:
                        print('Index out of range, choose again.')

                    except ValueError:
                        print('Index not an integer, choose again.')

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
        right_neighbor = self.root.get_neighbors(self.father)['right']
        if right_neighbor and not right_neighbor.is_carnivorous:
            right_neighbor.check_full()
            if not right_neighbor.is_full:
                if water_hole_control(-1):
                    right_neighbor.food_num += 1

class AdiposeTissue(Card):

    def __init__(self, player: Player, point=(0, 4), index=4):
        super().__init__(player, point, index)
        self.name = 'AdiposeTissue'
        self.extra_food = 0

    def __str__(self) -> str:
        return super().__str__() + f' {self.extra_food} food'

    def eat(self, food_num: int) -> int:
        if self.father.food_num > self.father.population:
            redundance = self.father.food_num - self.father.population
            self.extra_food += redundance
            if self.extra_food >= self.father.size:
                self.father.is_full = True
                self.extra_food = self.father.size
            
    def next_round(self):
        self.root.point += self.extra_food
        self.extra_food = 0
        
class LongNeck(Card):
    
    def __init__(self, player: Player, point=(5, 9), index=1):
        super().__init__(player, point, index)
        self.name = 'LongNeck'
    
    def announce(self):
        if not self.father.is_carnivorous:
            water_hole_control(1)
            self.father.eat(1)
            self.father.check_full()

class Symbiosis(Card):
    
    def __init__(self, player: Player, point=(2, 8), index=2):
        super().__init__(player, point, index)
        self.name = 'Symbiosis'
    
    def been_attack(self, hunter: Creature) -> bool:
        right_neighbor = self.root.get_neighbors(self.father)['right']
        if right_neighbor and right_neighbor.size > self.father.size:
            return False
        
        return True

class HardShell(Card):
    
    def __init__(self, player: Player, point=(-1, 8), index=2):
        super().__init__(player, point, index)
        self.name = 'HardShell'
    
    def been_attack(self, hunter: Creature) -> bool:
        if hunter.size > self.father.size + 4:
            return True

        return False

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
        if not self.father.is_carnivorous:
            if water_hole_control(-1):
                self.father.food_num += 1

class ClusterDefense(Card):
    
    def __init__(self, player: Player, point=(4, 7), index=1):
        super().__init__(player, point, index)
        self.name = 'ClusterDefense'
    
    def been_attack(self, hunter: Creature) -> bool:
        if hunter.population > self.father.population:
            return True

        return False
