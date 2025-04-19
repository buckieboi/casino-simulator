import random
from abc import ABC, abstractmethod

# --- BETS FRAMEWORK ---

class Bet(ABC):
    """Abstract base for any bet type."""
    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def resolve_on_come_out(self, roll):
        """
        Called on the come‑out roll.
        Returns net win (positive) or loss (negative), or None if unresolved.
        """
        pass

    @abstractmethod
    def resolve_point_phase(self, roll, point):
        """
        Called after a point is established.
        Returns net win/loss, or None if unsettled.
        """
        pass

class PassLineBet(Bet):
    """Traditional pass‑line bet."""
    def resolve_on_come_out(self, roll):
        if roll in (7, 11):
            return self.amount
        elif roll in (2, 3, 12):
            return -self.amount
        return None

    def resolve_point_phase(self, roll, point):
        if roll == point:
            return self.amount
        elif roll == 7:
            return -self.amount
        return None

class FieldBet(Bet):
    """Field bet pays 1:1, 2:1 on 2 or 12."""
    def resolve_on_come_out(self, roll):
        if roll in (3, 4, 9, 10, 11):
            return self.amount
        elif roll in (2, 12):
            return self.amount * 2
        else:
            return -self.amount

    def resolve_point_phase(self, roll, point):
        return None

class SnakeEyesBet(Bet):
    """Bet that next roll is snake eyes (2). Pays 30:1."""
    def resolve_on_come_out(self, roll):
        return self.amount * 30 if roll == 2 else -self.amount

    def resolve_point_phase(self, roll, point):
        return None

class AnySevenBet(Bet):
    """Bet that next roll is any 7. Pays 4:1."""
    def resolve_on_come_out(self, roll):
        return self.amount * 4 if roll == 7 else -self.amount

    def resolve_point_phase(self, roll, point):
        return None

class YoBet(Bet):
    """Bet that next roll is 11 (yo). Pays 15:1."""
    def resolve_on_come_out(self, roll):
        return self.amount * 15 if roll == 11 else -self.amount

    def resolve_point_phase(self, roll, point):
        return None

# --- PLAYER & GAME CLASSES ---

class Player:
    DENOMINATIONS = [5, 10, 25, 50, 100]

    def __init__(self, starting_chips=100):
        self.chips = starting_chips

    def place_bet_amount(self):
        """Prompt for a valid bet amount and deduct it."""
        print(f"  You have {self.chips} chips.")
        print("  Allowed chip values:", Player.DENOMINATIONS)
        while True:
            try:
                amt = int(input("  Enter bet amount: "))
            except ValueError:
                print("   → Please enter a whole number.")
                continue
            if amt <= 0:
                print("   → Bet must be positive.")
            elif amt > self.chips:
                print(f"   → You only have {self.chips} chips.")
            elif amt not in Player.DENOMINATIONS:
                print(f"   → Bet must be one of {Player.DENOMINATIONS}.")
            else:
                self.chips -= amt
                return amt

    def adjust_chips(self, net):
        """Adjust chip count and show result."""
        self.chips += net
        if net > 0:
            print(f"   -> You win {net} chips!")
        elif net < 0:
            print(f"   -> You lose {-net} chips.")
        else:
            print("   -> Push (no win/loss).")

class CrapsGame:
    BET_TYPES = [
        ('Pass Line', PassLineBet),
        ('Field', FieldBet),
        ('Snake Eyes (2)', SnakeEyesBet),
        ('Any Seven (7)', AnySevenBet),
        ('Yo (11)', YoBet),
    ]

    def __init__(self, player):
        self.player = player

    @staticmethod
    def roll_dice():
        return random.randint(1, 6), random.randint(1, 6)

    def collect_bets(self):
        print("\n--- Place your bets for next roll ---")
        bets = []
        for idx, (name, cls) in enumerate(CrapsGame.BET_TYPES, start=1):
            print(f" {idx}) {name}")
        print(" 0) Done betting")
        while True:
            choice = input("Select bet (number), or 0 to finish: ").strip()
            if choice == '0':
                break
            if not choice.isdigit() or not (1 <= int(choice) <= len(CrapsGame.BET_TYPES)):
                print("   → Invalid selection.")
                continue
            idx = int(choice) - 1
            amt = self.player.place_bet_amount()
            bet_cls = CrapsGame.BET_TYPES[idx][1]
            bets.append(bet_cls(amt))
        return bets

    def resolve_bets(self, bets, roll, point=None):
        unresolved = []
        for bet in bets:
            if point is None:
                net = bet.resolve_on_come_out(roll)
            else:
                net = bet.resolve_point_phase(roll, point)

            if net is not None:
                self.player.adjust_chips(net)
            else:
                # still unresolved (carries to point phase only if point exists)
                if point is None:
                    unresolved.append(bet)
                else:
                    unresolved.append(bet)

        return unresolved

    def play_round(self):
        bets = self.collect_bets()
        if not bets:
            print("No bets placed. Skipping round.")
            return

        # Come-out roll
        d1, d2 = self.roll_dice()
        total = d1 + d2
        print(f"\nCome‑out roll: {d1} + {d2} = {total}")

        unresolved = self.resolve_bets(bets, total)
        if not unresolved:
            return

        # Point established
        point = total
        print(f"Point is {point}. Rolling until resolved...")
        while unresolved:
            d1, d2 = self.roll_dice()
            total = d1 + d2
            print(f"  Rolled {d1} + {d2} = {total}")
            unresolved = self.resolve_bets(unresolved, total, point)


def main():
    player = Player(starting_chips=100)
    game = CrapsGame(player)

    print("Welcome to OOP Craps with multi‑bets!")
    while player.chips > 0:
        game.play_round()
        if player.chips <= 0:
            print("\nYou’re out of chips — game over!")
            break
        again = input("\nPlay another round? (y/n) ").lower()
        if again != 'y':
            break
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
