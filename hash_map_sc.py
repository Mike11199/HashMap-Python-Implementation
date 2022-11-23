# Name:             Michael Iwanek
# OSU Email:        iwanekm@oregonstate.edu
# Course:           CS261 - Data Structures
# Assignment:       Assignment #6 - HashMap Implementation - Part 1 - Separate Chaining
# Due Date:         12/02/22 @ 11:59PM
# Description:      Write methods to implement a HashMap, using separate chaining (linked lists at each array index) to resolve table collisions. 


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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


    def empty_buckets(self) -> int:
        """
        This method counts each array index in the hash table's underlying dynamic array which contains an empty linked list, and returns that count as an 
        integer.  
        """
        
        num_of_empty_buckets = 0
        
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:     
                num_of_empty_buckets += 1 
            
        return num_of_empty_buckets

    def table_load(self) -> float:
        """
        This method returns the load factor of the hash table as a float value.  This is needed to decide whether the table should be resized to reduce the 
        likelihood of collisions.
        
        Load Factor (lowercase lambda) = num elements (size) / num buckets (capacity) 
        """        
        load = self._size / self._capacity
        return load

    def clear(self) -> None:
        """
        This method clears the contents of the hash map's underlying dynamic array.  It iterates through the array and assigns an empty linked list to each
        index.  
        
        The capacity of the hash table remains unchanged.  The size of the hash table however is updated to ZERO to reflect that it no longer contains any
        nodes with key/value pairs.
        """
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        This method updates the capacity of the hash table, and in doing so, updates the underlying dynamic array and the linked list at each array index's 
        location.
        
        It ensures the capacity is a prime number, and not less than 1.
        
        A new dynamic array is created, and each element of the original array is traversed.  Each node in the linked list at each array index is also recomputed.
        This is because if the array capacity is increased, element that may have previously had a collision, and were added to a linked list, may no longer need
        to be linked at the same index, as there will be more spots available in the array.  As such, all nodes are rehashed using the hash function and new 
        capacity to determine the new index to insert into the hash table's underlying dynamic array.
        """
        
        # IF THE NEW CAPACITY IS LESS THAN 1, RETURN AND DO NOTHING
        if new_capacity < 1:
            return
    
        # IF THE NEW CAPACITY IS NOT A PRIME NUMBER, INCREMENT THE NUMBER UNTIL IT IS
        curr_capacity = self._capacity
        if not self._is_prime(new_capacity):
            new_capacity =  self._next_prime(new_capacity)
            
        new_table_load = self._size / new_capacity
        
        # IF THE TABLE LOAD IS NOT 1.0, DOUBLE THE CAPACITY
        while new_table_load > 1.0:
            new_capacity =  new_capacity * 2
            if not self._is_prime(new_capacity):                
                 new_capacity =  self._next_prime(new_capacity)
            new_table_load = self._size / new_capacity
        
        # REASSIGN NEW CAPACITY TO THE HASH TABLE'S CAPACITY VARIABLE, AND CREATE A NEW DYNAMIC ARRAY    
        self._capacity = new_capacity
        resized_buckets = DynamicArray()
        
        
        # ADD EMPTY LINKED LISTS AT EACH INDEX IN THE NEW DYNAMIC ARRAY CREATED
        for _ in range(new_capacity):
            resized_buckets.append(LinkedList())


        # RECOMPUTE THE HASH FOR EACH NON-EMPTY ELEMENT OF THE ORIGINAL ARRAY, TO ADD VALUES IN THE NEW DYNAMIC ARRAY CREATED
        for i in range(curr_capacity):
            if self._buckets[i].length() != 0:     
                
                # GET HEAD AND ITS KEY FROM LL FROM ORIGINAL HASH TABLE                
                for node in self._buckets[i]:
                    head = node
                    head_key = head.key
                    head_value = head.value

                    # REHASH KEY FOR RESIZED HASH TABLE
                    _hash = self._hash_function(head_key)
                    index = _hash % self._capacity
                
                    hash_map_bucket = resized_buckets[index]
                    hash_map_bucket.insert(head_key, head_value)   
          
        # AT END OF THE FUNCTION, REASSIGN THE HASH TABLE'S DYNAMIC ARRAY TO THE NEW ARRAY CREATED BY THIS FUNCTION                
        self._buckets = resized_buckets


    def get(self, key: str):
        """
        This method looks up a node using its key, and returns the value of that node if it is found.  It returns NONE if the key is not present in the hash 
        table.
        
        The method first calculates the position in the hash table's underlying dynamic array that the key should be at.  It then iterates through the linked
        list at each array index location until the key is found, or it has reached the end of the linked list.
        
        Time Complexity: O(1)
        """
        _hash = self._hash_function(key)
        index = _hash % self._capacity        
        hash_map_bucket = self._buckets[index]
        
        if hash_map_bucket.length() != 0:
            for node in hash_map_bucket:
                if node.key == key:
                    return node.value
        
        return None
        

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if a key is located in the hash map, or returns False if the key is not present (or the hash table is empty).
        
        The method first calculates the position in the hash table's underlying dynamic array that the key should be at.  It then iterates through the linked
        list at each array index location until the key is found, or it has reached the end of the linked list.
        
        Time Complexity: O(1)
        """
        if self._size == 0:
            return False
        
        _hash = self._hash_function(key)
        index = _hash % self._capacity        
        hash_map_bucket = self._buckets[index]
        
        if hash_map_bucket.length() != 0:
            for node in hash_map_bucket:
                if node.key == key:
                    return True
        
        return False

    def remove(self, key: str) -> None:
        """
        This method returns removes a node from linked list in the hash table's underlying dynamic array, if the key is present in the hash map.  If the key
        is not found, it does nothing.
        
        The method first calculates the position in the hash table's underlying dynamic array that the key should be at.  It then iterates through the linked
        list at each array index location until the key is found, or it has reached the end of the linked list.
        
        The method uses the .remove method of the linked list class to efficiently remove the node from the linked list.
        
        Time Complexity: O(1)
        """
        _hash = self._hash_function(key)
        index = _hash % self._capacity        
        hash_map_bucket = self._buckets[index]
        
        if hash_map_bucket.length() != 0:
            if hash_map_bucket.remove(key):
                self._size -= 1
            
                  

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method iterates through the hash table, and returns a dynamic array of tuples containing the key/value of each node in the hash table's linked
        lists.
        
        It only adds a tuple if the linked list is not empty, and has nodes at that location.
        """
        
        da_tuples = DynamicArray()
        
        for i in range(self._capacity):
            hash_map_bucket = self._buckets[i]
            if hash_map_bucket.length() != 0:    
                    for node in hash_map_bucket:
                        da_tuples.append((node.key, node.value))

        return da_tuples


def find_mode(da: DynamicArray): # -> tuple(DynamicArray, int):
    """
    This method is a function outside the hash table's class.  
    
    It receives a dynamic array, and returns a tuple.  The tuple consists of a list of the most frequently occurring items in the dynamic array, as well as the 
    integer representing how often those values ocurred.
    
    The method first creates a new hash table object from the hash table class.  It then iterates through the dynamic array given to the function, and counts each
    occurrence of the element. The highest count (mode) is also tracked.
    
    The method .get_keys_and_values of the hash table is called to return a dynamic array with the computed keys/counts. O(N)
    
    This new dynamic array is traversed, O(N), and if the count matches the mode, the tuple key is added to a new dynamic array.
    
    Finally, the tuple is returned which consists of this dynamic array as the first element, and the integer representing the mode as the second element.
    
    Time Complexity O(3N) or O(N)
    """

    # CREATE HASH MAP
    map = HashMap()
    highest_count = 0
    
    # IMPLEMENT THROUGH THE DYNAMIC ARRAY, AND COUNT EACH VALUE
    for i in range(da.length()):
        
        value_of_key = map.get(da[i])
        
        # IF VALUE IS ALREADY IN THE HASH TABLE, INCREMENT THE COUNTER. SET HIGHEST COUNT TO HIGHER OF ITSELF AND THE NEW COUNT VALUE
        if value_of_key:
            map.put(da[i], value_of_key +1)
            if value_of_key + 1 > highest_count:
                highest_count = value_of_key +1
                
        # IF VALUE IS NOT IN THE HASH TABLE, ADD A COUNT OF 1, AND SET HIGHEST COUNT TO 1 IF IT IS CURRENTLY LESS THAN 1. 
        else:
            map.put(da[i], 1)
            if 1 > highest_count:
                highest_count = 1
        
    # GET DYNAMIC ARRAY OF KEYS AND VALUES USING HASH TABLE METHOD        
    item_counter = map.get_keys_and_values()
    
    result_da = DynamicArray()
    
    # TRAVERSE THE ITEM COUNTER DYNAMIC ARRAY, AND IF THE TUPLE'S COUNT IS EQUAL TO THE MODE, ADD THAT ITEM TO THE RETURN DYNAMIC ARRAY
    for i in range(item_counter.length()):
        if item_counter[i][1] == highest_count:
            result_da.append(item_counter[i][0])
    
    # RETURN TUPLE OF THE DYNAMIC ARRAY CONTAINING ITEMS WITH THE HIGHEST COUNT, AND AN INTEGER REPRESENTING THE MODE
    return(result_da, highest_count)
           


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")