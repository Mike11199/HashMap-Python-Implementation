# HashMap Implementation

This is the portfolio project for the Oregon State University course CS 261 - Data Structures, which is allowed to be posted to a public GitHub repo.  The project implements a HashMap data structure using two distinct methods to handle table collisions - Open Addressing, and Separate Chaining.


- **Open Addressing**
   - In this implementation, the data structure probes for an empty spot in the HashTable's underlying dynamic array if a collision occurs, until it finds an empty spot to insert the element in. 

- **Separate Chaining**
   - In this implementation, each dynamic array element is a linked list, and additional key/value pairs can be added to the front of the linked list at each array spot in the case that keys hash to the same array index. 

</br>

# Hash Function

A hash function is a non-reversible function which converts data to a positive integer.  The modulus of this function result divided by the array capacity is used to place a key/value pair into the underlying dynamic array data structure.  A simmple hash function is used in this implementation, which uses the "ord" function to extract the unicode code for each number/char of the input, and multiplies it by the index of the element.  These are all summed to produce the result.    

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
