import random

def craps_game(chips):
    # Ask for a valid bet amount
    # ask user for bet
    # check  user bet too much
    # check if bet positive
    # check if value is a valid number.
    while True:
        try:
            bet = int(input("How much will you bet? "))
            if bet > chips:
                print("You cannot bet more than you have! You have", chips, "chips.")
            elif bet <= 0:
                print("Bet must be a positive amount.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    
    # Come-out roll
    # the first roll is made and informed to user.
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    first_roll = dice1 + dice2
    print(f"\nYou rolled {dice1} + {dice2} = {first_roll}")

    # Immediate win/loss conditions
    # check if first roll is 7 or 11 then user wins first time. update current chips from bet
    # if 2,3,12 made first froll user loses and loses bet.
    # past the point: first roll becomes point and inform user. 
    # make another roll update user on roll and keep checking if point number is made which is win, if 7 hit then loss, any other number keep rolling.
    if first_roll in (7, 11):
        print("Natural! You win!")
        chips += bet
    elif first_roll in (2, 3, 12):
        print("Craps! You lose!")
        chips -= bet
    else:
        # Establish the point
        point = first_roll
        print("Your point is now", point)
        while True:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            roll = dice1 + dice2
            print(f"You rolled {dice1} + {dice2} = {roll}")
            if roll == point:
                print("You hit your point! You win!")
                chips += bet
                break
            elif roll == 7:
                print("You rolled a 7 before hitting your point. You lose!")
                chips -= bet
                break
    return chips

def main():
    #test case for playe with 100 chips and give ui. 
    # this is checking if user has chips remaining, and will end the game when user reaches 0.
    # this does not account  for negative chips, as user only can bet available chips (no credit.)
    # ask the player once the game is over if they want to play again every loss.
    #if player loses all chips then  the game force exits player out.
    chips = 100  # Starting chips
    print("Welcome to the Craps game!")
    
    while chips > 0:
        print("\nYou have", chips, "chips.")
        chips = craps_game(chips)
        if chips <= 0:
            print("You're out of chips! Game over.")
            break
        play_again = input("\nPlay again? (y/n): ")
        if play_again.lower() != 'y':
            break
    
    print("Thanks for playing!")

if __name__ == "__main__":
    main()


#need to add feature where every roll made asks you to be more
# make options of what to bet on new points or other constants.  bet on snake eyes, 1,2,3,4,5,6,7.


# missing features: other ai playing, betting against the player. 
# the ratio of bet affects how much can be made

#ui featueres
#html, css, minimal javascript or bootsrap
# run as a local page, but can we run it on render or netlify as public avaiable website?
# or just host it on github io as a public webpage just for convience.