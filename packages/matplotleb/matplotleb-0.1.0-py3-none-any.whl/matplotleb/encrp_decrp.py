plaintext=input("Enter a one word,lowercase or uppercase:")
distance=int(input("Enter a distance value:"))
code=""
for ch in plaintext:
    ordvalue=ord(ch)
    ciphervalue=ordvalue+distance
    if'a'<=ch<='z':
        if ciphervalue>ord('z'):
            dis=ciphervalue-ord('z')-1
            ciphervalue=ord('a')+dis
    elif'A'<=ch<='Z':
        if ciphervalue>ord('Z'):
            dis=ciphervalue-ord('Z')-1
            ciphervalue=ord('A')+dis

    code+=chr(ciphervalue)
print(code)
decode=""
for ch in code:
    ordvalue=ord(ch)
    ciphervalue=ordvalue-distance
    if'a'<=ch<='z':
        if ciphervalue<ord('a'):
            dis=ord('a')-ciphervalue-1
            ciphervalue=ord('z')-dis
    elif'A'<=ch<='Z':
        if ciphervalue<ord('A'):
            dis=ord('A')-ciphervalue-1
            ciphervalue=ord('Z')-dis
    
    decode+=chr(ciphervalue)
print(decode)
