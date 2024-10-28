class mylist:
    def getinput(self):
        print("It is from List Class")
        self.list1=[]
        n=int(input("Enter the no of list elements:"))
        for i in range(n):
            element=int(input("Enter the list elements:"))
            self.list1.append(element)
    def additem(self):
        msum=0
        for i in self.list1:
            msum=msum+i
        print("Sum of list elements:",msum)

class mytuple:
    def getinput(self):
        print("It is from tuple class")
        self.tup1=[]
        n=int(input("Enter the no of tuple elements:"))
        for i in range(n):
            element=int(input("Enter the tuple elements:"))
            self.tup1.append(element)
        def additem(self):
            msum=0
            for i in self.tup1:
                msum=msum+i
            print("Sum of Tuple elements:",msum)
L1=mylist()
T1=mytuple()
for i in(L1,T1):
    i.getinput()
for i in(L1,T1):
    i.additem()
