import random

class Number_guessing_game:
    def play_game(self):
        random_guess = random.randint(1, 100)
        attempts = 0
        guessed = False

        while not guessed:
            try:
                player_guess = int(input("Enter your guess: "))
                attempts += 1

                if player_guess < random_guess:
                    print("Too low! Try again.")
                elif player_guess > random_guess:
                    print("Too high! Try again.")  
                else:
                    print(f"Congratulations! You guessed the number {random_guess} in {attempts} attempts.")
                    guessed = True
            except ValueError:
                print("Invalid input. Please enter a number.")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == 'yes' or play_again == 'y':
            self.play_game()
        else:
            print("Thank you for playing! Goodbye.")
     
if __name__ == "__main__":
    game = Number_guessing_game()
    game.play_game()
