import random

def play():
    user = input("Enter 'rock', 'paper', or 'scissors': ").lower()
    computer = random.choice(['rock', 'paper', 'scissors'])
    print('\nThe computer randomly entered "{}".'.format(computer))
    return user, computer
def user_win(player, opponent):
    if (player == 'rock' and opponent =='scissors') or (player == 'scissors' and opponent == 'paper') or (player == 'paper' and opponent == 'rock'):
        return 'Game result: you won!\n'
    elif player == opponent:
        return 'Game result: it\'s a tie!\n'
    
    elif player not in ['rock','paper','scissors']:
        return 'Oops, enter a correct word.'
    else:
        return 'Game result: you lost!'

def script():
    player, opponent = play()

    print(user_win(player,opponent))
    restart = input("Would you like to try again?")
    if restart == "yes":
        return script()
    if restart == "no":
        print("Thank you for playing.")
        
script()