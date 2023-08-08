class HashTable:
    def __init__(self):
        self.size = 40  # approximate number of packages
        self.table = [[] for _ in range(self.size)]  # initialize the table with empty lists

    def insert(self, key, value):
        # Compute the hash (index) of the key
        hash_index = self.hash(key)
        # Add the (key, value) pair to the list at the hash_index
        self.table[hash_index].append((key, value))

    def lookup(self, key):
        # Compute the hash (index) of the key
        hash_index = self.hash(key)
        # Look for the key in the list at the hash_index
        for pair in self.table[hash_index]:
            if pair[0] == key:
                return pair[1]
        # If the key is not found, return None
        return None

    def hash(self, key):
        # Compute a simple hash of the key
        return key % self.size

