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
from __future__ import annotations #needed so classes could depend on eachother regardless of order
import random
from typing import List 



#Card Class
class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit = 0, rank = 2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return (self.rank_list[self.rank] + " of " + self.suit_list[self.suit])

    def sameRank(self, other: Card): 
        """This function determines if two cards have the same rank"""
        return (self.rank == other.rank)

    def sameSuit(self, other: Card):
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

    def deal(self, hands: List["Hand"], n_cards = 14): 
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
        hands = list(self.users.values())
        self.deck.deal(hands)

        self.discardPile = [self.deck.removeCard()]
        self.currentSuit = self.discardPile[-1].suit
        self.currentRank = self.discardPile[-1].rank
        self.currentPlayer = random.choice(list(self.users.keys()))


    def getPlayersHand(self, name):
        return self.users[name]
            
    def getComputersHand(self):
        return self.users["Computer"]

    def playersTurn(self):
        #Checks to see if the user is the current player
        if self.currentPlayer != "Computer":
            print()
            print("Your turn:")
            print("You have ", len(self.getPlayersHand(list(self.users.keys())[0]).cards), "cards in your hand")
            print()
            print("Top card on discard pile: ", self.discardPile[-1]) 
            print()

            #Print full hand
            hand = self.getPlayersHand(self.currentPlayer)
            print("Your hand: ")
            for card in hand.cards:
                print(card, end = " | ")
            
            # Make a list of playable cards & print them out, if possible
            if hand.hasPlayableCard(self.discardPile[-1]):
                print()
                playableCards = [card for card in hand.cards if card.sameRank(self.discardPile[-1]) or card.sameSuit(self.discardPile[-1]) or card.rank == 8]

                print("Playable Cards: ")
                count = 0
                for card in playableCards:
                    print("Press ", count, " to play your:", end=" ")
                    print(card)
                    count += 1

                # If only one card is left and it is an 8, user wins immediately
                if len(hand.cards) == 1 and playableCards[0].rank == 8:
                    print()
                    print("You played a Wild Card (8) as your last card! You win!")
                    return 
                
                #Allows user to select what card they want to play
                print()
                validInput = False
                while not validInput:
                    try: 
                        cardIndex = int(input("Please select a card: "))
                        if 0 <= cardIndex < len(playableCards):
                            card = playableCards[cardIndex]
                            validInput = True
                        else:
                            print("Invalid choice. Please select a choice from those listed above")
                    except ValueError:
                        print("Invalid input. Please enter a number")

                hand.remove_card(card)
                self.discardPile.append(card)
                print("You played: ", card)

                #Allows user to change the suit if they play a wild card (8)
                if card.rank == 8:
                    print(" ")
                    print("Wild Card! You get to change the suit")
                    count = 0
                    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
                    for suit in suits:
                        print("Press ", count, " to play your:", end=" ")
                        print(suit)
                        count += 1

                    newSuit = int(input("Please select a suit: "))
                    while newSuit not in range(4):
                        newSuit = int(input("Invalid suit. Please select a choice from those listed above: "))
                    self.currentSuit = newSuit
                    print("Youse chose: ", suits[newSuit])
                    self.discardPile.append(Card(self.currentSuit, 8))

            #When player can't put a card down... makes them draw a card and skips their turn
            else: 
                print(" ")
                print("You have no playable cards, drawing from deck....")
                if self.deck.is_empty() == False:
                    cardDrawn = self.deck.removeCard()
                    hand.add_card(cardDrawn)
                    print("You drew: ", cardDrawn)
                else:
                    print("Deck is empty...Counting cards to determine a winner")

    
    def computerTurn(self):
        #Checks to see if the user is the current player
        if self.currentPlayer == "Computer":
            print()
            print("Computer's turn...")
            print("Computer has ", len(self.getComputersHand().cards), "cards in their hand")
            print("Top card on discard pile: ", self.discardPile[-1]) 
            print(" ")

            #Make a list of playable cards & print them out, if possible
            hand = self.getComputersHand()
            if hand.hasPlayableCard(self.discardPile[-1]):
                playableCards = [card for card in hand.cards if card.sameRank(self.discardPile[-1]) or card.sameSuit(self.discardPile[-1]) or card.rank == 8]

                
            #Computer will pick the first playable card in the list
                hand.remove_card(playableCards[0])
                self.discardPile.append(playableCards[0])
                print("The computer has played: ", playableCards[0])

                #If the last card played is a wild card, recognize the win without making computer pick a suit change
                if len(self.getComputersHand().cards) == 1 and playableCards[0].rank == 8:
                    print(" ")
                    print("The computer played a Wild Card (8) as their last card! Computer wins!")
                    return 

                #Allows computer to change the suit if they play a wild card (8)
                if playableCards[0].rank == 8:

                    print(" ")
                    print("Wild Card! Computer is changing the suit....")
                    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

                    # Count suits in computer's hand
                    suitCounts = [0, 0, 0, 0] 
                    for card in self.getComputersHand().cards:
                        suitCounts[card.suit] += 1

                    # Automatically picks the suit with the highest count
                    BiggestCountIndex = suitCounts.index(max(suitCounts))
                    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
                    self.currentSuit = BiggestCountIndex  # store suit as int

                    print("Computer chose: ", suits[BiggestCountIndex])
                    self.discardPile.append(Card(self.currentSuit, 8))

            #When computer can't put a card down... makes them draw a card and skips their turn
            else: 
                print("Computer has no playable cards, drawing from deck....")
                if self.deck.is_empty() == False:
                    cardDrawn = self.deck.removeCard()
                    hand.add_card(cardDrawn)
                else:
                    print("Deck is empty...Counting cards to determine a winner")


    def checkWinner(self):
        """This function checks if the game has a winner"""
        for player, hand in self.users.items():
            if len(hand.cards) == 0:
                print()
                print(player, "out of cards...", player, "wins!")
                return True
        if self.deck.is_empty():
            print()
            print("Deck is now empty...counting remaining cards to determine the winner")
            playerCardCount = len(self.getPlayersHand(list(self.users.keys())[0]).cards)
            computerCardCount = len(self.getComputersHand().cards)
            if playerCardCount < computerCardCount:
                print()
                print("You have less cards than the computer....You win!")
                return True
            elif computerCardCount < playerCardCount:
                print()
                print("The computer has less cards...Computer wins!")
                return True
            else:
                print()
                print("Both players have the same number of cards...It's a tie!")
                return True
        return False

    def nextTurn(self):
        """Switch to the next player"""
        if self.currentPlayer != "Computer":
            self.currentPlayer = "Computer"
        else:
            self.currentPlayer = list(self.users.keys())[0]





def main():
    print("Welcome to CRAZY 8!")
    print()
    name = input("Please enter your name: ")
    print()
    print("Shuffling...")
    print("Dealing...")

    game = CardGame(name)
    while not game.checkWinner():
        if game.currentPlayer != "Computer":
            game.playersTurn()
        else:
            game.computerTurn()

        #if not game.checkWinner():
        game.nextTurn()


if __name__ == "__main__":
    main()

    

    


