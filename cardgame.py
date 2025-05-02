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
import random #used for shuffling
from typing import List #I used this so that my IDE would recognize the type of objects prior to running (not necessary)
import tkinter as tk #for my creative display window


#Card Class
'''
The Card class sets up a card object. Each card has a suit and a rank, based on the standard deck of 52 cards. 
This class has a constructor to initialize each card with a suit and a rank. 
It also has a method to print out the value of a card. 
There are two more methods in this class which check 
    1. if one card has the same suit as another
    2. if one card has the same rank as another
'''
class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"] #list of possible suits a card could have
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"] #list of possible ranks a card could have

    def __init__(self, suit = 0, rank = 2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """This function prints out the value of a card"""
        return (self.rank_list[self.rank] + " of " + self.suit_list[self.suit])

    def sameRank(self, other: Card): 
        """This function determines if two cards have the same rank"""
        return (self.rank == other.rank)

    def sameSuit(self, other: Card):
        """This function determines if two cards have the same suit"""
        return (self.suit == other.suit)

#Deck Class
'''
The Deck class sets up an object that emulates a deck of cards. 
The constructor appends a standard deck of 52 cards into a list so that the deck can be accessed. 
This class has a few methods to achieve the following: 
                1. shuffle the deck
                2. remove a card from the deck
                3. check if the deck is empty
                4. deal cards to players from the deck

'''
class Deck: 
    def __init__(self):
        self.cards = []
        for i in range(4):
            for j in range(1, 14):
                self.cards.append(Card(i, j))

    def shuffle(self): 
        """This function shuffles the cards in a deck"""
        random.shuffle(self.cards)

    def removeCard(self):
        """This function removes a card from the deck"""
        return self.cards.pop()
    
    def is_empty(self):
        """This function returns True when the deck is empty"""
        return len(self.cards) == 0

    def deal(self, hands: List["Hand"], n_cards = 14): 
        """
        This function deals cards to each player
            - hands is a list of Hand objects
            - n_cards represents the total number of cards needed for the game
                - since each player gets 7 cards & there are 2 players, n_cards = 14

            - A card is removed from the deck and placed into a players hand.
            - This function utilizes modulus to alternate who is dealt a card each time (ex: each player gets one card before anyone gets two)
        """
        n_players = len(hands)
        for i in range(n_cards):
            #check to see if deck is empty (cant deal from an empty deck)
            if self.is_empty():
                break
            card = self.removeCard()
            current_player = i % n_players 
            hands[current_player].add_card(card)
    
#Hand Class
'''
The Hand class sets up a Hand object that resembles the cards in a player's hand.
The hand class has a constructor that initializes a list that will store the cards in the players hand.
This class has a few methods that achieve the following: 
                                1. add a card to the hand
                                2. remove a card from the hand
                                3. checks if the player has any cards that they can play for their turn 

'''
class Hand(Deck):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """This function adds a card to a Hand"""
        self.cards.append(card)

    def remove_card(self, card):
        """This function removes a card from a Hand"""
        self.cards.remove(card) 
    
    def hasPlayableCard(self, current_card):
        """
        This function checks to see if the player has any cards they can put in the discard pile
            A player would have a playable card if they have a wild card (an 8) or a card that matches either the suit or rank of the 
            card currently on the top of the discard pile 
        """
        for card in self.cards:
            if card.sameRank(current_card) or card.sameSuit(current_card) or card.rank == 8:
                return True
        return False

#CardGame class
    #A majority of my game-specific code is written in this class
    '''
    This class sets up a CardGame object. This stores most of my game-specific logic and this is called in order for the game to be played. 
    This class has a constructor that sets up the game, initializes hands for each player, and sets the initial scoring to 0 for each player.

    This class has methods to achieve the following: 
                        1. Set up a new game
                        2. get the cards in the players hand
                        3. get the cards in the computers hand
                        4. defines the logic needed for the player to complete their turn
                        5. defines the logic needed for the computer to complete their turn
                        6. Check who won the game 
                        7. Switch turns
                        8. Update the game score
                        9. Display the score 
                        10. Display a pop up window to show the game score and prompt the user if they want to play again or quit
                        11. Reset the game 
    
    '''
class CardGame: 
    def __init__(self, name):
        #dictionary that contains player's name and their Hand
        self.users = {
            name :  Hand(),
            "Computer" : Hand()
        }
        #For Creative Element --> scoreboard graphic (store the win count for each player)
        self.playerScore = 0
        self.computerScore = 0

        self.setupGame()

    def setupGame(self):
        """
        This function sets up for a new game to be played
            - A Deck is shuffled and cards are dealt to the players' hands
            - Another card from the Deck is removed and put on the top of the discared pile
            - The player who goes first is selected randomly 
        
        """
        self.deck = Deck()
        self.deck.shuffle()
        hands = list(self.users.values())
        self.deck.deal(hands)

        self.discardPile = [self.deck.removeCard()]
        self.currentSuit = self.discardPile[-1].suit #stores suit of the card on top of the discard pile
        self.currentRank = self.discardPile[-1].rank #stores rank of the card on top of the discard pile
        self.currentPlayer = random.choice(list(self.users.keys()))


    def getPlayersHand(self, name):
        """This function gets the Hand object (stores the cards in their hand) associated with the user's hand"""
        return self.users[name]
            
    def getComputersHand(self):
        """This function gets the Hand object(stores the cards in their hand) associated with the computer's hand"""
        return self.users["Computer"]

    def playersTurn(self):
        """This function contains the logic needed for the player to complete their turn"""
        #Checks to see if the user is the current player
        if self.currentPlayer != "Computer":
            print()
            print("Your turn:")
            print("You have ", len(self.getPlayersHand(list(self.users.keys())[0]).cards), "cards in your hand") #tell user how many cards are in their hand
            print()
            print("Top card on discard pile: ", self.discardPile[-1]) #tell user what the top card on the discard pile is
            print()

            #Print out all cards in the user's hand
            hand = self.getPlayersHand(self.currentPlayer)
            print("Your hand: ")
            for card in hand.cards:
                print(card, end = " | ")
            
            # Make a list of playable cards & print them out, if there is any playable cards in the user's hand
            if hand.hasPlayableCard(self.discardPile[-1]):
                print()
                #adds card to list playableCards if it is has the same suit or rank as the top card on the discard pile or if it is a wild card (8)
                playableCards = [card for card in hand.cards if card.sameRank(self.discardPile[-1]) or card.sameSuit(self.discardPile[-1]) or card.rank == 8]

                #print out the playable cards
                print("Playable Cards: ")
                count = 0
                for card in playableCards:
                    print("Press ", count, " to play your:", end=" ")
                    print(card)
                    count += 1

                # If only one card is left and it is an 8, user wins immediately (no need to pick a suit to switch to)
                if len(hand.cards) == 1 and playableCards[0].rank == 8:
                    print()
                    print("You played a Wild Card (8) as your last card! You win!")
                    return 
                
                #Allows user to select what card they want to play from the playable cards in their hand
                print()
                validInput = False
                while not validInput:
                    try: 
                        #check if the user made a valid choice (selected an index that represented a playable card)
                            #if they did, set that to be the card played and exit the while loop
                        cardIndex = int(input("Please select a card: "))
                        if 0 <= cardIndex < len(playableCards):
                            card = playableCards[cardIndex]
                            validInput = True
                        else:
                            #if a number was typed, but it does not represent an index of a playable card tell user to pick again
                            print("Invalid choice. Please select a choice from those listed above")
                    except ValueError:
                        #if a non-integer is inputted remind the user they must be typing in a number
                        print("Invalid input. Please enter a number")

                #remove the played card from the user's hand & put it on the top of the discard pile
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

                    while True:
                        newSuit = (input("Please select a suit: "))
                        try:
                            #check if the user made a valid choice (selected an index that represented a suit)
                            #if they did, set that to be the new suit to follow for the discard pile exit the while loop
                            newSuit = int(newSuit)
                            if newSuit not in range(4):
                                #if a number was typed, but it does not represent an index of a suit tell user to pick again
                                print("Invalid suit. Please select a choice from those listed above: ")
                            else:
                                break 
                        except ValueError:
                            #if a non-integer is inputted remind the user they must be typing in a number
                            print("Invalid input. Please enter a number: ")
                    
                    #add an 8 of the selected suit onto the top of the discard pile to reflect the suit change
                    self.currentSuit = newSuit
                    print("Youse chose: ", suits[newSuit])
                    self.discardPile.append(Card(self.currentSuit, 8))

            #When player can't put a card down... makes them draw a card and skips their turn
            else: 
                print(" ")
                print("You have no playable cards, drawing from deck....")
                if self.deck.is_empty() == False: #can only draw a card when the deck is not empty

                    #draw card by removing it from the deck and adding it to their hand
                    cardDrawn = self.deck.removeCard()
                    hand.add_card(cardDrawn)
                    print("You drew: ", cardDrawn)
                else:
                    print("Deck is empty...Counting cards to determine a winner")

    
    def computerTurn(self):
        """This function contains the logic needed for the computer to complete their turn"""
        #Checks to see if the computer is the current player
        if self.currentPlayer == "Computer":
            print()
            print("Computer's turn...")
            print("Computer has ", len(self.getComputersHand().cards), "cards in their hand")  #lets user know how many cards the computer has in their hand 
            print("Top card on discard pile: ", self.discardPile[-1]) #tells what the top card on the discard pile is 
            print(" ")

            #Make a list of playable cards for the computer, if the computer has any playable cards in their hand
            hand = self.getComputersHand()
            if hand.hasPlayableCard(self.discardPile[-1]):
                #adds card to list playableCards if it is has the same suit or rank as the top card on the discard pile or if it is a wild card (8)
                playableCards = [card for card in hand.cards if card.sameRank(self.discardPile[-1]) or card.sameSuit(self.discardPile[-1]) or card.rank == 8]

                
            #Computer will pick the first playable card in the list
                hand.remove_card(playableCards[0]) #remove first playable card from the computer's hand
                self.discardPile.append(playableCards[0]) #add this card to the top of the discard pile
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

                    # Count occurence of each suit in computer's hand
                    suitCounts = [0, 0, 0, 0] 
                    for card in self.getComputersHand().cards:
                        suitCounts[card.suit] += 1

                    # Automatically picks the suit that they have the most of
                    BiggestCountIndex = suitCounts.index(max(suitCounts))
                    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
                    self.currentSuit = BiggestCountIndex 

                    print("Computer chose: ", suits[BiggestCountIndex])
                    self.discardPile.append(Card(self.currentSuit, 8))

            #When computer can't put a card down... makes them draw a card and skips their turn
            else: 
                print("Computer has no playable cards, drawing from deck....")
                if self.deck.is_empty() == False: #can only draw a card when the deck is not empty
                    #draw card by removing it from the deck and adding it to computer's hand
                    cardDrawn = self.deck.removeCard()
                    hand.add_card(cardDrawn)
                else:
                    print("Deck is empty...Counting cards to determine a winner")


    def checkWinner(self):
        """
        This function checks if the game has a winner.

        The function will be set to True if.....
            - If one player has no cards left in their hand they will be the winner. 
            - If the deck is empty, the player who has the least amount of cards in their hand will be the winner
                - If the deck is empty, and both players have the same amount of cards in their hand it will be a tie

        Otherwise this function will return False
        """

        #Checks if players won by getting rid of all their cards
        for player, hand in self.users.items():
            if len(hand.cards) == 0:
                print()
                print(player, "out of cards...", player, "wins!")

                #for creative display
                winner = player #sets winner variable to the winning player
                self.updateScore(winner) #updates the score of the winner
                self.displayPopUp(winner) #displays pop-up score window
                
                return True
        
        #Determines a winner in the case where the deck is empty so no more cards can be drawn
            #whichever player has less cards in their hand will be the winner
        if self.deck.is_empty():
            print()
            print("Deck is now empty...counting remaining cards to determine the winner")
            playerCardCount = len(self.getPlayersHand(list(self.users.keys())[0]).cards)
            computerCardCount = len(self.getComputersHand().cards)
            #if the user has less cards than the computer.... user wins
            if playerCardCount < computerCardCount:
                print()
                print("You have less cards than the computer....You win!")

                #for creative display
                winner = list(self.users.keys())[0] #set the winner to be the user
                self.updateScore(winner) #update the user's win count
                self.displayPopUp(winner) #display pop-up score window

                return True

            #if the computer has less cards than the user... computer wins
            elif computerCardCount < playerCardCount:
                print()
                print("The computer has less cards...Computer wins!")

                #for creative display
                winner = "Computer" #set the winner to be the computer
                self.updateScore(winner) #update the computer's win count
                self.displayPopUp(winner) #display pop-up score window

                return True
            else:
                #when both players have the same # of cards it is a tie
                print()
                print("Both players have the same number of cards...It's a tie!")

                #for creative display
                winner = "Its a tie!" #set the winner variable to indicate its a tie
                #update both players' win counts
                self.updateScore("Computer")
                self.updateScore(list(self.users.keys())[0])
                self.displayPopUp(winner) #display pop-up score window

                return True
        return False

    def nextTurn(self):
        """This function switches the turn to the next player"""
        #if the current player is not the computer.... set the computer to be the new current player when this function is called
        if self.currentPlayer != "Computer":
            self.currentPlayer = "Computer"
        else:
            #if the current player is the computer... set the user to be the new current player when this function is called
            self.currentPlayer = list(self.users.keys())[0]


    #-----------------------------------FUNCTIONS ADDED FOR MY CREATIVE ELEMENT-----------------------------------
    def updateScore(self, winner):
        """This function updates which player won by adding a point to their win count (their score)"""
        #if the winner is not the computer (meaning the user won)... add 1 to the user's score
        if winner != "Computer":
            self.playerScore +=1
        #if the winner is the computer... add 1 to the computer's score
        elif winner == "Computer":
            self.computerScore +=1
    
    def displayScore(self):
        """This function displays the score for both players as a string"""
        return(str(list(self.users.keys())[0]) + ": " + str(self.playerScore) + " | Computer: " + str(self.computerScore))
    
    def displayPopUp(self, winner):
        """This function designs + displays the pop up window that will show up at the end of a game"""
        window = tk.Tk()
        window.title("Game Over") #title of pop-up window
        window.configure(bg="#f0f0f0") #background color
        window.geometry("300x200") #window size

        winnerText = str(winner) + " wins!" #stores text to indicate the winner
        scoreboardText = self.displayScore() #stores text to indicate the score
        winnerLabel = tk.Label(window, text=winnerText, font=('Helvetica', 24), fg="#2e8b57", bg="#f0f0f0") #displays winnerText in the pop-up window
        scoreboardLabel = tk.Label(window, text=scoreboardText, font=('Helvetica', 16), fg="black", bg="#f0f0f0") #displays scoreboardText in the pop-up window
        #pads the text in the window
        winnerLabel.pack(padx=20, pady=10) 
        scoreboardLabel.pack(padx=20, pady=10)

        def playAgain():
            """This function will restart to a fresh game when the playAgain button is pressed from the pop-up window"""
            window.destroy() #close the window
            self.resetGame() #reset to a new game
        
        def quitGame(): 
            """This function will quit the program when the quit button is pressed"""
            window.destroy() #close the window
            exit() #program will stop running
        
        buttonStyle = {"font": ("Helvetica", 12), "width": 12, "padx": 5, "pady": 5} #stylizes buttons for the pop-up window
        playAgainButton = tk.Button(window, text="Play Again", command=playAgain, **buttonStyle, fg="green") #creates a playAgain button, that will call the playAgain() function when pressed
        quitButton = tk.Button(window, text="Quit", command=quitGame, **buttonStyle, fg="red") #creates a quit button, that will call the quitGame() function when pressed
        #pads buttons in the window
        playAgainButton.pack(padx=20, pady=5)
        quitButton.pack(padx=20, pady=5)

        #keeps window open and running until it is closed by the user
        window.mainloop()
        #--------------------------------------END OF FUNCTIONS FOR MY CREATIVE ELEMENT----------------------------------



    def resetGame(self):
        """This function will set up a new game to be played"""
        print("Starting a new game...")
        print()
        self.setupGame() #this function is called so a fresh game is set up

        #while there is no winner.... take turns playing the game starting with whoever the 1st player was chosen to be (its random who is first)
        while not self.checkWinner():
            if self.currentPlayer != "Computer":
                self.playersTurn()
            else:
                self.computerTurn()
            self.nextTurn()


#Main method: this code is used to call everything I wrote in my classes
def main():
    print("Welcome to CRAZY 8!")
    print()
    name = input("Please enter your name: ") #allows the user to enter their name to be identified by
    print()
    print("Shuffling...")
    print("Dealing...")

    #initializes a CardGame object called game and tells the CardGame class what the user's name is
    game = CardGame(name)

    #find whose turn it is and keep switching turns until there is a winner
    while not game.checkWinner():
        if game.currentPlayer != "Computer":
            game.playersTurn()
        else:
            game.computerTurn()

        game.nextTurn()

#calls main method
if __name__ == "__main__":
    main()

    

    


