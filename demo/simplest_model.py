from random import randint

class Creature(object):
    
    def __init__(self):
        self.population = 1
        self.size = 1
        self.food = 0
        self.is_full = False
        self.is_alive = True
    
    def eat(self):
        if self.food < self.population:
            self.food += 1
        else:
            self.is_full = True
    
    def next_round(self):
        self.population = self.food
        self.food = 0
        if self.population == 0:
            self.is_alive = False
        
def play_game(water_hole: int):
    creature1 = Creature()
    creature2 = Creature()
    
    while True:
        if water_hole:
            creature1.eat()
            water_hole -= 1
            
            if randint(1, 3) == 1:
                creature1.population += 1
            
        else:
            break
        
        if water_hole:
            creature2.eat()
            water_hole -= 1
            
            if randint(1, 3) == 1:
                creature2.population += 1
                
        else:
            break
    
    creature1.next_round()
    creature2.next_round()
    
    if not creature1.is_alive or not creature2.is_alive:
        print('Game Over!')
        if creature1.is_alive:
            print('Creature1 win!')
            return True

        print('Creature2 win!')
        return True

    return water_hole

flag = False
water_hole = 0
while not flag:
    water_hole += 2
    
    flag = play_game(water_hole)
    if type(flag) == type(1):
        water_hole = flag
        flag = False
