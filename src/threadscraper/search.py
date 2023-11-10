from functools import singledispatch
import requests
from pydantic import Json
from time import sleep
import json
import os
from dotenv import load_dotenv


def search_users(query: str, dtsg: str = None, session_id: str = None) -> Json:
  '''
  Searches user by the specified query.

  Args:
    query (str): text to look users for. Potentially usernames or complete names.
    dtsg (str): Value generated by Meta to validated the session
    session_id (str): Cookie identifier for the user session

  Returns:
    List[User]: List of most relevant results and suggestions matching the query
  '''
  pass


def search_posts(query: str, dtsg: str = None, session_id: str = None, limit: int = 10, delay: int = 5) -> Json:
  '''
  Performs a search of posts matching the query or posted by users whose username
  matches the query

  Args:
    query (str): Search query.
    dtsg (str): Value generated by Meta to validated the session
    session_id (str): Cookie identifier for the user session
    limit (int, optional): Maximum amount of posts to search for. Defaults to 10.
    delay (int, optional): Delay between requests in seconds. Defaults to 5.

  Returns:
    Json (ThreadsData): List of nodes containing the most relevant threads results matching the query.
  '''
  pass