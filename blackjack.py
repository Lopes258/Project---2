import random


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}

playing = True


#CREATE THE CARDS
class Card:
    #HERE IS THE MERGE TO CREATE THE CARD
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        #IF YOU WANT TO KNOW WHAT IS THE CARD
    def __str__(self):
        return self.rank + ' of ' + self.suit

#CREATE ALL THE 52 CARDS
class Deck:
    #TO CREATE THE ALL CARDS
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def  __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has " + deck_comp
                    
    #SO DECK CAN BE SHUFLE IN THAT WAY THE CARDS WILL BE PICK AT RANDOM
    def shuffle(self):
        random.shuffle(self.deck)

    #TO PICK THE CARDS
    def deal_one(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        #TRACK ACES
        if card.rank == 'Ace' :
            self.aces += 1
    
    def adjust_for_ace(self):
        '''
        IF TOTAL VALUE > 21  AND I STILL HAVE AN ACE
        THAN CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        '''
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

'''TESTING TO SEE IF THE PULL CARD AND SHUFLLE IS WORKING
test_deck = blackjack_deck.Deck()
test_deck.shuffle()

test_player = Hand()
pulled_card = test_deck.deal_one()
print(pulled_card)
test_player.add_card(pulled_card)
print(test_player.value)
'''

class Chips:

    def __init__(self,total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet 
        self.bet = 0
        
    def lose_bet(self):
        self.total -= self.bet
        self.bet = 0
    
    def consult_total(self):
        return self.total
            

def take_bet(chips):

    while True:

        try: chips.bet = int(input("How many chips  would you like to bet? "))

        except ValueError:
            print("Sorry please provide a integer")
        else: 
            if chips.bet > chips.total:
                print("Sorry, you dont have enough chips! You have: {}".format(chips.total))
            else:
                break


def hit(deck,hand):
    single_card = deck.deal_one()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing 

    while True:
        x = input("Hit or Stand? Enter h or s ")

        if x[0].lower() == 'h':
            hit(deck,hand)
        
        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False
        
        else:
            print("Sorry, I did not uderstand that, Please enter h or s only!")
            continue

        break

def show_some(player,dealer):
     # IN THIS FUNCTION I WANT TO SHOW ONLY ONE OF THE DEALER'S CARDS AND SHOW ALL (2 CARDS) OF THE PLAYERS HAND/CARDS AT THE BEGINIING OF THE GAME
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)

   
def show_all(player,dealer):

    ''' 
    IN THIS FUNCTION I WANT TO SHOW ONLY ONE OF THE DEALER'S CARDS
    CALCULATE AND DISPLAY VALUE
    SHOW ALL OF THE PLAYERS HAND/CARDS
    '''
    
    print("\n Dealer's Hand: ",*dealer.cards, sep= '\n')  #DIFERENT WAY OF DOING THE FOR
    print(f"Value of Dealers's hand is: {dealer.value}")

    print("\n Player's Hand: ")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand is: {player.value}")


def player_busts(player,dealer,chips):
      
    print("BUST PLAYER!")
    chips.lose_bet()
    
def player_wins(player,dealer,chips):

    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):

    print("PLAYER WINS! DEALER BUSTED")
    chips.win_bet()

def dealer_wins(player,dealer,chips):

    print("DEALER WINS!")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and player tie! Push")




while True:

    print("WELCOME TO BLACKJACK")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal_one())
    player_hand.add_card(deck.deal_one())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())

    player_chips = Chips() 

    take_bet(player_chips)

    show_some(player_hand,dealer_hand)

    while playing:
        hit_or_stand(deck,player_hand)

        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)

            break

    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)

        show_all(player_hand,dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    print("\n Player total chips are at: {}".format(player_chips.total))


    new_game = input("Would you like to play another hand? y/n: ")

   
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing.")
        break