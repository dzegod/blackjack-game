from helpers.generalHelpers import clear_terminal
from models.userManager import UserManager
from services.blackjackService import BlackjackService


class RunnerService:
    def __init__(self):
        self.manager = UserManager()
        return

    def start_lobby(self):
        clear_terminal()
        initial = True
        print("Welcome to Blackjack-Game!")

        while True:
            if not initial:
                clear_terminal()

            initial = False
            print("1. Login")
            print("2. Register")
            print("3. Close")
            nickname = None
            choice = input("Select an option (1/3): ")

            if choice == '1':
                while True:
                    nickname = input("Enter your nickname (leave blank to quit): ")
                    if nickname == "":
                        break
                    user = self.manager.get_user(nickname)
                    if user:
                        self.start_game(user.nickname)
                        break
                    print("User not found. Try again.")
            elif choice == '2':
                while True:
                    if self.manager.can_create_users():
                        nickname = input("Choose your nickname: ")
                    else:
                        break

                    if nickname is not None and self.manager.get_user(nickname):
                        print("Nickname already taken")
                    else:
                        user = self.manager.register_user(nickname)
                        if user:
                            self.start_game(user.nickname)
                        break
            elif choice == "3":
                break
            else:
                print("Invalid choice")

        print("\nClosing game")
        return

    def start_game(self, nickname):
        game = BlackjackService(self.manager)
        user = self.manager.get_user(nickname)

        while True:
            clear_terminal()
            print(f"\n{user.nickname}, Balance: {user.balance}")
            print("1. Play round")
            print("2. Exit")
            action = input("Select option: ")

            if action == '1':
                game.play_round(user)
                self.manager.save_users()
                _ = input('Press enter to continue')
            elif action == '2':
                self.manager.save_users()
                print("Progress saved")
                break
            else:
                print("Invalid choice")
                return
