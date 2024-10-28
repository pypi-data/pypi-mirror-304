import numpy as np
def readmatrix(m,n):
    tot_ele=m*n
    print("Enter the elements of the matrix")
    A=np.zeros(tot_ele)
    A=np.reshape(A,(m,n))
    for i in range(m):
        for j in range(n):
            A[i,j]=int(input())
    return(A)


def add_matrix(A,B):
    size=A.shape
    row=size[0]
    col=size[1]
    tot_ele=row*col
    RES=np.zeros(tot_ele)
    RES=np.reshape(RES,(row,col))
    for i in range(row):
        for j in range(col):
            RES[i,j]=A[i,j]+B[i,j]
    return(RES)


def sub_matrix(A,B):
    size=A.shape
    row=size[0]
    col=size[1]
    tot_ele=row*col
    RES=np.zeros(tot_ele)
    RES=np.reshape(RES,(row,col))
    for i in range(row):
        for j in range(col):
            RES[i,j]=A[i,j]-B[i,j]
    return(RES)

def mul_matrix(A,B):
    size=A.shape
    row=size[0]
    col=size[1]
    tot_ele=row*col
    RES=np.zeros(tot_ele)
    RES=np.reshape(RES,(row,col))
    for i in range(row):
        for j in range(col):
            for k in range(row):
                RES[i,j]+=A[i,k]*B[k,j]
    return(RES)

def transposematrix(A):
    RES=np.zeros((A.shape[1],A.shape[0]))
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            RES[j,i]=A[i,j]      
    return(RES)

def printmatrix(A):
    size=A.shape
    row=size[0]
    col=size[1]
    print("Elements of the matrix")
    for i in range(col):
        for j in range(row):
            print(A[i,j],end="")
        print(end='\n')
