#Check if a Given Key Already Exists in Dictionary
# Creating a Dictionary
D1 = {'first_name': 'Jim', 'age': 23, 'height': 6.0, 'job': 'developer', 'company': 'XYZ'}


def check_key(x):
    if x in D1:
        return 'Yes'
    else:
        return 'No'


print("Is key named 'first_name' present?", check_key('first_name'))
print("Is key named 'jobs' present?", check_key('jobs'))