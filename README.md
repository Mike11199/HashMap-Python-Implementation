# HashMap Implementation

This is the portfolio project for the Oregon State University course CS 261 - Data Structures, which is allowed to be posted to a public GitHub repo.

The project implements a HashMap data structure using two distinct methods to handle table collisions - Open Addressing and Separate Chaining.  Open Addressing probes for an empty spot in the HashTable's underlying dynamic array if a collision occurs.  In Separate Chaining, each dynamic array element is a linked list, and additional key/value pairs can be added to the linked list at each array spot in the case that keys hash to the same array index. 


# Hash Function

A hash map uses a function to convert data to a positive integer, that can be used to then place a key/value pair into a dynamic array data structure.    

```python
def hash_function_2(key: str) -> int:
    """Sample Hash function #2 to be used with HashMap implementation"""
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash
```
