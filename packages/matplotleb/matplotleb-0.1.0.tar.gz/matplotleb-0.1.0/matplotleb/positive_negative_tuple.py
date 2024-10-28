n=int(input("Enter the number of elements:"))
positive_tuple=()
negative_tuple=()
for i in range(n):
    num=int(input("Enter a number:"))
    if num>=0:
        positive_tuple+=(num,)
    else:
        negative_tuple+=(num,)
print("\n Positive Numbers Tuple:",positive_tuple)
print("\n Negative Numbers Tuple:",negative_tuple)
