# HashMap Implementation

This is the portfolio project for the Oregon State University course CS 261 - Data Structures, which is allowed to be posted to a public GitHub repo.  The project implements a HashMap data structure using two distinct methods to handle table collisions - Open Addressing, and Separate Chaining.



- **Open Addressing**
   - In this implementation, the data structure probes for an empty spot in the HashTable's underlying dynamic array if a collision occurs, until it finds an empty spot to insert the element in. 

- **Separate Chaining**
   - In this implementation, each dynamic array element is a linked list, and additional key/value pairs can be added to the front of the linked list at each array spot in the case that keys hash to the same array index. 

</br>

# HashMap Time Complexity

A hash map allows insertion and lookup of values in amortized constant time O(1), with a potential O(N) resizing cost.  Resizing the table is performed in order to keep the table load factor low, which reduces the chance of collisions occurring. 

The load factor is expressed as n (number of elements) / m (number of buckets).

```math
\lambda	= n / m
```

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

In a hash table, the number of participants in the birthday paradox would be equivalent to the key/value pairs to be inserted in the table, as this calculates the number of possible comparsions between two elements or pairings.  


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

Using the same mathematical approach found in the birthday paradox, if we have 2,450 keys hashed into a million buckets, even with perfectly uniform random distribution (from a good hash function), according to the birthday problem there is approximately a 95% chance at least two of those keys will be hashed to the same slot.

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

Alternate calculation:


```math
\prod _{n=1}^{2450}\frac{\left(1000000-n\right)}{1000000}
```

```python
def calculate_probability_no_collisions():
    
    result = 1    
    for i in range(1,2450):
        result *= (1000000 - i)/1000000
    print(result)
        
    
def calculate_probability_no_collisions_2():
    
    constant = .999999
    result =1    
    for _ in range(3000025):
        result *= constant
    print(result)
    
calculate_probability_no_collisions()    # 0.049663
calculate_probability_no_collisions_2()  # 0.049785
```

</br>

# Separate Chaining

Separate chaining uses a linked list at each index location of the underlying dynamic array.  If a collision occurs, the key/value pair is added to the linked list at that index.

This table resizes the underlying dynamic array to double its capacity if the load factor is equal to or greater than 1.


![image](https://user-images.githubusercontent.com/91037796/204156689-e0456afc-acf2-4169-8a97-9fbd54997a2e.png)

</br>

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

```python
    def put(self, key: str, value: object) -> None:
        """
        This method inserts a new key/value pair into the hash table, and increments the hash table's size.
        
        If the key already exists in the table, the value of the key is updated.
        
        The method also handles table resizing.  It calculates the table load of the hash table, using the table load method.  This is calculated as follows:
        
            Load Factor (lowercase lambda) = num elements (size) / num buckets (capacity) 
        
        If the table load is greater or equal to 1.0, the capacity of the hash table is doubled, and incremented if it is not a prime number after being doubled. 
        This helps ensure the hash table has fewer collisions and maintains an average time complexity of O(1) for its operations.
        
        This method uses separate chaining to resolve table collisions.  Each array index in the hash table's underlying dynamic array consists of a linked list.
        If an element already exists at an index, the new key/value pair is added to the linked list.
        """
        
        # CALCULATE TABLE LOAD AND DOUBLE THE CAPACITY OF THE HASH TABLE IF NEEDED
        table_load = self.table_load()
        
        if table_load >= 1.0:  
            curr_capacity = self._capacity
            new_capacity = curr_capacity * 2
            self.resize_table(new_capacity)

        
        # CALCULATE THE INDEX OF THE KEY TO BE INSERTED/UPDATED USING THE HASH FUNCTION AND HASH TABLE CAPACITY
        _hash = self._hash_function(key)
        index = _hash % self._capacity
        
        hash_map_bucket = self._buckets[index]
        
        # IF THE LINKED LIST AT THAT ARRAY LOCATION IS EMPTY, INSERT NODE CONTAINING THE KEY, VALUE PAIR AT THE FRONT OF THE LL
        if hash_map_bucket.length() == 0:        
            hash_map_bucket.insert(key, value)
            self._size += 1
        # ELSE IF THE LINKED LIST CONTAINS THAT KEY, UPDATE THE KEY'S VALUE, OR INSERT THE NEW KEY/VALUE AT THE FRONT OF THE LL IF NOT ALREADY IN THE TABLE
        else:
            existing_node_with_key = hash_map_bucket.contains(key)
            if existing_node_with_key:
                existing_node_with_key.value = value
            else:
                hash_map_bucket.insert(key, value)
                self._size += 1

```

</br>

# Open Addressing


Quadratic Probing is calculated using the following formula, where i = index, m is the capacity of the array, and j is a separate variable incremented by 1 each time the probing is unsuccesful. 

```math 
({i_{initial} + j^2 }) \bmod m
```

j is incremented by 1 each time the probe occurrs, until an empty spot is found in the dynamic array to insert the element.  The numerator of the function is divided by the capacity, to obtain the modulus, which is used as the index to insert/probe for an empty spot.  This is so that insertion/probing can wrap back around the array if needed.

This table resizes the underlying dynamic array to double its capacity if the load factor is equal to or greater than 0.5.



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

```python
    def put(self, key: str, value: object) -> None:
        """
        This method adds a new key/value pair as a hash entry into the hash table, and increments the hash table's size.
        
        Before adding a value, the table load of the (num elements/ capacity) is calculated.  If the table load is above or equal to 0.5, meaning that half
        the underlying dynamic array's values are filled, the table is resized to double the current capacity, to the nearest prime number.  This helps reduce
        collisions and ensures O(1) time complexity for most operations.
        
        The method first uses the hash function to calculate the insertion point of the new key/value pair.
        
        If the insertion point is a tombstone, it will update the tombstone if its key matches the key to be added, or if the key is not elsewhere in the table.
        
        If the insertion point matches the key, it will update the value.
        
        If the insertion point is a key/value not matching the key and not a tombstone, it will continue to increment the index using quadratic probing, until
        an empty spot in the hash table is reached, or the previous conditions of finding the existing key, tombstone with existing key, or tombstone where key
        is not elsewhere is met.                  
        """
        table_load = self.table_load()
        
        # RESIZE IF HALF OF DYNAMIC ARRAY OF HASH TABLE'S FREE SPACE IS 50 PERCENT OR LESS
        if table_load >= 0.5:  
            curr_capacity = self._capacity
            new_capacity = curr_capacity * 2
            self.resize_table(new_capacity)

        # CALCULATE INITIAL INDEX BASED ON HASH FUNCTION AND KEY
        _hash = self._hash_function(key)
        index = _hash % self._capacity                        
        
        j = 1
        quad_index = index
        while self._buckets[quad_index] is not None:
                        
            if self._buckets[quad_index].is_tombstone is True:
                # IF A TOMBSTONE EXISTS WITH CURRENT KEY, UPDATE IT TO REMOVE THE TOMBSTONE AND UPDATE VALUE AS WELL
                if self._buckets[quad_index].key == key:
                    self._buckets[quad_index].value = value
                    self._buckets[quad_index].is_tombstone = False
                    self._size +=1
                    return 
                # IF A TOMBSTONE EXISTS NOT EQUAL TO THE CURRENT KEY, AND THE KEY DOES NOT EXIST ELSEWHERE IN THE TABLE, REPLACE TOMBSTONE WITH KEY/VALUE
                elif self.contains_key(key) is False:                    
                    new_entry = HashEntry(key, value) 
                    self._buckets[quad_index] = new_entry
                    self._size += 1    
                    return                
            
            # IF NOT THE VALUE IS NOT A TOMBSTONE, BUT IS EQUAL TO THE CURRENT KEY, SIMPLY UPDATE THE VALUE AND RETURN
            elif self._buckets[quad_index].key == key:
                self._buckets[quad_index].value = value
                return
            
            quad_index = (index + j**2) % self._capacity   #QUADRATIC PROBING TO INCREMENT INSERTION INDEX IF NEEDED
            j += 1   
            
        
        # IF THE FUNCTION REACHES HERE AND HAS NOT RETURNED, WE HAVE REACHED A NONE VALUE TO INSERT THE NEW KEY/VALUE PAIR INTO
        new_entry = HashEntry(key, value) 
        self._buckets[quad_index] = new_entry
        self._size += 1

      
```
