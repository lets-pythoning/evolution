class Creature(object):
    
    def __init__(self, id: int):
        self.id = id
        self.population = 1
        self.size = 1
        self.food = 0
        self.point = 0
    
    def __str__(self) -> str:
        return f'Creature{self.id}'
    
    def next_round(self) -> bool:
        self.population = self.food
        self.point += self.food
        self.food = 0
        if self.population == 0:
            print(f'Game over!\n{str(self)} lose!')
            
            return True
        
        return False

def attack(hunter: Creature, creature_list: list):
    for creature in creature_list:
        if creature.id != hunter.id:
            aim = creature
            
    if hunter.size > aim.size:
        print(f'{str(hunter)} attack successfully.')
        
        aim.population -= 1
        if hunter.population - hunter.food > aim.size:
            hunter.food = hunter.population
        else:
            hunter.food += aim.size
    
    else:
        print('Attack failed.')

creature1 = Creature(1)
creature2 = Creature(2)
creature_list = [creature1, creature2]
while True:
    while creature1.food < creature1.population or creature2.food < creature2.population:
        for creature in creature_list:
            # Because there isn't a complete decision to which creature can do what,
            # so some times if a creature is not full, it can increase its size or population
            # many times.
            
            if creature.food < creature.population:
                choice = input(f'{str(creature)}, what do you want to do?\n>').lower()
                if choice == 'attack':
                    attack(creature, creature_list)
                elif choice == 'population':
                    creature.population += 1
                else:
                    creature.size += 1

    # Because the simple of this model. If the creature already died in the attack,
    # they will still be able to kill another creature and win the game.
    
    flag = False
    for creature in creature_list:
        flag = flag or creature.next_round()
        
    if flag:
        break
