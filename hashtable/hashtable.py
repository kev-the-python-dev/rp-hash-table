'''Goals:
1. Resolve has collisions
2. Retain insertion order
3. Dynamically resize hash table
4. Calculate load factor
'''

BLANK = object() # To prevent allowing None values to be used for hashTable object upon creation

class hashTable:
    def __init__(self, max_capacity):
        self.values = max_capacity * [BLANK] # Quickesy way to populate list with given values

    def __len__(self):
        return len(self.values)

    def __setitem__(self, key, value):
        # Keep max_capacity fixed
        self.values[self._index(key)] = value

    def __getitem__(self, key):
        value = self.values[self._index(key)]
        if value is BLANK: # We use 'is' keyword t compare identity and not values 
            raise KeyError(key)
        return value

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key):
        # Taking advantage of mutator method
        self[key] = BLANK

    def _index(self, key):
        return hash(key) % len(self)