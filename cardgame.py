#Arden Sentak: I pledge my honor that I have abided by the Stevens Honor System

"""
The card game I am coding is based off of Crazy Eights.

INSTRUCTIONS: 

    GENERAL SETUP:
    - 2 player game (computer vs user)
    - Each player is dealt 7 cards (a standard 52 card deck is used to deal)
    - After each player is dealt their hand, the next card from the deck is flipped face up as the starting card for the discard pile
    - The player to go first will be randomly selected

    GAME FLOW: 
    - Players takes turns placing a card from their hand into the discard pile
        - The card a player places down must match either the suit or the rank of the top card in the discard pile

        WILD CARDS: 
        - An 8 represents a wild card; these can be placed on top of any card. 
            Additionally when an 8 is played, the player gets to choose the suit they want to be followed

        DRAWING CARDS:
        - If a player doesn't have any cards they can play they must draw a card from the deck. 
            - The players turn is over after they draw. They do not get to play the card even if its playable 

    HOW TO WIN: 
    - The first player to get rid of all their cards wins!

    EMPTY DECK WITH NO WINNER YET: 
    - If the deck is empty and there is not yet a winner, the person who currently has less cards in their hand wins!
        - If both players have the same amount of cards in their hand, the game ends in a tie
"""
import random


#Card Class
class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit = 0, rank = 2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (self.rank_list[self.rank] + " of " + self.suit_list[self.suit])

    def sameRank(self, other): 
        """This function determines if two cards have the same rank"""
        return (self.rank == other.rank)

    def sameSuit(self, other):
        """This function determines if two cards have the same suit"""
        return (self.suit == other.suit)

#Deck Class
class Deck: 
    def __init__(self):
        self.cards = []
        for i in range(4):
            for j in range(1, 14):
                self.cards.append(Card(i, j))

    def shuffle(self): 
        random.shuffle(self.cards)

    def removeCard(self):
        return self.cards.pop()
    
    def is_empty(self):
        return len(self.cards) == 0

    def deal(self, hands, n_cards = 14): 
        n_players = len(hands)
        for i in range(n_cards):
            if self.is_empty():
                break
            card = self.removeCard()
            current_player = i % n_players
            hands[current_player].add_card(card)
    
#Hand Class
class Hand(Deck):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card) 
    
    def hasPlayableCard(self, current_card):
        """This function checks to see if the player has any cards they can put in the discard pile"""
        for card in self.cards:
            if card.sameRank(current_card) or card.sameSuit(current_card) or card.rank == 8:
                return True
        return False

class CardGame: 
    def __init__(self, name):
        self.deck = Deck()
        self.deck.shuffle()
        self.users = {
            name :  Hand(),
            "Computer" : Hand()
        }
        hands = self.users.values()
        self.deck.deal(hands)

        self.discardPile = [self.deck.removeCard()]
        self.currentSuit = self.discardPile[-1].suit
        self.currentRank = self.discardPile[-1].rank
        self.currentPlayer = random.choice(self.users.keys())


    def getPlayersHand(self, name):
        return self.users[name]
            
    def getComputersHand(self):
        return self.users["Computer"]

    def playersTurn(self):
        if self.currentPlayer != "Computer":
            print("Your turn:")
            print("Top card on discard pile: {self.discardPile[-1]}") #FIXXXX---------------------------

            hand = self.getPlayersHand(self.currentPlayer)
            if hand.hasPlayableCard(self.discardPile[-1]):
                playableCards = [card for card in hand.cards if card.sameRank(self.discardPile[-1]) or card.sameSuit(self.discardPile[-1]) or card.rank == 8]

                print("Playable Cards: ")
                count = 0
                for card in playableCards:
                    print("Press ", count, " to play your:", end=" ")
                    print(card)
                    count += 1
                
                validInput = False
                while not validInput:
                    try: 
                        cardIndex = input("Please select a card: ")
                        if 0 <= cardIndex < len(playableCards):
                            card = playableCards[cardIndex]
                            validInput = True
                        else:
                            print("Invalid choice. Please select a choice from those listed above")
                    except ValueError:
                        print("Invalid input. Please enter a number")

                    hand.remove_Card(card)
                    self.discardPile.append(card)
                    print("You played: ", card)

                    if card.rank == 8:
                        print("Wild Card! You get to change the suit")
                        count = 0
                        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
                        for suit in suits:
                            print("Press ", count, " to play your:", end=" ")
                            print(suit)
                            count += 1

                        newSuit = input("Please select a suit: ")
                        while newSuit not in suits:
                            newSuit = input("Invalid suit. Please select a choice from those listed above")
                        self.currentSuit = suits[newSuit]
            else: 
                print("You have no playable cards, drawing from deck....")
                if self.deck.is_empty() == False:
                    cardDrawn = self.deck.removeCard()
                    hand.add_card(cardDrawn)
                    print("You drew: {cardDrawn}")
                else:
                    print("Deck is empty...")

                self.checkWinner()
    
    def computerTurn(self):
        pass

    def checkWinner(self):
        """Check if the game has a winner"""
        for player, hand in self.users.items():
            if len(hand.cards) == 0:
                print(f"{player} wins!") #FIX THIS DONT WANNA USE PRINTF---------------------
                return True
        if self.deck.is_empty():
            player_card_count = len(self.getPlayersHand("Player").cards)
            computer_card_count = len(self.getComputersHand().cards)
            if player_card_count < computer_card_count:
                print("Player wins!")
            elif computer_card_count < player_card_count:
                print("Computer wins!")
            else:
                print("It's a tie!")
            return True
        return False

    def nextTurn(self):
        """Switch to the next player"""
        self.currentPlayer = "Computer" if self.currentPlayer != "Computer" else "Player"




# Game Setup --> should prib go in main
game = CardGame("Player")
while not game.checkWinner():
    if game.currentPlayer == "Player":
        game.playersTurn()
    else:
        game.computerTurn()

    # After each turn, check the winner and switch turns
    if not game.checkWinner():
        game.nextTurn()


                    


                    





def main():
    print("Welcome to CRAZY 8!")
    print()
    name = input("Please enter your name: ")
    print()
    print("Shuffling...")
    print("Dealing...")
    


if __name__ == "__main__":
    main()

    

    


