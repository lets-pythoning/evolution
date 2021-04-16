from bases import Card, state
from os import system

def get_card(cards: list) -> Card:
    print([str(card) for card in cards], '\n')
    
    while True:
        index = input('Input card index: ')
        try:
            index = int(index)
            card = cards[index - 1]
            
            return card
        
        except IndexError:
            print('Index out of range, choose again.')
        
        except ValueError:
            print('Index not an integer, choose again.')

def get_food_card() -> list:
    cards = []
    for player in state['players']:
        card = get_card(player.cards)
        cards.append(card)
    
    return cards

def fresh():
    system('cls')
    
    for player in state['players']:
        print(str(player))
        for creature in player.creatures:
            print(f' - {str(creature)}: {[str(feature) for feature in creature.features]}')

    print(f'water hole: {state["water_hole"]}')
    print(f'deck: {len(state["deck"])}')
