class User:
    def __init__(self, nickname, balance):
        self.nickname = nickname
        self.balance = balance

    def adjust_balance(self, amount):
        self.balance += amount

    def to_dict(self):
        return {'nickname': self.nickname, 'balance': self.balance}
