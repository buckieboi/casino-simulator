import tkinter as tk
from tkinter import ttk, messagebox
import random
from abc import ABC, abstractmethod

DENOMINATIONS = [5, 10, 25, 50, 100]

# --- BET CLASSES ---
class Bet(ABC):
    name = "Bet"
    carries = False  # Does this bet carry into the point phase?

    def __init__(self, amount):
        self.amount = amount

    @abstractmethod
    def resolve(self, roll, point):
        """
        Resolve this bet for a given roll.
        roll: int sum of dice
        point: current point or None
        Returns (net, carries) where net is win(+) or loss(-) or 0, and carries is bool
        """
        pass

class PassLineBet(Bet):
    name = "Pass Line"
    carries = True

    def resolve(self, roll, point):
        if point is None:
            if roll in (7, 11):
                return self.amount, False
            elif roll in (2, 3, 12):
                return -self.amount, False
            else:
                return 0, True  # establish point
        else:
            if roll == point:
                return self.amount, False
            elif roll == 7:
                return -self.amount, False
            else:
                return 0, True

class FieldBet(Bet):
    name = "Field"
    carries = False

    def resolve(self, roll, point):
        # Only resolves on any roll
        if roll in (3, 4, 9, 10, 11):
            return self.amount, False
        elif roll in (2, 12):
            return self.amount * 2, False
        else:
            return -self.amount, False

class SnakeEyesBet(Bet):
    name = "Snake Eyes (2)"
    carries = False

    def resolve(self, roll, point):
        return (self.amount * 30, False) if roll == 2 else (-self.amount, False)

class AnySevenBet(Bet):
    name = "Any Seven (7)"
    carries = False

    def resolve(self, roll, point):
        return (self.amount * 4, False) if roll == 7 else (-self.amount, False)

class YoBet(Bet):
    name = "Yo (11)"
    carries = False

    def resolve(self, roll, point):
        return (self.amount * 15, False) if roll == 11 else (-self.amount, False)

BET_CLASSES = [PassLineBet, FieldBet, SnakeEyesBet, AnySevenBet, YoBet]

# --- GUI APPLICATION ---
class CrapsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Casino Craps Simulator")
        self.geometry("800x600")
        self.resizable(False, False)

        self.player_chips = 100
        self.current_bets = []  # list of Bet instances
        self.point = None

        self._build_widgets()

    def _build_widgets(self):
        # Top frame: chips and status
        top = ttk.Frame(self, padding=10)
        top.pack(fill='x')
        self.chips_var = tk.StringVar(value=f"Chips: {self.player_chips}")
        ttk.Label(top, textvariable=self.chips_var, font=('Arial', 16)).pack(side='left')
        self.point_var = tk.StringVar(value="Point: None")
        ttk.Label(top, textvariable=self.point_var, font=('Arial', 16)).pack(side='right')

        # Middle: bets selection
        bets_frame = ttk.LabelFrame(self, text="Place Your Bets", padding=10)
        bets_frame.pack(fill='x', padx=10, pady=5)
        self.bet_vars = []  # (check_var, amount_var)
        for idx, cls in enumerate(BET_CLASSES):
            row = ttk.Frame(bets_frame)
            row.grid(row=idx, column=0, sticky='w', pady=2)
            check_var = tk.IntVar(value=0)
            cb = ttk.Checkbutton(row, text=cls.name, variable=check_var)
            cb.pack(side='left')
            amt_var = tk.StringVar(value=str(DENOMINATIONS[0]))
            om = ttk.OptionMenu(row, amt_var, DENOMINATIONS[0], *DENOMINATIONS)
            om.pack(side='left', padx=10)
            self.bet_vars.append((cls, check_var, amt_var, cb, om))

        # Buttons: Place Bets, Roll
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill='x')
        self.place_btn = ttk.Button(btn_frame, text="Place Bets", command=self.place_bets)
        self.place_btn.pack(side='left', padx=5)
        self.roll_btn = ttk.Button(btn_frame, text="Roll Dice", command=self.roll_dice, state='disabled')
        self.roll_btn.pack(side='left', padx=5)

        # Log area
        log_frame = ttk.LabelFrame(self, text="Game Log", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.log_text = tk.Text(log_frame, state='disabled', wrap='word')
        self.log_text.pack(fill='both', expand=True)

    def log(self, msg):
        self.log_text.config(state='normal')
        self.log_text.insert('end', msg + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def place_bets(self):
        # Clear previous round
        self.current_bets.clear()
        # Read selections
        for cls, check_var, amt_var, cb, om in self.bet_vars:
            if check_var.get():
                try:
                    amt = int(amt_var.get())
                except ValueError:
                    messagebox.showerror("Invalid Bet", f"Enter a valid amount for {cls.name}.")
                    return
                if amt > self.player_chips:
                    messagebox.showerror("Insufficient Chips", f"Not enough chips for {cls.name}.")
                    return
                self.player_chips -= amt
                bet = cls(amt)
                self.current_bets.append(bet)

        if not self.current_bets:
            messagebox.showwarning("No Bets", "Select at least one bet.")
            return

        # Update UI
        self.update_chips()
        self.log(f"Placed bets: {', '.join(f'{b.amount} on {b.name}' for b in self.current_bets)}")
        # Disable bet controls
        for _, _, _, cb, om in self.bet_vars:
            cb.config(state='disabled')
            om.config(state='disabled')
        self.place_btn.config(state='disabled')
        self.roll_btn.config(state='normal')
        # Reset point for this round
        self.point = None
        self.point_var.set("Point: None")

    def roll_dice(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        total = d1 + d2
        self.log(f"Rolled {d1} + {d2} = {total}")

        new_bets = []
        for bet in self.current_bets:
            net, carries = bet.resolve(total, self.point)
            if net != 0:
                self.player_chips += net
                outcome = "wins" if net > 0 else "loses"
                self.log(f"{bet.name} {outcome} {abs(net)} chips.")
            else:
                self.log(f"{bet.name} pushes.")
            if carries:
                new_bets.append(bet)

        self.current_bets = new_bets
        self.update_chips()

        # Establish or clear point
        if self.point is None and any(isinstance(b, PassLineBet) for b in new_bets):
            self.point = total
            self.point_var.set(f"Point: {self.point}")
            self.log(f"Point is set to {self.point}.")

        # End of round
        if not self.current_bets:
            self.log("Round complete. Place new bets.")
            self.end_round()

    def end_round(self):
        # Re-enable bet controls
        for _, _, _, cb, om in self.bet_vars:
            cb.config(state='normal')
            om.config(state='normal')
        self.place_btn.config(state='normal')
        self.roll_btn.config(state='disabled')
        self.point = None
        self.point_var.set("Point: None")

    def update_chips(self):
        self.chips_var.set(f"Chips: {self.player_chips}")

if __name__ == "__main__":
    app = CrapsApp()
    app.mainloop()
