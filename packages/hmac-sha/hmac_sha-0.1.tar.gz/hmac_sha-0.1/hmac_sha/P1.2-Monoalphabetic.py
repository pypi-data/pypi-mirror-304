def encrypt(message, key):
    cipher = ""
    for i in message:
        if i.isupper():
            cipher += chr((ord(i) + key - 65) % 26+65)
        elif i.islower():
            cipher += chr((ord(i)+ key - 97) % 26+97)
        else:
            cipher+=""
    return cipher

message = input("Enter the plain text: ")
key = input("enter the key: ")
if key.isupper():
    key = ord(key) - 65
elif key.islower():
    key = ord(key) - 97
else:
    key = int(key)
print("Cipher text:",encrypt(message,key))