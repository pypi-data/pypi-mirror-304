def encrypt_text(plaintext,n):
    ans = ""
    for i in range(len(plaintext)):
        ch = plaintext[i]
        if ch=="":
            ans+=""
        elif (ch.isupper()):
            ans += chr((ord(ch)+ n-65)%26+65)
        else:
            ans += chr((ord(ch) + n-97) %26+97)
    return ans

plaintext = "HELLO TYCS Caesar Cipher"
n = 1
print("Plain Text is: ",plaintext)
print("Shift Pattern is: ",str(n))
print("Cipher Text is: ",encrypt_text(plaintext,n))