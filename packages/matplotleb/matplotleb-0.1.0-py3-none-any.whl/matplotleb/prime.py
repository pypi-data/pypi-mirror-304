def is_Prime(n):
  if n<=1:
    return False
  for i in range(2, (N//2)+1):
    if n%i == 0:
       return False
    return True
N=int(input("Enter the no. of elements:"))
NUMLIST=[]
PRIMELIST=[]
NONPRIMELIST=[]
for i in range(N):
  number=int(input("Enter a number:"))
  NUMLIST.append(number)
  if is_Prime(number):
    PRIMELIST.append(number)
  else:
    NONPRIMELIST.append(number)
count_primes=len(PRIMELIST)
count_nonprimes=len(NONPRIMELIST)
print("\n All elements of NUMLIST:",NUMLIST)
print(f"Count of prime numbers:{count_primes }, Elements of PRIME LIST:{PRIMELIST}")
print(f"Count of non prime numbers:{count_nonprimes}, Elements of NONPRIME LIST :{NONPRIMELIST}")
