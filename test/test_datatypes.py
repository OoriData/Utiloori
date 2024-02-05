'''
pytest test

or

pytest test/test_datatypes.py
'''
import utiloori.datatypes

def test_validate_uuid():
    assert utiloori.datatypes.validate_uuid('123e4567-e89b-12d3-a456-426614174000') == True
    assert utiloori.datatypes.validate_uuid('123e4567-e89b-12d3-a456-42661417400') == False
    assert utiloori.datatypes.validate_uuid('123e4567-e89b-12d3-a456-4266141740000') == False
    assert utiloori.datatypes.validate_uuid('123e4567-e89b-12d3-a456-42661417400-') == False
