from .utils import Lakehouse 
from .utils import Util

def get_Lakehouse():
    return Lakehouse()

def dump(obj: object):
    return Util().dump(obj)
