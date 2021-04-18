from unittest import TestCase, main
from game_utils import attack, players
from cards import AdiposeTissue, Climb, Carnivorous, Foraging, water_hole, Creature
from debug_utils import can_attack

class TestAttack(TestCase):
    
    def setUp(self):
        self.player_hunter = players[0]
        self.player_aim = players[1]

        self.hunter = self.player_hunter.creatures[0]
        self.aim = self.player_aim.creatures[0]
        
        self.grass_eater = Creature(id_=2, player=self.player_hunter)
        
    def testAttack(self):
        adipose = AdiposeTissue(player=self.player_hunter)
        climb = Climb(player=self.player_aim)
        hunter_climb = Climb(player=self.player_hunter)
        carnivorous = Carnivorous(player=self.player_hunter)
        
        self.hunter.size = 3
        self.hunter.add_feature(hunter_climb)
        self.hunter.add_feature(adipose)
        self.hunter.add_feature(carnivorous)
        self.player_hunter.announce()
        
        self.aim.size = 2
        self.aim.population = 2
        self.aim.add_feature(climb)
        self.player_aim.announce()
        
        self.assertTrue(can_attack(self.hunter, self.aim))
        
        attack(self.hunter)

        self.assertEqual(self.aim.population, 1)
        self.assertEqual(self.hunter.food_num, 1)
        self.assertFalse(self.hunter.is_full)
        self.assertEqual(self.hunter.features[-1].extra_food, 1)
    
    def testEat(self):
        global water_hole
        
        water_hole += 1
        
        foraging = Foraging(player=self.player_hunter)
        
        self.grass_eater.add_feature(foraging)
        self.grass_eater.eat(1)
        
        self.assertEqual(water_hole, 1)
        self.assertTrue(self.grass_eater.is_full)
        self.assertEqual(self.grass_eater.food_num, 1)

if __name__ == "__main__":
    main()
