import random

total_chips = 5
total_amount = 100

print("Welcome to the Craps game.")

def craps_game():
    total_bet = int(input("How much will you bet? "))  # Fixed input syntax
    
    while True:
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        first_roll = dice1 + dice2

        # Base cases
        if first_roll == 7 or first_roll == 11:  # Fixed comparison operators
            # Update chips: don't return chips on loss or calculate for win return
            total_bet = total_bet * 2
            return total_bet
        
        if first_roll == 2 or first_roll == 3 or first_roll == 12:  # Fixed comparison operators
            # Lower the total_bet as it's a loss
            total_bet = total_bet / 2
            return total_bet
        else:
            point_roll = first_roll  # Assuming it's the point number

            while True:
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                second_roll = dice1 + dice2
                
                if second_roll == point_roll:  # Fixed comparison operator
                    print("Player wins!")
                    break
                elif second_roll == 7:  # Fixed condition
                    print("Player loses!")
                    break
