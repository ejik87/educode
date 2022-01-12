
class CoffeeCrafter:
    # Receipt  list
    espresso = [250, 0, 16, 4]
    latte = [350, 75, 20, 7]
    cappuccino = [200, 100, 12, 6]

    def __init__(self):
        self.state = 'menu'
        self.store_water = 400
        self.store_milk = 540
        self.store_beans = 120
        self.store_cups = 9
        self.cash = 550

    def main(self):
        while True:
            cmd = input('Write action (buy, fill, take, remaining, exit):\n')
            if cmd == 'buy':
                ent = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n")
                if ent == '1':
                    craft = self.espresso
                elif ent == '2':
                    craft = self.latte
                elif ent == '3':
                    craft = self.cappuccino
                elif ent == 'back':
                    continue
                else:
                    print('Wrong enter')
                self.buy(craft)
            elif cmd == 'fill':
                self.fill()
            elif cmd == 'take':
                self.take()
            elif cmd == 'remaining':
                self.status()
            elif cmd == 'exit':
                break
            else:
                print('Command not found')

    # Print status machine
    def status(self):
        print(f'''\nThe coffee machine has:
{self.store_water} of water
{self.store_milk} of milk
{self.store_beans} of coffee beans
{self.store_cups} of disposable cups
${self.cash} of money
''', sep='\n')

    # Input to fill.
    def fill(self):
        print('Write how many ml of water you want to add:')
        self.store_water += int(input())
        print('Write how many ml of milk you want to add:')
        self.store_milk += int(input())
        print('Write how many grams of coffee beans you want to add:')
        self.store_beans += int(input())
        print('Write how many disposable coffee cups you want to add:')
        self.store_cups += int(input())

    # Input to take.
    def take(self):
        print(f"I gave you ${self.cash}")
        self.cash = 0

    def buy(self, var):
        a = var[0]
        b = var[1]
        c = var[2]
        if a > self.store_water:
            low_in = 'water'
            print(f'Sorry, not enough {low_in}!')
        elif b > self.store_milk:
            low_in = 'milk'
            print(f'Sorry, not enough {low_in}!')
        elif c > self.store_beans:
            low_in = 'coffee beans'
            print(f'Sorry, not enough {low_in}!')
        elif self.store_cups == 0:
            low_in = 'cups'
            print(f'Sorry, not enough {low_in}!')
        else:
            self.store_water -= a
            self.store_milk -= b
            self.store_beans -= c
            self.store_cups -= 1
            self.cash += var[3]
            print('I have enough resources, making you a coffee!')


coffee = CoffeeCrafter()
coffee.main()