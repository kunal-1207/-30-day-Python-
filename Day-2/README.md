# Day 2 - Find Duplicates in a List

## Challenge

Write a function to find duplicates in a list.

**Focus:** Functions, Loops

**Hint:** Use sets to help identify duplicates efficiently.

---

## Program Overview

The goal of this program is to identify duplicate elements in a list using a function. The function `find_duplicates()` iterates over the input list and identifies any elements that occur more than once.

---

## Implementation

```python
# Define the function find_duplicates that takes a list as input

def find_duplicates(lst):
    # Initialize an empty set to track seen elements
    seen = set()
    # Initialize another set to track duplicate elements
    duplicates = set()

    # Iterate over each item in the input list
    for item in lst:
        # If the item is already in the seen set, it is a duplicate
        if item in seen:
            duplicates.add(item)
        else:
            # Otherwise, add it to the seen set
            seen.add(item)
    
    # Convert the duplicates set to a list and return it
    return list(duplicates)

# Sample list to test the function
lst = [1, 2, 3, 4, 5, 1, 2, 3]

# Print the output of the find_duplicates function
print(find_duplicates(lst))
```

---

## Line-by-Line Breakdown

1. **Function Definition:** `def find_duplicates(lst):`

   * This line defines a function named `find_duplicates` that accepts a single parameter `lst`, which is expected to be a list of elements.

2. **Initialize 'seen' Set:** `seen = set()`

   * This initializes an empty set named `seen` that will be used to track elements encountered in the list.

3. **Initialize 'duplicates' Set:** `duplicates = set()`

   * This initializes another empty set named `duplicates` to store the elements that occur more than once.

4. **For Loop:** `for item in lst:`

   * This loop iterates over each element (`item`) in the input list `lst`.

5. **Check for Duplicates:** `if item in seen:`

   * If the current `item` is already in the `seen` set, it is added to the `duplicates` set.

6. **Add to Seen Set:** `else: seen.add(item)`

   * If the `item` is not in the `seen` set, it is added to the `seen` set for future checks.

7. **Return Duplicates as a List:** `return list(duplicates)`

   * The `duplicates` set is converted to a list before being returned to maintain consistency in data type.

8. **Test Data:** `lst = [1, 2, 3, 4, 5, 1, 2, 3]`

   * A sample list is defined to test the function.

9. **Function Call and Output:** `print(find_duplicates(lst))`

   * The `find_duplicates` function is called with the sample list, and the result is printed to the console.

---

## Expected Output

```
[1, 2, 3]
```

The program identifies `1`, `2`, and `3` as duplicate elements in the sample list.

---

## Key Concepts

* **Sets:** Used to track unique elements and identify duplicates efficiently.
* **Loops:** Iterate over each item in the list to check for duplicates.
* **Functions:** Encapsulate logic to make the program modular and reusable.

---

## Further Enhancements

* Allow the function to handle nested lists.
* Accept different data types and handle them appropriately.
* Implement error handling for invalid inputs.

---

Thank you for reviewing this README! Feel free to suggest improvements or ask for further explanations.
