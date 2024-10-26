def prime_checker(p):
    if p < 1:
        return -1
    elif p > 1:
        if p == 2:
            return 1
        for i in range(2,p):
            if p%i == 0:
                return -1
            return 1
        
def primitive_check(g,p,L):
    for i in range(1,p):
        L.append(pow(g,i)%p)
    for i in range(1,p):
        if L.count(i)>1:
            L.clear()
            return -1
        return 1
    
l = []

P = int(input("Enter P: "))
while l:
    if prime_checker(P)==-1:
        print("Number is Not Prime, Please Enter Again!")
        continue
    break

G = int(input(f"Enter The Primitive root of {P}: "))
while l:
    if primitive_check(G,P,l)==-1:
        print(f"Number is not a primitive root of {P}, Please try again!")
        continue
    break

x1,x2 = int(input("Enter The private key of user 1 : ")),int(input("Enter the private key of user 2 : "))

while l:
    if x1 >= P or x2 >= P:
        print(f"Private key of both the user should be less than {P}!")
        continue
    break

y1,y2 = pow(G,x1)%P,pow(G,x2)%P
k1,k2 = pow(y2,x1)%P,pow(y1,x2)%P
print(f"\nSecret Key for user 1 is {k1}\nSecret key for user 2 is {k2}\n")

if k1==k2:
    print("Keys have been exchanged succesfully")
else:
    print("Keys have not been exchanged succesfully")