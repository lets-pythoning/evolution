from random import randint, shuffle

from constants import *
from errors import Dead, OwnerError

water_hole = 0

def isinstance_decorator(type_: object) -> object:
    def call_function(function: object) -> object:
        def wrapper(obj: object):
            if isinstance(obj, type_):
                function(obj)
            else:
                raise TypeError(f'obj must be {type_.__name__} object: {type(obj)}')
        
        return wrapper
    
    return call_function

class Card(object):

    __slots__ = ['point', 'index', 'name', 'extra_food', 'root', 'father']

    def __init__(self, player, point=None, index=1):
        if isinstance(point, int):
            self.point = randint(*point)
        else:
            self.point = randint(-3, 8)

        self.index = index
        self.name = 'WildCard'

        # 如果father为Player对象, 那就说明牌未被放置, 反之亦然.
        # root为最高级, 一定是Player对象.

        self.root = player
        self.father = player

    def __repr__(self) -> str:
        return f'<Card name={self.name} point={self.point}>'

    def __str__(self) -> str:
        return self.name + f' ({self.point})'

    def __gt__(self, other) -> bool:
        return False

    def on_place(self, creature):
        self.father = creature

    def been_attack(self, hunter) -> bool:
        return True

    def eat(self, food_num: int): ...
    def next_round(self): ...
    def announce(self): ...
    def on_remove(self): ...

class Player(object):

    __slots__ = ['creatures', 'id_', 'cards', 'point']

    def __init__(self, id_: int):
        self.creatures = [Creature(id_=1, player=self)]
        self.id_ = id_
        self.point = 0
        self.cards = []

    def __str__(self) -> str:
        return f'Player ({self.id_})'

    def __repr__(self) -> str:
        return f'<Player id_={self.id_} point={self.point}>'

    def get_neighbors(self, id_: int) -> dict:
        creature_ids = list(map(lambda creature: creature.id, self.creatures))
        index = creature_ids.index(id_)
        neighbors = {'left': None, 'right': None}
        if index != 0:
            neighbors['left'] = self.creatures[index - 1]

        try:
            neighbors['right'] = self.creatures[index + 1]
        except IndexError:
            pass

        return neighbors

    def announce(self):
        for creature in self.creatures:
            creature.announce()

    def next_round(self):
        for creature in self.creatures:
            try:
                creature.next_round()
                
            except Dead as e:
                print(e)
                del creature
            
class Creature(object):
    
    __slots__ = ['id_', 'size', 'population', 'hidden_features', 'features', 'father', 'is_full', 'is_carnivorous', 'food_num']
    
    def __init__(self, id_: int, player: Player):
        self.id_ = id_
        self.size = 1
        self.population = 1
        self.hidden_features = []
        self.features = []
        self.father = player
        self.is_full = False
        self.is_carnivorous = False
        self.food_num = 0
    
    def __str__(self) -> str:
        return f'Creature ({self.id_})'
    
    def __repr__(self) -> str:
        return f'<Creature id_={self.id_} population={self.population} size={self.size} father={repr(self.father)} is_carnivorous={self.is_carnivorous} food_num={self.food_num}>'

    def add_feature(self, feature):
        # 判断是否是未放置且自己拥有的牌.
        if feature.root == self.father:
            if feature not in self.features and feature not in self.hidden_features:
                if len(self.features) < 3:
                    feature.father = self
                    feature.on_place(self)
                    
                    self.hidden_features.append(feature)
                
                else:
                    raise IndexError('Features more than 3!')
            
            else:
                raise ValueError(f'Same feature {str(feature)} been placed!')
            
        else:
            raise OwnerError('Not owned card been placed!')
    
    def delete_feature(self, index: int):
        if isinstance(index, int):
            if index >= 0:
                # 在IO判断时, hidden_features永远在features后面, 所以索引较大. 
                # 从普通人的角度来看, 索引从1开始, 所以减一
                
                length_of_features = len(self.features)
                if length_of_features >= index:
                    feature = self.features.pop(index - 1)
                elif len(self.features) + len(self.hidden_features) >= index:
                    feature = self.hidden_features.pop(index - length_of_features - 1)
                else:
                    raise IndexError(f'Index out of range: {index - 1}')

                feature.on_remove()
                del feature
            
            else:
                raise IndexError(f'Index out of range: {index}')
        
        else:
            # 尝试类型转换.
            
            try:
                index = int(index)
            except ValueError as e:
                raise ValueError('Index not int!') from e
            else:
                self.delete_feature(index)
    
    def announce(self):
        self.features += self.hidden_features
        self.features.sort(key=lambda feature: feature.index)
        
        for feature in self.features:
            feature.announce()
    
    def next_round(self):
        self.population = self.food_num
        self.father.point += self.food_num
        self.food_num = 0
        if not self.population:
            raise Dead(self.__str__() + ' dead.')
            
        for feature in self.features:
            feature.next_round()
    
    def eat(self, food_num: int):
        # 先累加食物, 超出也没关系, 如果没有脂肪组织, 后面会自动变成种群数量.
        
        global water_hole

        if self.is_carnivorous:
            self.food_num += food_num
        
        elif water_hole >= food_num:
            self.food_num += food_num
            water_hole -= food_num
            
        self.features.sort(key=lambda feature: feature.index)
        for feature in self.features:
            feature.eat(food_num)
        
        if self.population < self.food_num:
            redundance = self.food_num - self.population
            water_hole += redundance
            self.food_num = self.population
            
        self.check_full()
    
    def check_full(self):
        if self.food_num >= self.population:
            if 'AdiposeTissue' in map(lambda feature: feature.name, self.features):
                return

            self.is_full = True
            return

__all__ = ['Creature', 'Card', 'Player', 'isinstance_decorator', 'water_hole']
