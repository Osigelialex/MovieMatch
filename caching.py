"""A module for caching search results
"""
from typing import Dict


class Cache:
  """implements a simple cache for search results
  """
  
  MAX_SIZE = 25

  def __init__(self) -> None:
    """Initializes the cache
    """
    self.cached_data = {}
  
  @staticmethod
  def validate_inputs(key: str, value: Dict) -> bool:
    """Validates key and value inputs

    Args:
        key (str): movie Title
        value (Dict): Movie data

    Returns:
        bool: True or False
    """
    if key is None or len(value) == 0:
      return False
    return True
  
  def put(self, key: str, value: Dict) -> None:
    """Stores key with value in cache

    Args:
        key (str): Title of searched movie
        value (Dict): data about movie gotten from API
    """
    input_is_valid = self.validate_inputs(key, value)
    if not input_is_valid:
      return
    
    if len(self.cached_data) == Cache.MAX_SIZE:
      self.cached_data.pop()
      self.cached_data[key] = value
    
    self.cached_data[key] = value
  
  def get(self, key: str) -> Dict:
    """Gets stored value in cache
    
    Args:
      key (str): Title of movie
    """ 
    if key is None or key not in self.cached_data:
      return None
    
    return self.cached_data[key]
    