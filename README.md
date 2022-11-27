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
</br>

# Table Collisions - The Birthday Paradox

Reference https://betterexplained.com/articles/understanding-the-birthday-paradox/

A simplified way to view the chance of a hash table collision is by using the Birthday Paradox.  This is a non-intuitive problem which states that in a room of 23 people, there is about a 50% chance two share the same birthday.

To explain this concept, we can take the possible two-person combinations of these 23 people, which is equal to 253. This is the number of pairs of people we can create where order doesn't matter, or number of potential birthday comparisons.

In a hash table, the number of people in the birthday paradox would be equivalent to the key/value pairs to be inserted in the table, as this calculates the number of possible comparsions between two elements or pairings.  


![image](https://user-images.githubusercontent.com/91037796/204158108-db5e66fc-bc83-432a-8cb2-8ef02a8244a8.png)


In the birthday paradox there is a 99.7% chance two pairs will not share the same birthday.

```math
{1 - \frac{1}{365} = \frac{364}{365} = .997260}
```

Taking the exponent of that chance, or multiplied by the number of 253 possible pairs of comparisons, there is a roughly 49.95% chance none of them will have the same birthday, or 1 - 49.95% = 50.05% chance at least one person will share a birthday.


```math
{1 - \frac{1}{365} = \frac{364}{365} = .997260}
```


```math
\displaystyle{\left(\frac{364}{365}\right)^{253} = .4995}
```

</br> 

# Table Collisions - HashMap Example

Using similar math following the birthday problem, if we have 2,450 keys hashed into a million buckets, even with perfectly uniform random distribution (from a good hash function), according to the birthday problem there is approximately a 95% chance at least two of those keys will be hashed to the same slot.

We use the combination formula from 2,450 keys choose two to calculate that there are 3,000,025 possible pairs or comparisons.


```math
C(n,k) = \binom{n}{k} = \frac{2,450!}{2!(2,448)! } = 3,000,025 
```

There is a 999,999 in 1,000,000, or 99.9999% chance of not being in a collision for a single pair.  This is the chance of NOT inserting a key/value pair into the same bucket. Assuming a hash function with a uniform distribution.  Then the probability would be (n-2)/n for the next pair, but the math below will not consider that to simplify the example.

The chance of there NOT being a collision for all possible pairings of 2,450 keys inserted to the hash table, is the probability of not having a single collision raised to the exponent of the number of pairs:

```math
{0.999999}^{3,000,025} = 4.97% 
```
If there is a 4.97% of there not being a single collision in a hash table with 1 million buckets and 2,450 keys, then there is a ( 1 - 4.97% ), or 95% chance that at least two keys in this hash table will be hashed to the same slot.  In other words, a 95% chance this table would have a collision.

This is significant as one would think a collision would be more unlikely in a situation where so little of this hash table is used (2,450 elements with 1,000,000 buckets).

As such, separate chaining and open addressing is used to handle these potential collisions.


</br>

# Separate Chaining

Separate chaining uses a linked list at each index location of the underlying dynamic array.  If a collision occurs, the key/value pair is added to the linked list at that index.

This table resizes the underlying dynamic array to double its capacity if the load factor is equal to or greater than 1.

This can 

![image](https://user-images.githubusercontent.com/91037796/204156689-e0456afc-acf2-4169-8a97-9fbd54997a2e.png)


```python
class HashMap:
   def __init__(self, capacity: int, function) -> None:

   def __str__(self) -> str:

   def _next_prime(self, capacity: int) -> int:

   @staticmethod
   def _is_prime(capacity: int) -> bool:

   def get_size(self) -> int:

   def get_capacity(self) -> int:

   def put(self, key: str, value: object) -> None:

   def empty_buckets(self) -> int:

   def table_load(self) -> float:
   
   def clear(self) -> None:
   
   def resize_table(self, new_capacity: int) -> None:
   
   def get(self, key: str):
   
   def contains_key(self, key: str) -> bool:
   
   def remove(self, key: str) -> None:
   
   def get_keys_and_values(self) -> DynamicArray:
   
   def find_mode(da: DynamicArray):

```



</br>

# Open Addressing


Quadratic Probing is calculated using the following formula, where i = index.  j is incremented by 1 each time the probe occurrs, until an empty spot is found in the dynamic array to insert the element.

This table resizes the underlying dynamic array to double its capacity if the load factor is equal to or greater than 0.5.

```math 
{i_{initial} + j^2 } \bmod m
```

![image](https://user-images.githubusercontent.com/91037796/204156785-6202cd9b-e6e5-455c-83fc-a50534af536c.png)


If elements are removed, removed elements are converted to tombstone values, so that lookups of existing elements do not end early.  This means a flag of the element is set to True to indicate the key/value pair is a tombstone, as oppossed to setting it back to the default value of None.

</br>

```python
class HashMap:
    def __init__(self, capacity: int, function) -> None:

    def __str__(self) -> str:

    def _next_prime(self, capacity: int) -> int:

    @staticmethod
    def _is_prime(capacity: int) -> bool:
   
    def put(self, key: str, value: object) -> None:
    
    def empty_buckets(self) -> int:

    def resize_table(self, new_capacity: int) -> None:
      
    def get(self, key: str) -> object:
      
    def contains_key(self, key: str) -> bool:

    def remove(self, key: str) -> None:
 
    def clear(self) -> None:

    def get_keys_and_values(self) -> DynamicArray:

    def __iter__(self):

    def __next__(self):
```
