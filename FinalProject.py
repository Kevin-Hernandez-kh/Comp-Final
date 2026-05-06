"""Kevin Hernandez
Python Party - a simulation of a single player party board game with CPUs and items that lasts
20 turns and when the game ends the winner is based on who has the most stars """

import random
ITEMS = ["Coin Booster, Poison, Teleporter, Double Dice, Star Taker"]

class Die:
    ###This class represents a die value of one that randomly picks a between 1 to 10.###

    def __init__(self):
        self.value = 1

    def roll(self):
        self.value = random.randint(1, 10)

    def getValue(self):
        return self.value
        

    def __str__(self):
        return str(self.getValue())

class Board:
    ## initalizes the board and implements spaces with different effects
    def __init__(self):
        self.spaces = []

        # Add multiple coin spaces
        for _ in range(5):
            self.spaces.append(Space("Coin +5", "coin", 5))

        for _ in range(3):
            self.spaces.append(Space("Coin -3", "coin", -3))

        # Add multiple item spaces
        for _ in range(4):
            self.spaces.append(Space("Item Box", "item"))

        # Add star spaces
        for _ in range(2):
            self.spaces.append(Space("Star Space", "star"))

        # Add event spaces
        for _ in range(3):
            self.spaces.append(Space("Event Space", "event"))

        # Adds the start space
        self.spaces.append(Space("Start"))

        random.shuffle(self.spaces)

class Space:
    # initialization of spaces #
    def __init__(self, name, effect_type=None, value=0,):
        self.name = name
        self.effect_type = effect_type  # "coin", "item", "star", "event"
        self.value = value              # amount of coins, etc.
        
        

    
    
    def apply_effect(self, player):
        if self.effect_type == "coin":
            player.change_coins(self.value)
            print(f"{player.name} {'gains' if self.value > 0 else 'loses'} {abs(self.value)} coins!")

        elif self.effect_type == "item":
            item = random.choice(ITEMS)
            player.add_item(item)
            print(f"{player.name} found an item: {item}!")

        elif self.effect_type == "star":
            if player.coins >= 20:
                player.coins -= 10
                player.stars += 1
                print(f"{player.name} earned a STAR!")

            else:
                print(f"You don't have enough coins for a star")

        elif self.effect_type == "event":
            print(f"{player.name} triggered an event!")

        else:
            print(f"{player.name} landed on {self.name}. Nothing happens.")


class Items:
    def __init__(self, name, effect = None):
        self.name = name
        self.effect = effect
    
    def __str__(self):
        return self.name



def apply_item_effect(player, item, players):
    if item == "Coin Booster":
        print(f"{player.name} gets +3 coins!")
        player.change_coins(3)

    elif item == "Poison":
        print(f"{player.name} loses 2 coins!")
        player.change_coins(-2)

    elif item == "Teleporter":
        print(f"{player.name} teleports to Start!")
        player.position = 0
        player.land_on_space()

    elif item == "Double Dice":
        print(f"{player.name} rolls twice!")
        roll1 = player.rollDice()
        roll2 = player.rollDice()
        total = roll1 + roll2
        print(f"Total movement: {total}")
        player.move(total)

    elif item == "Star Taker":
        print(f"{player.name} steals a star from the richest player!")
        candidates = [p for p in players if p.stars > 0 and p != player]

        if not candidates:
            print(f"No stars available to steal!")
            return

        
        target = max(candidates, key=lambda p: p.stars)

        # Transfer the star
        target.stars -= 1
        player.stars += 1

        print(f"{player.name} stole a star from {target.name}!")

class Player:
    
    def __init__(self, name, board, is_cpu=False):
        self.name = name
        self.board = board
        self.position = 0
        self.die1 = Die()
        self.is_cpu = is_cpu
        self.inventory = []
        self.coins = 0
        self.stars = 0

    
    def rollDice(self):
        self.die1.roll()
        return self.die1.getValue()

    # how the player moves in the board #
    def move(self, steps):
        self.position = (self.position + steps) % len(self.board.spaces)
        self.land_on_space()

    def land_on_space(self):
        space = self.board.spaces[self.position]
        print(f"{self.name} landed on {space.name}")
        space.apply_effect(self)

    def change_coins(self, amount):
        self.coins = max(0, self.coins + amount)
    
    # function for adding items to player inventory#
    def add_item(self, item):
        if len(self.inventory) < 3:
            self.inventory.append(item)
            print(f"{self.name} picked up {item}")
        else:
            print(f"{self.name}'s inventory is full")

    def use_item(self, item, players):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{self.name} used {item}")
            apply_item_effect(self, item, players)
        else:
            print(f"{self.name} does not have {item}")

# define how the cpus act in the game#
def cpu_turn(player, players):
    print(f"\n--- {player.name}'s CPU Turn ---")

    # CPU randomly decides whether to use an item (30% chance) #
    if player.inventory and random.random() < 0.3:
        item = random.choice(player.inventory)
        print(f"{player.name} decides to use {item}")
        player.use_item(item, players)
        return

    # Otherwise CPU rolls the dice #
    roll = player.rollDice()
    print(f"{player.name} rolled: {roll}")
    player.move(roll)

def Winner(players):
    print("\n===== GAME OVER =====")
    print("Final Results:")

    for p in players:
        print(f"{p.name}: {p.stars} stars, {p.coins} coins")

    # Finds the highest star count #
    max_stars = max(p.stars for p in players)

    # Gets all players who have that many stars #
    winners = [p for p in players if p.stars == max_stars]

    if len(winners) == 1:
        print(f"\n {winners[0].name} wins with {max_stars} stars!")
    else:
        # if Tie-breaker: use coins #
        print("\nTie detected! Using coins as tie-breaker...")
        max_coins = max(p.coins for p in winners)
        final_winners = [p for p in winners if p.coins == max_coins]

        if len(final_winners) == 1:
            print(f" {final_winners[0].name} wins with {max_stars} stars and {max_coins} coins!")
        else:
            print("It's a complete tie!")

def game_loop(player, players):
    # The gameplay loop #
    while True:
        print("\n=== GAME MENU ===")
        print("1. Roll Dice")
        print("2. Use Item")
        print("3. Check Inventory")
        print("4. Quit Game")

        choice = input("Choose an option: ").strip()
        # choice options #
        if choice == "1":
            roll = player.rollDice()
            print(f"You rolled: {roll}")
            player.move(roll)
            return

        elif choice == "2":
            use_item_menu(player, players)

        elif choice == "3":
            show_inventory(player)

        elif choice == "4":
            print("Ending game...")
            break

        else:
            print("Invalid choice.")

def show_inventory(player):
    # item inventory menu #
    print("\n=== INVENTORY ===")
    if not player.inventory:
        print("Inventory is empty")
        return
    for i, item in enumerate(player.inventory, start=1):
        print(f"{i}. {item}")

def use_item_menu(player, players): # how the user can select an item to use
    show_inventory(player)
    if not player.inventory:
        return

    choice = input("Choose an item number: ").strip()
    if not choice.isdigit():
        print("Invalid choice")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(player.inventory):
        print("Invalid item number")
        return

    item = player.inventory[index]
    player.use_item(item, players)


def play_game(rounds=20):
    # the turn loop/main loop#
    board = Board()
    players = [
        Player("Player 1", board),
        Player("CPu 1", board, is_cpu=True),
        Player("CPU 2", board, is_cpu=True),     
        Player("CPU 3", board, is_cpu=True) 
        ]   

    for round_num in range(1, rounds + 1):
        print(f"\n===== ROUND {round_num} =====") #shows the round number and standings#

        print("\nCurrent Standings:")
        for p in players:
            print(f"{p.name}: {p.stars} stars, {p.coins} coins")

        for player in players:
            print(f"\n--- {player.name}'s Turn ---")
            # checks if a player is a cpu or not #
            if player.is_cpu:
                cpu_turn(player, players)
            else:
                game_loop(player, players)

    Winner(players)

def main():
    play_game(20)

if __name__ == "__main__":
    main()