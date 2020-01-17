# Example Input:
# Please give a number as 1st variable: 1 (e.g. int a=1)
# Please give a number as 2nd variable: 2 (e.g. int b=2)
# Note: You’re not allowed to use another variable, such as (int c) or (int temp), inside the code/program/algorithm.
# The output will be the values of the input variables that were swapped.
# Example Output:
# The value of the 1st variable: 2 (e.g. int a)
# The value of the 2nd variable: 1 (e.g. int b)

a = int(input('Please give a number as 1st variable: '))
b = int(input('Please give a number as 2nd variable: '))

a = a + b
b = a - b
a = a - b

print("\nThe value of the 1st variable:", a)
print("The value of the 2nd variable:", b)
