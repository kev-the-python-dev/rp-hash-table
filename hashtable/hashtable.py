'''Goals:
1. Resolve has collisions
2. Retain insertion order
3. Dynamically resize hash table
4. Calculate load factor
'''
from multiprocessing.sharedctypes import Value
from typing import NamedTuple, Any

class Pair(NamedTuple):
    key: Any
    value: Any
#None = object() # To prevent allowing None pair to be used for hashTable object upon creation

class hashTable:

    # Taking advantage of short-circuiting
    @classmethod
    # If capacity isn't specified, we fall back to default behavior (multiply dictionary's len by 10)
    def from_dict(cls, dictionary, capacity=None):
        hash_table = cls(capacity or len(dictionary) * 10) # cls required to taek class dictionary as parameter
        for key, val in dictionary.items():
            hash_table[key] = val
        return hash_table

    def __init__(self, max_capacity):
        if max_capacity <= 0:
            raise ValueError('Max capacity must be a positive number')
        self._pair = max_capacity * [None] # Quickesy way to populate list with given pair

    def __len__(self):
        return len(self.pair)

    def __setitem__(self, key, pair):
        # Keep max_capacity fixed
        self._pair[self._index(key)] = Pair(key, pair)

    def __getitem__(self, key):
        pairs = self._pair[self._index(key)]
        if pairs is None: # We use 'is' keyword t compare identity and not pair 
            raise KeyError(key)
        return pairs.value

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __delitem__(self, key):
        # Taking advantage of mutator method
        if key in self:
            self._pair[self._index(key)] = None
        else:
            raise KeyError(key)

    def __str__(self):
        pairs = []
        for key, val in self.pair:
            pairs.append(f'{key!r}: {val!r}') #!r required for calling repr()
        return '{' + ', '.join(pairs) + '}'

    # Required to iterate through class instance (must return iterator object)
    def __iter__(self):
        yield from self.keys # Yeild is needed to define our in-place iterator object

    def __repr__(self):
        cls = self.__class__.__name__ # Avoiding hard-coded name incase class needs to be renamed
        return f'{cls}.from_dict({str(self)})'
    
    # So hash table is equal to itself, its copy, or another instance with same k/v pairs
    def __eq__(self, other_table):
        if self is other_table:
            return True
        if type(self) is not type(other_table):
            return False
        return set(self.pair) == set(other_table.pair)
    
    # Don't remove otherwise copies may just be references to same object vs. their own object
    @property
    def values(self):
        return [val_pair.value for val_pair in self.pair]
    
    @property
    def pair(self):
        return {val_pair for val_pair in self._pair if val_pair} # creates separate list (needed to create different object from copy)
    
    @property
    def keys(self):
        return {val_pair.key for val_pair in self.pair} # Ensure no keys are same name
    
    @property
    def capacity(self):
        return len(self._pair)

    def _index(self, key):
        return hash(key) % self.capacity

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def copy(self):
        return hashTable.from_dict(dict(self.pair), self.capacity)
    