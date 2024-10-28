mylist=[]
N=int(input("Enter the number of elements:"))
for i in range(N):
  no=int(input("Enter the value:"))
  mylist.append(no)
ev_li=[]
od_li=[]
for i in mylist:
  if(i%2==0):
    ev_li.append(i)
  else:
    od_li.append(i)
print("Even lists:",ev_li)
print("Odd lists:",od_li)
