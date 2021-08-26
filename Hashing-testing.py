#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 17:21:17 2021

@author: pin
"""
import hashlib
import os
from passlib.hash import pbkdf2_sha256

# Get the password from the user
password = input("Password: ")
'''
# Generate a random salt, 16 bytes long
salt = os.urandom(16)

print(salt.hex())

# Combine them using the most secure hashing algorithm I could find in hashlib
password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)

# Print the result in hexidecimal form
print(password.hex())
'''

# This is how passlib hashing works
hashed = pbkdf2_sha256.hash(password)

print(hashed)

hashed = pbkdf2_sha256.hash(password)

print(hashed)

print(pbkdf2_sha256.verify(password, hashed))
