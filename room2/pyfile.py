import bcrypt

enter = input("Password: ")
entered = enter.encode()

with open ("pass.hash", "rb") as p:
    passw = p.read()

if bcrypt.checkpw(entered, passw):
    print (f"correct {enter}")
else:
    print ("stupid")
