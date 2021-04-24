from game_utils import *

def play():
    while is_deck():
        split_cards()
        private_move()
        announce()
        
        flag = eat_together()
        while flag:
            flag = eat_together()
        
        next_round()
