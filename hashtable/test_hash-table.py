'''Test-driven Development Goals:
1. Resolve has collisions
2. Retain insertion order
3. Dynamically resize hash table
4. Calculate load factor
'''

import pytest
from pytest_unordered import unordered

from hashtable import hashTable

def test_should_pass():
    assert hashTable(max_capacity=100) is not None

def test_max_capacity_report():
    assert len(hashTable(max_capacity=100)) == 100

def test_create_empty_value_slots():
    assert hashTable(max_capacity=3)._pair == [None, None, None] # White-box testing

def test_insert_keys_and_value_pairs():
    # Given
    hash_table = hashTable(max_capacity=100)

    # When
    hash_table['Hola'] = 'Hello'
    hash_table[98.6] = 37
    hash_table[False] = True

    # Then
    assert ('Hola', 'Hello') in hash_table.pair
    assert (98.6, 37) in hash_table.pair
    assert (False, True) in hash_table.pair

    # Additional insertion for additional test
    assert len(hash_table) == 100

def test_table_should_not_contain_none_value_when_created():
    assert None not in hashTable(max_capacity=100).values

def test_insert_none_value():
    hash_table = hashTable(max_capacity=100)
    hash_table['key'] = None
    assert ('key', None) in hash_table.pair
@pytest.fixture # Avoid duplicating same hashTable setup
def hash_table():
    # Given
    sample_data = hashTable(max_capacity=100)

    # When
    sample_data['Hola'] = 'Hello'
    sample_data[98.6] = 37
    sample_data[False] = True
    return sample_data

def test_should_find_value_in_key(hash_table):
    assert hash_table['Hola'] == 'Hello'
    assert hash_table[98.6] == 37
    assert hash_table[False] is True

def test_should_raise_error_on_missing_key():
    hash_table = hashTable(max_capacity=100)
    
    with pytest.raises(KeyError) as exception_information: # Don't forget to add conditional to accessor method --> located in hashTable.getitem()
        hash_table['Missing_Key']
    assert exception_information.value.args[0] == 'Missing_Key'

def test_should_find_key(hash_table):
    assert 'Hola' in hash_table

def test_should_not_find_key(hash_table):
    assert 'Missing_Key' not in hash_table

def test_should_get_value(hash_table):
    assert hash_table.get('Hola') == 'Hello'

def test_should_get_none_when_key_missing(hash_table):
    assert hash_table.get('Missing_Key') is None

def test_should_delete_key_value_pair(hash_table):
    assert ('Hola', 'Hello') in hash_table.pair

    del hash_table['Hola']

    assert 'Hello', 'Hola' not in hash_table.pair

    # Ensure Hash deletion does not shrink overall hash table
    assert len(hash_table) == 100

def test_should_return_pairs(hash_table):
    assert('Hola', 'Hello') in hash_table.pair
    assert(98.6, 37) in hash_table.pair
    assert (False, True) in hash_table.pair

def test_should_return_copy_of_pairs(hash_table):
    assert hash_table.pair is not hash_table.pair

def test_should_not_include_blank_pairs(hash_table):
    assert None not in hash_table.pair

def test_should_return_duplicate_values():
    hash_table = hashTable(max_capacity=100)
    hash_table['Alice'] = 24
    hash_table['Bob'] = 42
    hash_table['Joe'] = 42
    assert [24, 42, 42] == sorted(hash_table.values)

# Won't take order into account when comparing 2 (or more) lists
def test_should_get_unordered_values(hash_table):
    assert unordered(hash_table.values) == ['Hello', 37, True]

def test_should_get_values_of_empty_hash_table():
    assert hashTable(max_capacity=100).values == []

def test_should_return_copy_of_values(hash_table):
    assert hash_table.values is not hash_table.values

# Hash table's keys must be unique
def test_should_get_keys(hash_table):
    assert hash_table.keys == {'Hola', 98.6, False}

def test_should_get_keys_of_empty_hash_table():
    assert hashTable(max_capacity=100).keys == set() # No empty set literal in Python

def test_should_return_copy_of_keys(hash_table):
    assert hash_table.keys is not hash_table.keys

def test_should_return_kv_pairs(hash_table):
    assert hash_table.pair == {
        ('Hola', 'Hello'),
        (98.6, 37),
        (False, True)
    }

def test_should_get_pairs_from_empty_hash_table():
    assert hashTable(max_capacity=100).pair == set()

def test_should_convert_to_dict(hash_table):
    dictionary = dict(hash_table.pair)
    assert set(dictionary.keys()) == hash_table.keys
    assert set(dictionary.items()) == hash_table.pair
    assert list(dictionary.values()) == unordered(hash_table.values)