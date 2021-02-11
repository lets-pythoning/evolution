from json import dump
from components import Status

def save_game(status: Status) -> dict:
    players = {}
    for player in status.players:
        creatures = {}
        for creature in player.creatures:
            creatures[str(creature)] = {
                'id':creature.id,
                'population':creature.population,
                'size':creature.size,
                'features':creature.feature,
                'real_features':creature.real_features,
                'hidden_features':creature.hidden_features
            }
        
        players[str(player)] = {
            'is_first': player.is_first,
            'cards': player.cards,
            'id':player.id,
            'creature':creatures
        }
    
    deck = []
    for card in status.deck.cards:
        deck.append({
            'name':card.name,
            'is_ignored':card.is_ignored,
            'food_point':card.food_point
        })
    
    data = {
        'players':players,
        'deck':deck,
        'water_hole':status.water_hole
    }
    
    dump(data, 'game.json')
    
    return data
