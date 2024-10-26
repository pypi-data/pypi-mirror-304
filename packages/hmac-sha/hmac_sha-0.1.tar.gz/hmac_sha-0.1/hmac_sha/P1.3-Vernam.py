def stringEncryption(text,key):
    cipherText = ""
    cipher = []
    for i in range(len(key)):
        cipher.append(ord(text[i]) - ord('A') + ord(key[i]) - ord('A'))
    for i in range(len(key)):
        if cipher[i] > 25:
            cipher[i] = cipher[i] -26
    for i in range(len(key)):
        x = cipher[i] + ord('A')
        cipherText += chr(x)
    return cipherText

plainText = "HelloTYCS"
key = "MONEYBANK"
encryptedText = stringEncryption(plainText.upper(),key.upper())
print("Cipher Text - ",encryptedText)