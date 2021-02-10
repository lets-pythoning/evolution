from random import choice
from time import sleep
import os
from utils import CARDS, CONSTANTS, ORDERS, Player, Creature
from attack_and_defense import eat
from output import ask_add_character, ask_food_card, attack, output_info

def render_deck() -> list:
    deck = []
    while len(deck) != CONSTANTS['CARDS_NUM']:
        card = choice(CARDS)
        if deck.count(card) < CONSTANTS['SINGLE_CARD_LIMIT']:
            deck.append(choice(CARDS))
    
    return deck

def clear(deck: list, pond: int, players: list) -> None:
    os.system('cls')
    output_info(deck, pond, players)

def run_game() -> None:
    deck = render_deck()
    water_hole = 0
    water_hole_temp = 0
    
    players = [Player(number + 1) for number in range(CONSTANTS['PLAYER_NUM'])]
    turn = 1
    while deck:
        print(f'This is turn {turn} now.')
        for player in players:
            print(f'{str(player)} on the move.')
            
            if turn == 1:
                player.add_creature(Creature(id=1, population=1, size=1))
            
            cards_num = 3 + len(player.creatures_list)
            if len(deck) >= cards_num:
                for i in range(cards_num):
                    card = [choice(deck)]
                    
                    player.add_cards(card)
                    deck.remove(card[0])
                
            else:
                player.add_cards(deck)
                deck = 0

            print(f'{str(player)} get {cards_num} cards from the deck.')
            print(f'Deck has {len(deck)} cards left.')
            
            sleep(3)
        
        for player in players:
            clear(deck, water_hole, players)
            
            ask_add_character(player)
            water_hole_temp += ask_food_card(player)
            
            clear(deck, water_hole, players)
        
        water_hole += water_hole_temp
        clear(deck, water_hole, players)
        for player in players:
            for creature in player.creatures_list:
                characters = creature.characters
                if '多产' in characters and water_hole and creature.get_info()[0] != 6:
                    creature.update_info(attr='population', is_add=True)
                if '长颈' in characters and not creature.get_info()[2]:
                    creature.eat()

        clear(deck, water_hole, players)
        eat(players, water_hole)

        clear(deck, water_hole, players)
        for player in players:
            n = 0
            for creature in player.creatures_list:
                characters = creature.characters
                if '食腐' in characters:
                    creature.eat(num=attack_num)
                if '觅食' in characters and creature.get_info[3]:
                    creature.eat()
                if '协作' in characters and player.creatures_list[-1].get_info[4] != creature.get_info[4]:
                    player.creatures_list[n + 1].eat()
                    
                n += 1
        
        turn += 1

run_game()
