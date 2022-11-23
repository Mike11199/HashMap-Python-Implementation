# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """
        table_load = self.table_load()
        
        if table_load >= 0.5:  
            curr_capacity = self._capacity
            new_capacity = curr_capacity * 2
            self.resize_table(new_capacity)

        
        _hash = self._hash_function(key)
        index = _hash % self._capacity                        
        
        j = 1
        quad_index = index
        while self._buckets[quad_index] is not None:
                        
            if self._buckets[quad_index].is_tombstone is True:
                if self._buckets[quad_index].key == key:
                    self._buckets[quad_index].value = value
                    self._buckets[quad_index].is_tombstone = False
                    self._size +=1
                    return 
                elif self.contains_key(key) is False:
                    new_entry = HashEntry(key, value) 
                    self._buckets[quad_index] = new_entry
                    self._size += 1    
                    return                
    
            elif self._buckets[quad_index].key == key:
                self._buckets[quad_index].value = value
                return
            
            quad_index = (index + j**2) % self._capacity
            j += 1   
            

        # if while loop terminates we have reached an array index with value of None
        new_entry = HashEntry(key, value) 
        self._buckets[quad_index] = new_entry
        self._size += 1

      

    def table_load(self) -> float:
        """
        This method returns the table load factor which is defined as the below function:
        
                Load Factor (lowercase lambda) = num elements (size) / num buckets (capacity) 
                
        The put method of the hash table will call the resize function based on the load factor's value.
        """        
        load = self._size / self._capacity
        return load

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets (dynamic array indexes with the value of None) in the hash table.
        
        A tombstone value is NOT considered an empty bucket.
        """
        num_of_empty_buckets = 0
        
        for i in range(self._capacity):
            if self._buckets[i] is None: 
                num_of_empty_buckets += 1 
            
        return num_of_empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """
        This method resizes the hash table.  It will only resize a hash table to a value equal or larger to the number of elements present in the 
        internal dynamic array.  It will also ensure the new capacity is a prime number.
        
        The method creates a new hash table object, and re-hashes each element into the original hash table in its new position, based on the new capacity.
        
        It uses the put method, which handles resizing if the table load drops to or below 0.5.                
        """
        
        # DO NOTHING IF NEW CAPACITY IS SMALLER THAN NUMBER OF ELEMENTS CURRENTLY IN THE HASH TABLE ( AS ELEMENTS WOULD BE LOST )
        if new_capacity < self._size:
            return

        # IF NEW CAPACITY IS NOT PRIME, INCREMENT UNTIL IT IS A PRIME NUMBER            
        if not self._is_prime(new_capacity):
            new_capacity =  self._next_prime(new_capacity)
            
        # CREATE A NEW HASH MAP WITH THE NEW CAPACITY GIVEN    
        new_hash_map = HashMap(new_capacity, self._hash_function)
        
        # ITERATE THROUGH THE OLD HASH MAP.  IF THE VALUE IS NOT NONE, ADD IT TO THE NEW HASH MAP USING THE NEW HASH MAP'S PUT FUNCTION
        for i in range(self._capacity):
            if self._buckets[i]:
                new_key = self._buckets[i].key
                new_value = self._buckets[i].value
                new_hash_map.put(new_key, new_value)  # PUT FUNCTION WILL HANDLE ADDITIONAL RESIZING BASED ON TABLE LOAD IF NEEDED


        # SWAP UNDERLYING DYNAMIC ARRAY AND CAPACITY FROM NEW HASH TABLE TO CURRENT HASH TABLE.  SIZE REMAINS THE SAME
        self._buckets = new_hash_map._buckets
        self._capacity = new_hash_map._capacity


    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        if self._size == 0:
            return
        
        _hash = self._hash_function(key)
        index = _hash % self._capacity        
        hash_map_entry = self._buckets[index]
        
        if hash_map_entry is None:    
            return 
        else:
            j = 1
            quadratic_index = index

            while self._buckets[quadratic_index] is not None:
                
                if self._buckets[quadratic_index].key == key:
                    return self._buckets[quadratic_index].value
                
                quadratic_index = (index + j**2) % self._capacity
                j += 1                
                            
        return 

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        if self._size == 0:
            return False
        
        _hash = self._hash_function(key)
        index = _hash % self._capacity        
        hash_map_entry = self._buckets[index]
        
        if hash_map_entry is None:    
            return False
        else:
            j = 1
            quadratic_index = index

            while self._buckets[quadratic_index] is not None:
                
                if self._buckets[quadratic_index].key == key:
                    return True
                
                quadratic_index = (index + j**2) % self._capacity
                j += 1                
                            
        return False

    def remove(self, key: str) -> None:
        """
        This method removes a given key and its value from the hash map.  It uses quadratic probing (initial index + j^2), until it reaches an index with None, in
        case the value to be removed was inserted after encountering a table collision. 
        
        In the case of this hash table, when removing a key/value, the index where the key/value was located at is NOT changed to None.
        
        Instead, the is_tombstone method of the hash entry class that occupies 
        """
        
        _hash = self._hash_function(key)
        index = _hash % self._capacity        
        hash_map_entry = self._buckets[index]
        
        if hash_map_entry is None:    
            return 
        else:
            j = 1
            quadratic_index = index

            while self._buckets[quadratic_index] is not None:
                
                if self._buckets[quadratic_index].key == key and self._buckets[quadratic_index].is_tombstone is False:
                    self._buckets[quadratic_index].is_tombstone = True
                    self._size -= 1
                    return
                
                quadratic_index = (index + j**2) % self._capacity
                j += 1                
                            
    def clear(self) -> None:
        """
        This method clears all values in the underlying dynamic array of the hash table.  It iterates through the dynamic array and sets each
        index to None.  Then it resets the size variable of the hash table to zero to reflect that it contains no elements.
        
        Capacity remains unchanged.
        """
        for i in range(self._capacity):
            self._buckets[i] = None
        
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a new dynamic array, where each index is a tuple of the key/value pair stored in the hash map.
        
        The tuples are returned from smallest to greatest index from where they are located in the hash table's underlying dynamic array, 
        from their insertion point based on the hash function and quadratic open addressing scheme, and not in any particular order.
        """
        da_tuples = DynamicArray()
        
        for i in range(self._capacity):
            hash_entry = self._buckets[i]
            if hash_entry is not None and hash_entry.is_tombstone is False:    
                da_tuples.append((hash_entry.key, hash_entry.value))

        return da_tuples

    def __iter__(self):
        """
        This returns the iterator.  In the iterator, we create a variable, index to track our position in the hash map class.
        """
        self._index = 0  # reference module 3 example from Canvas
        return self

    def __next__(self):
        """
        This advances the iterator through each element of the hash map that is NOT empty, empty being "None".
        """
        
        if self._index == self._capacity:
            raise StopIteration
        
        hash_val = self._buckets[self._index]        
         
        while hash_val is None:
            self._index += 1
            if self._index == self._capacity:
                raise StopIteration
            hash_val = self._buckets[self._index]             
        
        self._index += 1
        return hash_val
        

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    
    
    
    print("\nPDF - failed resize test case - gradescope #1")
    print("-------------------")
    m = HashMap(163, hash_function_2)
    gradescope_array = [[0,38,1596],[1,259,10878],[2,77,3234],[3,467,19614],[4,155,6510],[5,519,21798],[6,298,12516],[7,597,25074],[8,389,16338],[9,493,20706],
                        [10,207,8694],[11,363,15246],[12,649,27258],[13,675,28350],[14,779,32718],[15,545,22890],[17,558,23436],[18,25,1050],[19,714,29988],
                        [20,571,23982],[21,805,33810],[22,662,27804],[23,909,38178],[24,688,28896],[26,740,31080],[28,636,26712],[29,792,33264],[30,623,26166],
                        [31,584,24528],[32,818,34356],[33,870,36540],[35,766,32172],[37,753,31626],[39,844,35448],[41,935,39270],[42,896,37632],[43,727,30534],
                        [44,883,37086],[45,922,38724],[46,974,40908],[50,857,35994],[52,948,39816],[57,987,41454],[60,831,34902],[67,961,40362],[131,220,9240],
                        [133,311,13062],[134,610,25620],[135,103,4326],[136,402,16884],[138,350,14700],[139,701,29442],[140,142,5964],[141,441,18522],
                        [142,233,9786],[143,532,22344],[144,324,13608],[145,480,20160],[146,415,17430], [147,272,11424],[148,506,21252],[149,181,7602],[150,116,4872],[151,454,19068],
                        [152,51,2142],[153,246,10332],[154,90,3780],[155,337,14154],[156,194,8148],[157,129,5418],[158,64,2688],[159,285,11970],[160,376,15792],
                        [161,428,17976],[162,168,7056]]
    m._size = 75

    for array_elem in gradescope_array:
        hash_entry = HashEntry(str(array_elem[1]),array_elem[2])
        m._buckets[array_elem[0]] = hash_entry
        
    m.resize_table(111)

       
    
    
    
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)