"""
Lab 1
Group #6
Authors: Kar Chan and Sean Fay
Date: 03/04/2026

This program implements two games:
1. Number Guessing Game - User tries to guess a random number within a certain number of tries
2. Rock-Paper-Scissors Game - User plays rock-paper-scissors against the computer

The user can choose which game to play and can play multiple rounds of either game.
"""

import random

def guessing_game():
    """
    Number Guessing Game
    
    This function implements a number guessing game where the computer generates
    a random number between 1 and 100. The user has 5 attempts to guess the number.
    After each guess, the program provides feedback (too high/too low) and shows
    the number of tries remaining. If the user fails to guess correctly, the
    correct number is revealed. The user can choose to play again.
    
    Author: Fay
    
    """
    while True:  # Main game loop for playing multiple rounds
        # Generate random number between 1 and 100
        secret_number = random.randint(1, 100)
        max_tries = 5
        tries_left = max_tries
        
        print("\nI'm thinking of a number between 1 and 100.")
        
        # Game round loop
        while tries_left > 0:
            try:
                # User input 
                if tries_left == max_tries:
                    guess = int(input(f"Guess what it is. You have {tries_left} tries: "))
                else:
                    guess = int(input(f"Nope! Try again ({tries_left} tries left): "))
                
                # Validate input
                if guess < 1 or guess > 100:
                    print("Please enter a number between 1 and 100.")
                    continue
                
                # Check the guess
                if guess == secret_number:
                    print("You got it!")
                    break
                elif guess < secret_number:
                    print("Too low.", end=" ")
                else:
                    print("Too high.", end=" ")
                
                tries_left -= 1
                
                # Tries remaining
                if tries_left == 0:
                    print(f"\nNope! You lost. The number was {secret_number}")
                    
            except ValueError:
                print("Please enter a valid number.")
        
        # Ask if user wants to play again
        play_again = input("\nDo you want to play again? (Y/N): ").upper()
        while play_again not in ['Y', 'N']:
            play_again = input("Please enter Y or N: ").upper()
        
        if play_again == 'N':
            break


def rock_paper_scissors():
    """
    Rock-Paper-Scissors Game
    
    This function implements a rock-paper-scissors game where the user plays against
    the computer. The computer randomly selects rock, paper, or scissors (represented
    by numbers 1, 2, 3 respectively). The user chooses their move by entering the
    corresponding number. The program determines the winner according to standard
    rock-paper-scissors rules and displays the result. The user can play multiple rounds.
    
    Rules:
    - Rock (3) beats Scissors (2)
    - Scissors (2) beats Paper (1)
    - Paper (1) beats Rock (3)
    
    Author: Chan
   
    """
    # Options displayed
    choices = {1: "paper", 2: "scissors", 3: "rock"}
    
    while True:  # Game loops until user decides to quit
        # Computers selection
        computer_choice = random.randint(1, 3)
        
        print("\n--- Rock-Paper-Scissors Game ---")
        
        # Users selection
        while True:
            try:
                user_choice = int(input("Enter your choice: 1. paper, 2. scissors, 3. rock: "))
                if user_choice in [1, 2, 3]:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Display choices
        print(f"\nYou chose: {choices[user_choice]}")
        print(f"Computer chose: {choices[computer_choice]}")
        
        # Determine winner
        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == 1 and computer_choice == 3) or \
             (user_choice == 2 and computer_choice == 1) or \
             (user_choice == 3 and computer_choice == 2):
            print(f"You win! {choices[user_choice].capitalize()} beats {choices[computer_choice]}!")
        else:
            print(f"You lose! {choices[computer_choice].capitalize()} beats {choices[user_choice]}!")
        
        # Ask if user wants to play again
        play_again = input("\nDo you want to play again? (Y/N): ").upper()
        while play_again not in ['Y', 'N']:
            play_again = input("Please enter Y or N: ").upper()
        
        if play_again == 'N':
            break


def display_welcome():
    """Display welcome message explaining the program"""
    print("=" * 50)
    print("Do you want to play a game?")
    print("=" * 50)
    print("\nChoose wisely...")
    print("1. Guess the secret number")
    print("2. Rock-Paper-Scissors")
    print("\nPlay till your hearts content...and don't lose or elif!")


def main():
    """
    Main program function
    
    This function serves as the entry point for the program. It displays a welcome
    message and presents a menu for the user to choose which game to play.
    The user can continue playing games until they choose to quit.
    """
    display_welcome()
    
    while True:  # Main program loop
        # Display game menu
        print("\n" + "-" * 30)
        print("GAME MENU")
        print("-" * 30)
        print("1. Guessing Game")
        print("2. Rock-Paper-Scissors")
        print("3. Escape the program")
        print("-" * 30)

        # Get user's choice and validate input
        try:
            choice = int(input("Which game do you want to play? (1-3): "))
            
            if choice == 1:
                print("\n" + "=" * 30)
                print("NUMBER GUESSING GAME")
                print("=" * 30)
                guessing_game()
            elif choice == 2:
                print("\n" + "=" * 30)
                print("ROCK-PAPER-SCISSORS")
                print("=" * 30)
                rock_paper_scissors()
            elif choice == 3:
                print("\nThank you for playing! Goodbye!")
                break
            else:
                print("Please enter a number between 1 and 3.")
                
        except ValueError:
            print("Please enter a valid number.")


# Test section
if __name__ == "__main__":
    # Run the main program
    main()
    
    # Uncomment the following lines to test individual games:
    # print("\n" + "="*50)
    # print("TESTING INDIVIDUAL GAMES")
    # print("="*50)
     
    # print("\nTesting Guessing Game:")
    # guessing_game()
     
    # print("\nTesting Rock-Paper-Scissors:")
    # rock_paper_scissors()