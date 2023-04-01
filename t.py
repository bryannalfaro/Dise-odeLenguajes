dictionary = {'a':[1,2],'b':[[2],[3]]}

#count the amount of nested lists in the dictionary
def count_nested_lists(dictionary):
    count = 0
    for key in dictionary:
        for value in dictionary[key]:
            if isinstance(value,list):
                count += 1
    return count

b = count_nested_lists(dictionary['a'])
print(b)