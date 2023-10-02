import json
from appscraping import queryuser

def test_queryuser():
  result = queryuser("jeffnippard")
  print(result)
  assert type(result) == json