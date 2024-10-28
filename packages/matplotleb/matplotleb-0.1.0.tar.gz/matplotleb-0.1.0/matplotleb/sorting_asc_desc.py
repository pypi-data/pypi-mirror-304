def sort(num,order):
    n=len(num)
    for i in range(n-1):
        for j in range(n-i-1):
            if(order=="asc" and num[j]>num[j+1])or(order=="desc" and num[j]<num[j+1]):
                num[j],num[j+1]=num[j+1],num[j]
    return num
num_count=int(input("Enter the number of elements:"))
num=[]
for i in range(num_count):
    nums=int(input(f"Enter element{i+1}:"))
    num.append(nums)

print("Original list:",num)

print("Sorted in ascending order:",sort(num,"asc"))

print("Sorted in descending order:",sort(num,"desc"))
