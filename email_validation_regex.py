import re
email_cond="^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"
user_email=input("enter the email: ")
if re.search(email_cond,user_email):
    print("right email")
else:
    print("wrong email")