from random import randint
from constants import CONSTANTS, CARDS_SET

class CreatureSeq(object):
    
    def __init__(self, owner):
        self.owner = owner
        self.creatures = []
        self.creatures_by_id = []
    
    def __str__(self) -> str:
        return [str(creature) for creature in self.creatures]
    
    def add_creature(self, creature):
        if creature.id not in self.creatures_by_id:
            self.creatures.append(creature)
            self.creatures_by_id = self.get_ids()
        
        else:
            raise ValueError('Creature already exists!')
    
    def delete_creature(self, creature):
        self.creatures.remove(creature)
        self.creatures_by_id = self.get_ids()
    
    def get_ids(self):
        return [creature.id for creature in self.creatures]
    
    def left(self, id: int):
        location = self.creatures_by_id.index(id)
        if location == 0:
            return None
        else:
            return self.creatures[location - 1]
    
    def right(self, id: int):
        location = self.creatures_by_id.index(id)
        if location == len(self.creatures) - 1:
            return None
        else:
            return self.creatures[location + 1]

class Creature(object):
    
    def __init__(self, id: int, creature_seq: CreatureSeq):
        self.id = id
        self.population = 1
        self.size = 1
        self.father = creature_seq
        self.features = set()
        self.real_features = set()
        self.hidden_features = set()
        self.neighbor = [
            self.father.left(self.id),
            self.father.right(self.id)
        ]
    
    def __str__(self) -> str:
        return f'Creature{self.id}'
    
    def add_feature(self, feature) -> bool:
        self.features += self.hidden_features
        
        if feature not in self.features and feature not in self.hidden_features:
            if len(self.features) + len(self.hidden_features) < CONSTANTS['FEATURE_MAX']:
                feature.check_ignore()
                if feature.is_ignored:
                    self.hidden_features.add(feature)
                    
                    return True
                
                else:
                    self.real_features.add(feature)
                    self.hidden_features.add(feature)
                    
                    return True
            
            else:
                return False
        
        else:
            return False

class Feature(object):
    
    def __init__(self, food_point_range=(-3, 8)):
        self.name = None
        self.is_ignored = False
        self.food_point = randint(food_point_range[0], food_point_range[1])
        self.creature = None
        
        self.check_ignore()
    
    def __str__(self) -> str:
        return self.name

    def check_ignore(self):
        if self.creature and self.name:
            if self.creature.is_herbivore and self.name in CARDS_SET['need_carnivore']:
                self.is_ignored = True
            elif not self.creature.is_herbivore and self.name in CARDS_SET['need_herbivore']:
                self.is_ignored = True
            elif self.creature.neighbor.count(None) == 2 and self.name in CARDS_SET['need_neighbor']:
                self.is_ignored = True
            else:
                return None

class Deck(object):
    
    def __init__(self):
        self.cards = []
        self.cards_num = 0
    
    def __str__(self):
        return [str(card) for card in self.cards]

    def add_cards(self, cards: list):
        for card in cards:
            if not isinstance(card, Feature):
                raise ValueError('"cards" is not combinated just by object of Card')
            
        self.cards_num += len(cards)
        self.cards += cards

    def get_cards(self, num: int) -> list:
        if num >= self.cards_num:
            return self.cards
        else:
            return self.cards[:num]

class Player(object):
    
    def __init__(self, id: int):
        self.is_first = False
        self.cards = []
        self.id = id
        self.creatures = CreatureSeq(self)
    
    def add_creature(self, creature: Creature):
        self.creatures.add_creature(creature)
    
    def delete_creature(self, creature):
        self.creatures.delete_creature(creature)
    
    def get_cards(self, deck: Deck):
        cards_num = CONSTANTS['LOWER_LINE_OF_CARDS'] + len(self.creatures.creatures)
        self.cards.append(deck.get(cards_num))

    def check_deletion(self) -> bool:
        for creature in self.creatures.creatures:
            if creature.population == 0:
                self.delete_creature(creature)
                
                return True

class Status(object):
    
    def __init__(self, players: list):
        self.players = players
        self.deck = Deck()
        self.water_hole = 0
    
    def read(self, status: Status):
        self.players = status.players
        self.deck = status.deck
        self.water_hole = status.water_hole

__all__ = ['CreatureSeq', 'Creature', 'Feature', 'Deck', 'Player', 'Status']
