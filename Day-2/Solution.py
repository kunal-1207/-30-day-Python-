# Day 2
# Challenge: Write a function to find duplicates in a list.
# Focus: functions, loops
# Example Hint: Use sets

def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)
lst = [1, 2, 3, 4, 5, 1, 2, 3]
print(find_duplicates(lst))  
