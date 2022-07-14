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
    assert len(hashTable(max_capacity=100)) == 0

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
    assert ('Hola', 'Hello') in hash_table._pair
    assert (98.6, 37) in hash_table._pair
    assert (False, True) in hash_table._pair

    # Additional insertion for additional test
    assert len(hash_table) == 3

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
    assert len(hash_table) == 2

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

# Hash table length
def test_should_report_length_of_empty_hash_table():
    assert len(hashTable(max_capacity=100)) == 0

def test_should_not_create_hashtable_with_zero_capacity():
    with pytest.raises(ValueError):
        hashTable(max_capacity=0)

def test_should_not_create_hash_table_with_negative_capacity():
    with pytest.raises(ValueError):
        hashTable(max_capacity=-100)

def test_should_report_length(hash_table):
    assert len(hash_table) == 3

def test_should_report_capacity_of_empty_hash_table():
    assert hashTable(max_capacity=100).capacity == 100

def test_should_report_capcity(hash_table):
    assert hash_table.capacity == 100

# Making Hash Table Iterable
def test_should_iterate_over_keys(hash_table):
    for key in hash_table.keys:
        assert key in ('Hola', 98.6, False)

def test_should_iterate_over_values(hash_table):
    for value in hash_table.values:
        assert value in ('Hello', 37, True)

def test_should_iterate_over_pairs(hash_table):
    for key, val in hash_table.pair:
        assert key in hash_table.keys
        assert val in hash_table.values

def test_should_iterate_over_hashTable_instance(hash_table):
    for key in hash_table:
        assert key in ('Hola', 98.6, False)

# Hash Table Text Representation
def test_should_use_literal_for_str(hash_table):
    assert str(hash_table) in {
        '{\'Hola\': \'Hello\', 98.6: 37, False: True}',
        '{\'Hola\': \'Hello\', False: True, 98.6: 37}',
        '{98.6: 37, \'Hola\': \'Hello\', False: True}',
        '{98.6: 37, False: True, \'Hola\': \'Hello\'}',
        '{False: True, \'Hola\': \'Hello\', 98.6: 37}',
        '{False: True, 98.6: 37, \'Hola\': \'Hello\'}',
    }

def test_should_create_hash_table_from_dict():
    dictionary = {'Hola': 'Hello', 98.6: 37, False: True}

    hash_table = hashTable.from_dict(dictionary)

    assert hash_table.capacity == len(dictionary) * 10
    assert hash_table.keys == set(dictionary.keys())
    assert hash_table.pair == set(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())

def test_should_have_canonical_string_representation(hash_table):
    assert repr(hash_table) in {
        'hashTable.from_dict({\'Hola\': \'Hello\', 98.6: 37, False: True})',
        'hashTable.from_dict({\'Hola\': \'Hello\', False: True, 98.6: 37})',
        'hashTable.from_dict({98.6: 37, \'Hola\': \'Hello\', False: True})',
        'hashTable.from_dict({98.6: 37, False: True, \'Hola\': \'Hello\'})',
        'hashTable.from_dict({False: True, \'Hola\': \'Hello\', 98.6: 37})',
        'hashTable.from_dict({False: True, 98.6: 37, \'Hola\': \'Hello\'})',
    }

# Hash Table Equality
def test_should_compare_equality_to_itself(hash_table):
    assert hash_table == hash_table

def test_should_compare_equality_to_hash_table_copy(hash_table):
    assert hash_table is not hash_table.copy()
    assert hash_table == hash_table.copy()

def test_should_compare_equality_with_different_key_value_order(hash_table):
    hash_table_1 = hashTable.from_dict({'a': 1, 'b': 2, 'c': 3})
    hash_table_2 = hashTable.from_dict({'b': 2, 'a': 1, 'c': 3})
    assert hash_table_1 == hash_table_2

def test_should_compare_unequal_tables(hash_table):
    other_table = hashTable.from_dict({'different': 'value'})
    assert hash_table != other_table

def test_should_compare_unequal_with_another_data_type(hash_table):
    assert hash_table != 100
    
def test_should_copy_key_val_pairs_and_capacity(hash_table):
    copy = hash_table.copy()
    assert copy is not hash_table
    assert set(hash_table.keys) == set(copy.keys)
    assert unordered(hash_table.values) == copy.values
    assert set(hash_table.pair) == set(copy.pair)
    assert hash_table.capacity == copy.capacity

def test_should_compare_equality_of_tables_with_different_capacity():
    data = {'a': 1, 'b': 2, 'c': 3}
    hash_table_1 = hashTable.from_dict(data, capacity=42)
    hash_table_2 = hashTable.from_dict(data, capacity=100)
    assert hash_table_1 == hash_table_2