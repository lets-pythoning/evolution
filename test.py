from unittest import TestCase, main
from game_utils import attack, players, eat
from cards import AdiposeTissue, Climb, Carnivorous, Foraging, water_hole, Creature, Player
from debug_utils import can_attack

class TestAttack(TestCase):
    
    def testAttack(self):
        player_hunter = players[0]
        player_aim = players[1]

        hunter = player_hunter.creatures[0]
        aim = player_aim.creatures[0]
        
        adipose = AdiposeTissue(player=player_hunter)
        climb = Climb(player=player_aim)
        hunter_climb = Climb(player=player_hunter)
        carnivorous = Carnivorous(player=player_hunter)
        
        hunter.size = 3
        hunter.add_feature(hunter_climb)
        hunter.add_feature(adipose)
        hunter.add_feature(carnivorous)
        player_hunter.announce()
        
        aim.size = 2
        aim.population = 2
        aim.add_feature(climb)
        player_aim.announce()
        
        self.assertTrue(can_attack(hunter, aim))
        
        attack(hunter)

        self.assertEqual(aim.population, 1)
        self.assertEqual(hunter.food_num, 1)
        self.assertFalse(hunter.is_full)
        self.assertEqual(hunter.features[-1].extra_food, 1)
    
    def testEatGrass(self):
        global water_hole
        
        player = players[0]
        
        foraging = Foraging(player=player)
        grass_eater = Creature(id_=2, player=player)
        
        water_hole += 1
        
        grass_eater.add_feature(foraging)
        grass_eater.eat(1)
        
        self.assertEqual(water_hole, 1)
        self.assertTrue(grass_eater.is_full)
        self.assertEqual(grass_eater.food_num, 1)
    
    def testEat(self):
        global water_hole
        
        water_hole += 2
        
        player = players[0]
        player.next_round()
        
        player.creatures[0].is_carnivorous = False
        
        eat(player)

if __name__ == "__main__":
    main()
