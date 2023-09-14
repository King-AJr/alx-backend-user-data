#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = "bob@bob.com"
password = "MyPwdOfBob"
auth = Auth()

auth.register_user(email, password)

reset_pass = auth.get_reset_password_token(email)
print(reset_pass)
password = "retwdgf"
print(auth.update_password(reset_pass, password))
