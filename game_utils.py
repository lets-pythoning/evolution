from cards import *

GAME = LD['game_util']

# ---------------- #
#  Lower Function  #
# ---------------- #

def _render_card(name: str) -> object:
    try:
        obj = eval(name + '("in deck")')
    except NameError as e:
        raise NameError(f'No card named {name}.') from e

    return obj

deck = [_render_card(name) for name in CARDS * SINGLE_CARD_NUM]
players = [Player(id_=id_) for id_ in range(1, PLAYER_NUM + 1)]

shuffle(deck)

def _get_card(cards: list) -> Card:
    print([str(card) for card in cards], '\n')

    while True:
        index = input(GAME['which_card'])
        try:
            index = int(index)
            card = cards[index - 1]

            return card

        except IndexError:
            print(ERROR['card_index_overflow'])
        except ValueError:
            print(ERROR['index_not_interger'])

def _get_creature(creatures: list) -> Creature:
    if len(creatures) == 1:
        fresh()
        return creatures[0]

    while True:
        index = input(GAME['which_creature'])
        try:
            index = int(index)
            creature = creatures[index - 1]
            
            break

        except IndexError:
            print(ERROR['creature_index_overflow'])
        except ValueError:
            print(ERROR['index_not_interger'])
    
    return creature

def fresh():
    system('cls')

    for player in players:
        print(str(player))
        for creature in player.creatures:
            features = [str(feature) for feature in creature.features]
            print(GAME['fresh']['creature_intro'].format(str(creature), features, creature.food_num, creature.population, creature.size))

        print(GAME['fresh']['player_cards'].format(len(player.cards)))
        print(GAME['fresh']['player_point'].format(player.point))

    print()

    print(GAME['fresh']['water_hole'].format(water_hole_control()))
    print(GAME['fresh']['deck_num'].format(len(deck)))
    
    print()

def _choose_return(player: Player, creature: Creature):
    while True:
        choice = input(GAME['card']['gain']).lower()
        if ('population'.startswith(choice) or choice in ('+p', '++')) and creature.population != 6:
            creature.population += 1
            break

        if ('size'.startswith(choice) or choice in ('+s', '++')) and creature.size != 6:
            creature.size += 1
            break

        if choice in ('add creature', 'ac', '+c', '++', 'add', 'a', 'ad'):
            position = input(GAME['card']['ask_for_side'])
            if 'left'.startswith(position):
                player.creatures.insert(0, Creature(player=player))
                break

            player.creatures.append(Creature(player=player))
            break

        print(GAME['card']['what'])

def _get_food_card() -> list:
    cards = []
    for player in players:
        print(GAME['get_food_card'].format(str(player)))
        
        card = _get_card(player.cards)
        cards.append(card)
        player.cards.remove(card)
        
        fresh()

    return cards

def _can_attack(hunter: Creature, aim: Creature) -> bool:
    disabled = [False] * len(aim.features)
    hunter_size = hunter.size

    for feature in hunter.features:
        feature.on_attack(aim)

    for index, aim_feature in enumerate(aim.features):
        if aim_feature.been_attack(hunter):
            disabled[index] = True
            continue

        flag_list = []
        hunter.features.sort(key=lambda card: card.index)
        for hunter_feature in hunter.features:
            flag_list.append(hunter_feature > aim_feature)

        if any(flag_list):
            disabled[index] = True

    if hunter.size > aim.size and not (False in disabled):
        hunter.size = hunter_size
        return True

    return False

# ---------------- #
#  Upper Function  #
# ---------------- #

def announce():
    food_cards = _get_food_card()
    for card in food_cards:
        water_hole_control(card.point)
        del card

    for player in players:
        player.announce()
    
    sleep(2)
    fresh()

def next_round():
    for player in players:
        player.next_round()
        if player.creatures == []:
            creature = Creature(player=player)
            player.creatures.append(creature)
    
    sleep(2)
    fresh()
    
def attack(hunter: Creature):
    while True:
        fresh()
        player_index = input(GAME['attack']['ask_player_index'])
        try:
            player = players[int(player_index) - 1]
            break
        
        except IndexError:
            print(ERROR['player_index_overflow'])
        except ValueError:
            print(ERROR['index_not_interger'])

    fresh()
    print(GAME['attack']['aim_player_hint'].format(str(player)))
        
    creature = _get_creature(player.creatures)
    
    if _can_attack(hunter, creature):
        creature.population -= 1
        hunter.eat(creature.size)
        
        print(GAME['attack']['succeeded'])
        sleep(1)
    
    else:
        print(GAME['attack']['failed'])
        sleep(1)

def eat(player: Player):
    fresh()
    print(GAME['not_full_hint'].format(str(player)))

    creature_not_full = list(filter(lambda creature: not creature.is_full, player.creatures))
    creature = _get_creature(creature_not_full)

    if creature.is_carnivorous:
        attack(creature)
    else:
        if water_hole_control() == 0:
            print(GAME['eat']['no_water_hole'])
            sleep(1)
            
            return

        creature.eat(1)

def is_deck() -> bool:
    if deck:
        return True
    
    return False

def split_cards():
    global deck
    
    for player in players:
        card_num = 3 + len(player.creatures)
        if len(deck) >= card_num:
            cards = deck[-card_num:]
            deck = deck[:-card_num]
        
        else:
            cards = deck
            deck = []
            
        for card in cards:
            card.root = player
            card.father = player
            
            player.cards.append(card)

def add_card(player: Player):
    fresh()
    print(GAME['card']['show_card'].format([str(card) for card in player.cards]))
    
    if len(player.cards) > 1:
        creature = _get_creature(player.creatures)
        
        features = creature.hidden_features + creature.features
        features = [str(feature) for feature in features]
        
        print(GAME['card']['creature_features'].format(str(creature), features))
        
        card = _get_card(player.cards)
        try:
            creature.add_feature(card)
            player.cards.remove(card)
        
        except (IndexError, ValueError) as e:
            print(e)
            sleep(2)
    
    else:
        print(GAME['card']['stop'])
        sleep(2)

def delete_card(player: Player):
    fresh()

    creature = _get_creature(player.creatures)
    if creature.features:
        features = [str(feature) for feature in creature.features]
        print(GAME['card']['creature_features'].format(str(creature), features))
        
        card = _get_card(creature.features)
        creature.delete_feature(card)
        
        _choose_return(player, creature)
    
    else:
        print(GAME['card']['no_feature'])
        sleep(2)

def private_move():
    fresh()
    
    for player in players:
        input(GAME['card']['private_move'].format(str(player)))
        
        answer = ''
        while True:
            fresh()
            answer = input(GAME['card']['what_to_do']).lower()
            
            if answer in ('del', 'd', 'delete', '-'):
                delete_card(player)
            elif answer in ('add', 'a', '+'):
                add_card(player)
            elif answer in ('q', 'quit'):
                break

        fresh()

def eat_together() -> bool:
    result = False
    for player in players:
        fresh()
        
        if any(not creature.is_full for creature in player.creatures):
            choice = input(GAME['eat']['eat_or_not'].format(str(player))).lower()
            if choice in ('yes', 'y'):
                result = True
                eat(player)
        
        else:
            print(GAME['eat']['all_full'].format(str(player)))
            sleep(1)
            
    return result

def check_winner():
    for player in players:
        for creature in player.creatures:
            player.point += creature.population
            player.point += len(creature.features)
    
    print('# ' + '-' * 10 + ' #')
    print('# ' + str(max(players, key=lambda player: player.point)).center(10) + ' #')
    print('# ' + '-' * 10 + ' #')

if __name__ == '__main__':
    print(ERROR['wrong_file_warning'])
