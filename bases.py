from os import system
from random import randint, shuffle
from sys import argv
from time import sleep
from typing import Any, Callable, List, Tuple, Union

from constants import *
from errors import Dead, OwnerError

LD = LANGUAGE_DICT
ERROR = LD['error_message']
CARD = LD['card']
BASE = LD['base']

water_hole = 0

def isinstance_decorator(type_: Any) -> Callable:
    def call_function(function: Callable) -> Callable:
        def wrapper(obj: Any):
            if isinstance(obj, type_):
                function(obj)
            else:
                raise TypeError(f'obj must be {type_.__name__} object: {type(obj)}')
        
        return wrapper
    
    return call_function

def water_hole_control(number: int = 0) -> int:
    # 因为全局变量的关系, 这里规定一个对水塘进行设置的API
    
    global water_hole
    
    water_hole += number
    if water_hole < 0:
        water_hole = 0
    
    return water_hole

class Card(object):

    __slots__ = ['point', 'index', 'name', 'extra_food', 'root', 'father']

    def __init__(self, player, point: Tuple[int, int] = None, index: int = 1):
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

    def on_attack(self, aim): ...
    def eat(self, food_num: int): ...
    def next_round(self): ...
    def announce(self): ...
    def on_remove(self): ...

class Player(object):

    __slots__ = ['creatures', 'id_', 'cards', 'point']

    def __init__(self, id_: int):
        self.creatures = [Creature(player=self)]
        self.id_ = id_
        self.point = 0
        self.cards = []

    def __str__(self) -> str:
        return BASE['player_as_string'].format(self.id_)

    def __repr__(self) -> str:
        return f'<Player id_={self.id_} point={self.point}>'

    def get_neighbors(self, creature) -> dict:
        index = self.creatures.index(creature)
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
                
                self.creatures.remove(creature)
                del creature

class Creature(object):
    
    __slots__ = ['size', 'population', 'hidden_features', 'features', 'father', 'is_full', 'is_carnivorous', 'food_num']
    
    def __init__(self, player: Player):
        self.size = 1
        self.population = 1
        self.hidden_features = []
        self.features = []
        self.father = player
        self.is_full = False
        self.is_carnivorous = False
        self.food_num = 0
    
    def __str__(self) -> str:
        return BASE['creature_as_string'].format(self.father.creatures.index(self) + 1)
    
    def __repr__(self) -> str:
        return f'<Creature population={self.population} size={self.size} father={repr(self.father)} is_carnivorous={self.is_carnivorous} food_num={self.food_num}>'
    
    def add_feature(self, new_feature):
        # 判断是否是未放置且自己拥有的牌.
        if new_feature.root == self.father:
            feature_names = [feature.name for feature in self.features + self.hidden_features]
            if new_feature.name not in feature_names:
                if len(feature_names) < 3:
                    new_feature.father = self
                    new_feature.on_place(self)
                    
                    self.hidden_features.append(new_feature)
                
                else:
                    raise IndexError(ERROR['features_more_than_three'])
            
            else:
                raise ValueError(ERROR['same_feature'].format(str(new_feature)))
            
        else:
            raise OwnerError('Not owned card been placed!')
    
    def delete_feature(self, feature):
        try:       
            self.features.remove(feature)
        except ValueError as e:
            raise OwnerError(f'Not owned feature: {repr(feature)}') from e

        feature.on_remove()
        del feature
    
    def announce(self):
        self.features += self.hidden_features
        self.hidden_features = []
        self.features.sort(key=lambda feature: feature.index)
        
        for feature in self.features:
            feature.announce()
    
    def next_round(self):
        self.population = self.food_num
        self.father.point += self.food_num
        self.food_num = 0
        self.is_full = False
        if self.population <= 0:
            raise Dead(ERROR['creature_dead'].format(str(self.father), str(self)))

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
        
        else:
            return

        self.features.sort(key=lambda feature: feature.index)
        for feature in self.features:
            feature.eat(food_num)

        for creature in self.father.creatures:
            creature.check_full()

    def check_full(self):
        global water_hole
        
        if self.population <= self.food_num:
            redundance = self.food_num - self.population
            water_hole += redundance
            self.food_num = self.population
            
            if CARD['adipose_tissue']['name'] in map(lambda feature: feature.name, self.features):
                return

            self.is_full = True
