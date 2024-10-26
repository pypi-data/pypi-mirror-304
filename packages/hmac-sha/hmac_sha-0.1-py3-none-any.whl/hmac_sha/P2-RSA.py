import math
p=3
q=7
n=p*q

print("N =",n)
phi = (p-1)*(q-1)

e=2

while(e<phi):
    if(math.gcd(e,phi)==1):
        break
    else:
        e += 1

print("E =",e)

k=2
d=((k*phi)+1)/e
print("D =",d)
print("Public Key:",e,n)
print("Private Key:",d,n)

msg=11
print("Original Message:",msg)

C = pow(msg,e)
C = math.fmod(C,n)
print("Encrypted message:",C)

M = pow(C,d)
M = math.fmod(M,n)
print("Decrypted Message:",M)