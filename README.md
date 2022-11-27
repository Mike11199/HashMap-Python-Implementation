# HashMap Implementation

This is the portfolio project for the Oregon State University course CS 261 - Data Structures, which is allowed to be posted to a public GitHub repo.  The project implements a HashMap data structure using two distinct methods to handle table collisions - Open Addressing, and Separate Chaining.


- **Open Addressing**
   - In this implementation, the data structure probes for an empty spot in the HashTable's underlying dynamic array if a collision occurs, until it finds an empty spot to insert the element in. 

- **Separate Chaining**
   - In this implementation, each dynamic array element is a linked list, and additional key/value pairs can be added to the front of the linked list at each array spot in the case that keys hash to the same array index. 

</br>

# Hash Function

A hash function is a non-reversible function which converts data to a positive integer.  The modulus of this function result divided by the array capacity is used to place a key/value pair into the underlying dynamic array data structure.  A simple hash function is used in this implementation, which uses the "ord" function to extract the unicode code for each number/char of the input, and multiplies it by the index of the element.  These are all summed to produce the result.    

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


# Table Collisions

Reference https://betterexplained.com/articles/understanding-the-birthday-paradox/

A simplified way to view the chance of a hash table collision is by using the Birthday Paradox.  This is a non-intuitive paradox which states that in a room of 23 people, there is about a 50% chance two share the same birthday.

To explain this concept, we can take the combination of these 23 people, which is equal to 253. This is the number of pairs of people we can create where order doesn't matter, or number of birthday comparisons.

In a hash table, the mumber of people would be equal to the capacity of our table, for example, if we had a hash table with 23 slots and choosing two elements that could hash to the same index.


![image](https://user-images.githubusercontent.com/91037796/204158108-db5e66fc-bc83-432a-8cb2-8ef02a8244a8.png)



# Separate Chaining

![image](https://user-images.githubusercontent.com/91037796/204156689-e0456afc-acf2-4169-8a97-9fbd54997a2e.png)


# Open Addressing

Quadratic - Probing

![image](https://user-images.githubusercontent.com/91037796/204156785-6202cd9b-e6e5-455c-83fc-a50534af536c.png)
