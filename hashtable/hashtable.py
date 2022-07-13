'''Goals:
1. Resolve has collisions
2. Retain insertion order
3. Dynamically resize hash table
4. Calculate load factor
'''
from typing import NamedTuple, Any

class Pair(NamedTuple):
    key: Any
    value: Any
#None = object() # To prevent allowing None pair to be used for hashTable object upon creation

class hashTable:
    def __init__(self, max_capacity):
        self._pair = max_capacity * [None] # Quickesy way to populate list with given pair

    def __len__(self):
        return len(self._pair)

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

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key):
        # Taking advantage of mutator method
        if key in self:
            self._pair[self._index(key)] = None
        else:
            raise KeyError(key)
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
    
    def _index(self, key):
        return hash(key) % len(self)

    