#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
TODO instead of getpass, use stdiomask
it has to be installed, which I don't think I can do on the VM
https://pypi.org/project/stdiomask/
also don't know if it will work in the IDE

'''

from getpass import getpass
import hashlib
import os


# Defines a function for signing up
def sign_up():
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
        username = input("Please choose a username: ")        
        
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
    # In theory, getpass should make that input invisible, but it doesn't work in Spyder
    password = getpass("Please enter a password: ").encode()
    password2 = getpass("Please enter your password again: ").encode()
    
    # If their inputs don't match, they need to enter it again until they do
    while password != password2:
        print("\nYou entered your passwords differently. Make sure you enter the same password")
        password = getpass("Please enter a password: ").encode()
        password2 = getpass("Please enter your password again: ").encode()


    # Generate a random salt, 16 bytes long
    salt = os.urandom(16)
    
    # Convert it to hex to save, and convert it to hex then bytes to use
    salt_save = str(salt.hex())
    salt = salt.hex().encode()
    
    # Salt and hash the password (in the most secure way I can work out using hashlib)
    # This hashes it 100000 times using the protocol sha256 
    password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    
    # Convert back to a string for writing to the file
    password = str(password.hex())
    
    # Store their details to a list, adding formatting
    details = [username, " ", password, " ", salt_save, " ", name, "\n"]


    # Open our account details file in append mode
    f = open("account_details.txt", "a")
    
    # Add the new details to a new line
    f.writelines(details)
    
    # Let them know it's worked
    print("You have successfully created an account")
    
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
                
                salt = details[2].encode()
                password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
                
                # If that matches, they're in
                if password.hex() == details[1]:
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
        
                if username == details[0]:
                    salt = details[2].encode()
                    
                    password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
                    
                    if password.hex() == details[1]:
                        print(f"\nWelcome {details[3]}!")
                        return

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

# Ask them if they have an account
print("Welcome to generic account services")
action = input("Do you already have an account? (Y/N) ").upper()[0]

# If they don't, run signup. If they do, run login
if action == "N":
    sign_up()
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
            sign_up()
            
        else:
            login_choice = input("Do you want to log in? (Y/N) ").upper()[0]
            
            if login_choice == "Y":
                login()
                
            elif login_choice == "N":
                print("\nOkay, goodbye!")
                break
            
            else:
                print("\nPlease only answer with a yes or no")
