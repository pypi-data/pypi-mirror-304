import numpy as np
rows=int(input("Enter the number of rows:"))
cols=int(input("Enter the number of cols:"))

print("\nEnter  elements  for the 1st matrix")
matrix1=[]
for i in range(rows):
  row=[]
  for j in range(cols):

    element=int(input())
    row.append(element)
  matrix1.append(row)
matrix1=np.array(matrix1)

print("\nEnter  elements  for the 2nd matrix")
matrix2=[]
for i in range(rows):
  row=[]
  for j in range(cols):

    element=int(input())
    row.append(element)
  matrix2.append(row)
matrix2=np.array(matrix2)

result=matrix1+matrix2

print("\n1st Matrix:")
print(matrix1)

print("\n2nd Matrix:")
print(matrix2)

print("\n Sum of matrices:")
print(result   )
