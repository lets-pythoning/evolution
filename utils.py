CONSTANTS = {
    'CARDS_NUM':10,
    'SINGLE_CARD_LIMIT':2,
    'PLAYER_NUM':2,
    'MAX_PS':6
}

ORDERS = {
    'been_eating':['穴居', '硬壳', '攀爬', '集群防御'],
    'attack_cards':['智力', '集群狩猎', '攀爬']
}

CARDS = [
    '脂肪组织', '多产', '穴居', '食肉', '硬壳', '攀爬', '集群防御',
    '智力', '集群狩猎', '攀爬', '食腐', '协作', '觅食', '长颈'
]

class Creature(object):
    
    def __init__(self, id, population=1, size=1, character_list=None) -> None:
        self.characters = set(character_list) if character_list else set()
        self.secret_characters = set()
        self._id = id
        self._population = population
        self._size = size
        self._is_creophagism = True if '食肉' in self.characters else False
        self._food = 0
        self._extra_food = 0
    
    def __str__(self) -> str:
        return f'Creature{self._id}'
    
    def get_info(self) -> tuple:
        return self._population, self._size, self._is_creophagism, self._food, self._id

    def get_characters(self) -> set:
        return self.characters
    
    def eat(self, num=1) -> None:
        if self._food < self._population:
            if self._food + num <= self._population:
                self._food = self._food + num 
            else:
                if '脂肪组织' in self.characters and self._extra_food < self._size:
                    self._extra_food = self._extra_food + num if self._extra_food + num <= self._size else self._size   
                else:
                    raise ValueError('Creature already full!')

        elif '脂肪组织' in self.characters and self._extra_food < self._size:
                    self._extra_food = self._extra_food + num if self._extra_food + num <= self._size else self._size   

        else:
            raise ValueError('Creature already full!')
    
    def next_round(self) -> None:
        self._population = self._food
        self._food = 0 + self._extra_food if 0 + self._extra_food < self._population else self._population
        self._extra_food = 0
    
    def add(self, character: str) -> None:
        if character in CARDS:
            if character not in self.characters and character not in self.secret_characters:
                self.secret_characters.add(character)
                if character == '食肉':
                    self._is_creophagism = True
            
            else:
                raise ValueError(f'{character} is already exists!')
            
        else:
            raise UnboundLocalError(f'{character} is not a valid character.')
    
    def delete(self, character: str) -> None:
        if character in CARDS:
            if character in self.characters:
                self.characters.remove(character)
                if character == '食肉':
                    self._is_creophagism == False
            
            else:
                raise ValueError(f'{character} does not exist!')
        
        else:
            raise UnboundLocalError(f'{character} is not a valid character.')
    
    def update_info(self, attr: str, is_add: bool) -> None:
        if attr == 'population':
            if is_add:
                if self._population != CONSTANTS['MAX_PS']:
                    self._population += 1
                else:
                    raise ValueError(f'{attr} is already full. Max is {CONSTANTS["MAX_PS"]}.')
            
            else:
                if self._population != 1:
                    self._population -= 1
        
        elif attr == 'size':
            if is_add:
                if self._size != CONSTANTS['MAX_PS']:
                    self._size += 1
                else:
                    raise ValueError(f'{attr} is already full. Max is {CONSTANTS["MAX_PS"]}.')
        
        else:
            raise UnboundLocalError(f'{attr} is not a valid attr.')

class Player(object):
    
    def __init__(self, id: int) -> None:
        self.creatures_list = []
        self.cards = []
        self._id = id
        self._creatures_num = 0

    def __str__(self) -> str:
        return f'Player{self._id}'

    def add_creature(self, creature: Creature) -> None:
        self.creatures_list.append(creature)
        self._creatures_num += 1

    def add_cards(self, cards: list) -> None:
        self.cards.extend(cards)

    def get_creatures(self) -> tuple:
        return tuple([creature.get_info()[4] for creature in self.creatures_list])
    
    def get_cards(self) -> tuple:
        return tuple(self.cards)
    
    def get_id(self) -> int:
        return id

    def delete_card(self, card: str) -> None:
        if self.cards.count(card):
            self.cards.remove(card)
