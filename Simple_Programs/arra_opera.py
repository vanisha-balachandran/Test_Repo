x = [1,3,2,6,7,9,10,4,5]
print("Original List value of x :" + str(x))
'''
print("Append a list")
x.append(8)
print(x)
print("**********************")
print("Extend a list")
x.extend([8, 'Geeks', 'Always'])
print(x)
print("**********************")
print("Insert to a list")
x.insert(3, "check")
print(x)
print("**********************")
print("Remove from a list")
x.remove(3)
print(x)
print("**********************")
print("Pop from a list")
x.pop(4)
print(x)
print("**********************")
print("Reverse a list")
x.reverse()
print(x)
print("**********************")
print("Length a list")
a = len(x)
print(a)
print("**********************")
y = [1,6,3,4,8,2]
print("min & max a list")
print("Min Val = %d, Max Value = %d"%(min(y),max(y)))
print("**********************")
print("Count a occurance in a list")
a = x.count(8)
print(a)
print("**********************")
print("Concatenate two list")
a = ['s','a','i']
c = x + a
print(c)
print("**********************")

#zip lists
test_list1 = [[1, 3], [4, 5], [5, 6]]
test_list2 = [[7, 9], [3, 2], [3, 10]]

# printing original lists
print("The original list 1 is : " + str(test_list1))
print("The original list 2 is : " + str(test_list2))

# using map() + __add__
# zipping lists of lists
res = list(map(list.__add__, test_list1, test_list2))

# printing result
print("The modified zipped list is : " + str(res))
'''


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


# Driver Code
lst1 = [15, 9, 10, 56, 23, 78, 5, 4, 9]
lst2 = [9, 4, 5, 36, 47, 26, 10, 45, 87]
print(intersection(lst1, lst2))