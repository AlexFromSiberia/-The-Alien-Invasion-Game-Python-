from alien_invasion import *

class Purse():
    def __init__(self, currency = "Unknown", name = 'Unknown'):
        self.__money = 0
        self.currency = currency
        self.name = name

    def popolnim(self, summa):
        self.__money = self.__money + summa

    def tratim(self, summa):
        self.__money = self.__money - summa


    def info(self):
        print(self.__money, self.currency, self.name)

    def __del__(self):
        print('wallet deleted')

x = Purse('USD', 'Alex')
x.popolnim(100)
x.tratim(2)
x.money = 300
x.info()
print(x.money)

print(ai._fire_bullet() = new_bullet)