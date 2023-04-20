def sublist(num_list):
    i = 0
    sublist = []
    while num_list[i] != 5 and i < len(num_list):
        sublist.append(num_list[i])
        i += 1
    return sublist
print(sublist([1,2,3,4,5]))