'''Test-driven Development Goals:
1. Resolve has collisions
2. Retain insertion order
3. Dynamically resize hash table
4. Calculate load factor
'''
from re import M
import pytest

from hashtable import hashTable, BLANK # BLANK needed tomark slots as empty

def test_should_pass():
    assert hashTable(max_capacity=100) is not None

def test_max_capacity_report():
    assert len(hashTable(max_capacity=100)) == 100

def test_create_empty_value_slots():
    # Given 
    expected_vals = [BLANK, BLANK, BLANK]
    hash_table = hashTable(max_capacity=3)

    # When 
    actual_vals = hash_table.values

    # Then
    assert actual_vals == expected_vals

def test_insert_keys_and_value_pairs():
    # Given
    hash_table = hashTable(max_capacity=100)

    # When
    hash_table['Hola'] = 'Hello'
    hash_table[98.6] = 37
    hash_table[False] = True

    # Then
    assert "Hello" in hash_table.values
    assert 37 in hash_table.values
    assert True in hash_table.values

    # Additional insertion for additional test
    assert len(hash_table) == 100

def test_table_should_not_contain_none_value_when_created():
    assert None not in hashTable(max_capacity=100).values

def test_insert_none_value():
    # Given
    hash_table = hashTable(max_capacity=100)
    
    # When
    hash_table['key'] = None
    
    # Then
    assert None in hash_table.values

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