from services.runnerService import RunnerService
from models.user import User


def main():
    print('Starting Blackjack Game')
    RunnerService().start_lobby()


if __name__ == '__main__':
    main()
