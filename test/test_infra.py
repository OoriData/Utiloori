'''
pytest test

or

pytest test/test_infra.py
'''
from utiloori import __about__

def test_version():
    assert __about__.__version__ == __about__.__version__