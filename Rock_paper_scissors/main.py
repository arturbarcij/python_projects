import random


class Rock_paper_Scissors:
    def __init__(self) -> None:
        self.choices = ["rock", "paper", "scissors"]
        self.user_score = 0
        self.computer_score = 0

    def get_computer_choice(self):
        return random.choice(self.choices)

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "tie"
        elif (user_choice == "rock" and computer_choice == "scissors") or \
            (user_choice == "paper" and computer_choice == "rock") or \
            (user_choice == "scissors" and computer_choice == "paper"):
            return "user"
        else:
            return "computer"

    def play_game(self):
        choices = ["rock", "paper", "scissors"]
        user_score = 0
        computer_score = 0

        while True:
            user_choice = ""
            while user_choice not in self.choices:
                user_choice = input("Please enter rock, paper, or scissors: ").lower()
                if user_choice not in self.choices:
                    print("Invalid choice. Try again.")

            computer_choice = self.get_computer_choice()
            print(f"Computer chose: {computer_choice}")

            winner = self.determine_winner(user_choice, computer_choice)
            if winner == "tie":
                print("It's a tie!")
            elif winner == "user":
                print("You win!")
                self.user_score += 1
            else:
                print("Computer wins!")
                self.computer_score += 1

            print(f"Score - You: {self.user_score}, Computer: {self.computer_score}")

            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again != "yes":
                break

        print("Thanks for playing!")


if __name__ == "__main__":
    game = Rock_paper_Scissors()
    game.play_game()