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
    
    check_winner()

def parser(string: str, clear: bool = True):
    words = string.split()
    
    length = 0
    for word in words:
        print(word, end=' ')
        
        length += len(word)
        if length >= IO_CHAR_LIMIT:
            length = 0
            print()
    
    input('')
    if clear:
        system('cls')
    else:
        fresh()

def play_with_help():
    with open('./hints.json', 'r', encoding='utf-8') as file:
        hints = load(file)

    system('cls')

    parser(hints['openingIntroduction'])
    parser(hints['creaturesIntroduction'])
    parser(hints['haveFun'])
    
    first_time = [True] * 3
    while is_deck():
        split_cards()
        
        if first_time[0]:
            parser(hints['addCardGuide'], clear=False)
            parser(hints['deleteCardGuide'], clear=False)
            parser(hints['howToQuit'], clear=False)
            parser(hints['privateMoveConclusion'])
            first_time[0] = False
            
        private_move()
        
        if first_time[1]:
            parser(hints['foodCard'])
            first_time[1] = False
        
        fresh()
        announce()

        if first_time[2]:
            parser(hints['herbivoresEatGuide'])
            parser(hints['carnivoresEatGuide'])
            parser(hints['defenseAndAttack'])
            parser(hints['eatConclusion'])
            first_time[2] = False
            
        flag = eat_together()  
        while flag:
            flag = eat_together()

        next_round()

    check_winner()

if __name__ == '__main__':
    filename, *args = argv
    if args:
        if args[0] == 'help-mode':
            play_with_help()
    
    else:
        play()
