from stdiomask import getpass
from passlib.hash import pbkdf2_sha256
import os
import re

# Defines a function to validate a password
def validate(password):
    if len(password) < 7:
        val = True
    elif not re.search("[a-z]", password):
        val = True
    elif not re.search("[A-Z]", password):
        val = True
    elif not re.search("[0-9]", password):
        val = True
    elif not re.search("[_@$]", password):
        val = True
    elif re.search("\s", password):
        val = True
    else:
        val = False
    
    return val
    
    


# Defines a function for signing up
def sign_up(val):
    # Try to open our details file
    try:
        f = open("account_details.txt", "r")
    
    # If that doesn't work, create the file, then open it
    except FileNotFoundError:
        f = open("account_details.txt", "x")
        f.close
        f = open("account_details.txt", "r")    
    
    # So the user knows what's up
    print("\n---Signup---")
    
    # This while loop runs until appropriate details are entered or they choose to leave
    while True:
        # Ask the user to enter their name and username
        name = input("Please enter your name: ").title()
        
        enter_username = True
        
        while enter_username:
            username = input("Please choose a username (It cannot contain a space): ")        
            if re.search("\s", username):
                print("That username contained a space")
            else:
                enter_username = False
        
        # Read each line of our file
        for line in f.readlines():
            # Extract the user's details from the line
            details = line.strip().split()
            # We only want to use the username, which is in the first column
            details = details[0]
            
            # If their username is in our database, we must ask them to enter a different one
            if username == details:
                # We do this as many times as needed until we get a unused username
                while True:
                    # Tell them their username is already being used
                    print("\nThat username is already in use")
                    
                    # Ask if they want to switch to login, if they do, run login
                    switch_to_login = input("Do you want to login instead? (Y/N) ").upper()[0]
                    
                    if switch_to_login == "Y":
                        login()
                        return
                    
                    # Ask them if they want to try with a new username, if they do, let them
                    again = input("Do you want to sign up with a different username? (Y/N) ").upper()[0]
                    
                    if again == "Y":
                        username = input("Please choose a username: ")
                    else:
                        return
                    
                    if username != details:
                        break
        
        # If the previous code ran through without anything happening,
        # then their username was unique and we can stop checking it
        break
    
    
    # They now need to enter a password
    password = "a"
    password2 = "b"
    
    # If their inputs don't match, they need to enter it again until they do
    while password != password2:    
    
        # In theory, getpass should make that input invisible, but it doesn't work in Spyder
        print("""Your password must be over 6 digits, contain uppercase and lowercase letters, 
              at least one number, at least one special character and no spaces""")
        password = getpass("Please enter a password: ").encode()
        
        while val:    
            val = validate(password)
            
            if val:
                print("Your password is missing one or more of the requirements")
                print("""Your password must be over 6 digits, contain uppercase and lowercase letters, 
                      at least one number, at least one special character and no spaces""")
            
                password = getpass("Please enter a password: ").encode()
        
        password2 = getpass("Please enter your password again: ").encode()
        
        if password == password2:
            break
        else:
            print("\nYou entered your passwords differently. Make sure you enter the same password")
    

    # Hash the password using passlib
    password = pbkdf2_sha256.hash(password)
    
    # Store their details to a list, adding formatting
    details = [username, " ", password, " ", name, "\n"]


    # Open our account details file in append mode
    f = open("account_details.txt", "a")
    
    # Add the new details to a new line
    f.writelines(details)
     
    # Let them know it's worked
    print(f"\nWelcome {username} You have successfully created an account")
    
    f.close()


# A function to log the user in
def login():
    # Let them know they're logging in
    print("\n---Login---")
    
    # Try and open the details file
    try:
        f = open("account_details.txt", "r")
        # IF the file is empty, give them the option to sign up instead
        if os.stat("account_details.txt").st_size == 0:
            print("There are no user details in the file, you must sign up to create one")
        
            while True:
                switch_to_sign = input("Do you want to sign up now? (Y/N) ").upper()[0]
                if switch_to_sign == "Y":
                    sign_up()
                    return
                elif switch_to_sign == "N":
                    return
                else:
                    print("\nPlease only answer yes or no") 
        
    # If that doesn't work, tell them why
    except FileNotFoundError:
        print("\nThere is no username file, you must sign up to create one")
        
        # And give them the option to sign up instead
        while True:
            switch_to_sign = input("Do you want to sign up now? (Y/N) ").upper()[0]
            if switch_to_sign == "Y":
                sign_up()
                return
            elif switch_to_sign == "N":
                return
            else:
                print("\nPlease only answer yes or no")   
    
    # Set our checker that we'll use later
    invalid_input = False
    
    # This loop runs until the entered details match a user,
    # or the user chooses to leave
    while True:
        # Get them to enter their details
        username = input("Username: ")
        password = getpass("Password: ").encode()
        
        # Run through our file, and extract details
        for line in f.readlines():
            details = line.strip().split()
            
            # If the username matches, hash the password
            if username == details[0]:
                encrypted_password = details[1]
                
                # If that matches, they're in
                if pbkdf2_sha256.verify(password, encrypted_password):
                    print(f"\nWelcome {details[3]}!")
                    return
    
        # This option only becomes relevant on later iterations of the loop
        if invalid_input:
            print()
            
        # The first time the loop runs, this is what it will show
        else:
            print("\nThe username or password is incorrect")
    
        # Ask them if they want to try again
        again = input("Do you want to try again? (Y/N) ").upper()[0]
        
        # If so, run the whole login process again
        if again == "Y":
            f.seek(0)
            username = input("Username: ")
            password = getpass("Password: ").encode()
            
            
            for line in f.readlines():
                details = line.strip().split()
        
                # If the username matches, hash the password
                if username == details[0]:
                    encrypted_password = details[1]
                    
                    # If that matches, they're in
                    if pbkdf2_sha256.verify(password, encrypted_password):
                        print(f"\nWelcome {details[3]}!")
                        return
            
            print("The username or password is incorrect")
    

        # If they say no, ask them if they want to sign up instead        
        elif again == "N":
            while True:
                switch_to_sign = input("Do you want to create an account? (Y/N) ").upper()[0]
            
                # If yes, run sign_up, if not, leave the function
                if switch_to_sign == "Y":
                    sign_up()
                    return
                elif switch_to_sign == "N":
                    return
                else:
                    print("\nPlease enter a valid answer (Yes or No)")
                    
            
        # If they enter something weird, ask them to enter it normally
        else:
            print("\nPlease enter a valid answer (Yes or No)")
            
            # Next time the while loop runs, don't show the "incorrect details" message
            invalid_input = True
    
    f.close()


# Decide if you want to have the passwords validated
val = True

# Ask them if they have an account
print("Welcome to generic account services")
action = input("Do you already have an account? (Y/N) ").upper()[0]

# If they don't, run signup. If they do, run login
if action == "N":
    sign_up(val)
elif action == "Y":
    login()

# This allows them to do either option as many times as they need
while True:
    
    # Ask them a series of questions about what they might want to do,
    # Depending on their answers, lead them to a function or end the program
    again = input("Do you want to do anything else? (Y/N) ").upper()[0]
    
    if again == "N":
        print("\nOkay, goodbye!")
        break
    
    elif again == "Y":
        sign_up_choice = input("Do you want to create an account? (Y/N) ").upper()[0]
        
        if sign_up_choice == "Y":
            sign_up(val)
            
        else:
            login_choice = input("Do you want to log in? (Y/N) ").upper()[0]
            
            if login_choice == "Y":
                login()
                
            elif login_choice == "N":
                print("\nOkay, goodbye!")
                break
            
            else:
                print("\nPlease only answer with a yes or no")
