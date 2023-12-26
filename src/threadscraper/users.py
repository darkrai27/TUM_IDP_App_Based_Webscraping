from functools import singledispatch
import requests
from pydantic import Json
from time import sleep
import json
import os
from dotenv import load_dotenv

from threadscraper.userSchemas import User, FollowsCounts
from threadscraper.postSchemas import ThreadsData

"""
This file contains all functions to retrieve specific information about a user
"""

headers = {
  'authority': 'www.threads.net',
  'accept': '*/*',
  'accept-language': 'es-ES,es;q=0.7',
  'content-type': 'application/x-www-form-urlencoded',
  'origin': 'https://www.threads.net',
  'referer': 'https://www.threads.net/search',
  'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-model': '""',
  'sec-ch-ua-platform': '"macOS"',
  'sec-ch-ua-platform-version': '"13.4.0"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

load_dotenv('.env')

@singledispatch
def get_user_info(arg, dtsg: str, session_id: str) -> Json:
  """
  Returns a user profile by its user internal id (number) or it's username (string) if matched with an existing one.
  Using the internal id provides more output data in friendship_data and bio_links.

  Args:
    arg (int): unique user internal id.
    arg (str): unique username of the user.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    Json (User): Json containing all information about the user.

  """
  return arg

@get_user_info.register
def _(arg: int, dtsg: str = None, session_id: str = None) -> Json:

  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{arg}"}}',
      'doc_id': '6298858840243790',
  }
  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)

  if response.ok:
    try:
    # res = Json1.model_validate_json(response.text)
      res = json.loads(response.text)['data']['userData']['user']
      print(res)
      res = User.model_validate_json(json.dumps(res, ensure_ascii=False))

      return res.model_dump(mode='json', exclude_unset=True)
    except:
      print("Error - Invalid session / response. Please check your sessiones and try again.")
  else: 
    print(f"Error - Invalid response, status code: {response.status_code}")
  return None
  
@get_user_info.register
def _(arg: str, dtsg: str = None, session_id: str = None) -> Json:
  
  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"username":"{arg}"}}',
    'doc_id': '6422182904495995',
  }
  cookies = {
    'sessionid': session_id,
  } 

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  if response.ok:
    try:
      res = json.loads(response.text)['data']['xdt_user_by_username']
      res = User.model_validate_json(json.dumps(res, ensure_ascii=False))
      return res.model_dump(mode='json', exclude_unset=True)
    except Exception as e:
      print("Error - Invalid session / response. Please check your sessiones and try again.", e)
  else: 
    print(f"Error - Invalid response, status code: {response.status_code}")
  return None
    
def get_follows_info(username: str, dtsg: str = None, session_id: str = None) -> Json:
  '''
  Returns an overview information of the number of followers and following of an account
  using the internal userID to perform the query.

  Args:
    username (str): unique username of a user
    dtsg (str): Value generated by Meta to validated the session
    session_id (str): Cookie identifier for the user session

  Returns:
    Json (FollowsCounts): Object containing all counts of follows, following and pending follows.
  '''

  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")
  
  profile = get_user_info(username, dtsg, session_id)
  profile = User.model_validate(profile)

  user_id = profile.pk

  cookies = {
    'sessionid': session_id
  }

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID":"{user_id}"}}',
      'doc_id': '6732076973551340',
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  response = json.loads(response.text)
  response = FollowsCounts.model_validate_json(json.dumps(response["data"]["counts"], ensure_ascii=False))

  return FollowsCounts.model_dump(response, mode='json', exclude_unset=True)

def get_fw(username: str, mode: str, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:
  """
  Wrapper function to perforrm the logic and queries of get_followers and get_following
  """
  
  if mode == "followers":
    doc_id = '6615219665191418'
  elif mode == "following":
    doc_id = '6602037909881597'
  else:
    assert False, "Invalid mode"
  
  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")
  
  profile = get_user_info(username, dtsg, session_id)
  profile = User.model_validate(profile)

  user_id = profile.pk

  cookies = {
    'sessionid': session_id
  }

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"userID":"{user_id}"}}',
    'doc_id': doc_id
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  response = json.loads(response.text)
  res = response

  count = len(response["data"][mode]["edges"])
  end_cursor = response["data"][mode]["page_info"]["end_cursor"]
  if end_cursor is None:
    end_cursor = count

  while (count < n or n == -1) and res["data"][mode]["page_info"]["has_next_page"]:
    data['variables'] = f'{{"after":"{end_cursor}","before":null,"count":20,"first":10,"last":null,"userID":"{user_id}","__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true}}'
    response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
    response = json.loads(response.text)
    if response["data"][mode]["edges"] is not None:
      res["data"][mode]["edges"].extend(response["data"][mode]["edges"])
      count += len(response["data"][mode]["edges"])
      end_cursor = response["data"][mode]["page_info"]["end_cursor"]
    
    sleep(delay)

  return res["data"][mode]["edges"]

def get_followers(username: int, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:

  '''
  Collects all (or n) followers of the specified account.
  Limited to 50 for some accounts - apparently if the account is verified.
  (The 50 more relevant for the account we are using to perform the query)

  Args:
    username (str): Unique username of the user
    n (int): Maximum amount of people following to return. Use -1 to get all of them.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    Json: List of users object containing information about the users who followed certain acount
  '''
  return get_fw(username, "followers", n, delay, dtsg, session_id)

def get_following(username: int, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:

  '''
  Collects all (or n) accounts being followed by the specified user.

  Args:
    username (str): Unique username of the user
    n (int): Maximum amount of people following to return. Use -1 to get all of them.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    Json: List of users who followed the specified user most recently.
  '''
  return get_fw(username, "following", n, delay, dtsg, session_id)

def get_user_posts(username: str, mode: str, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:
  '''
  Returns all posts, replies or reposts or the most recent ones from the requested user up to a specified limit.

  Strategy: use the unique user internal id to perform recursive queries.
  Performs each query with certain delay to avoid banning the account for bot activity.

  Args:
    username (str): Unique username of the user
    mode (str): "post" for posts, "reply" for replies and "repost" for reposts
    n (int): Maximum amount of posts to query. From most recent to older. 100 by default
    dtsg (str): Value generated by Meta to validated the session
    session_id (str): Cookie identifier for the user session
    delay (int): Delay in seconds between each recursive query to avoid accounts suspensions for bot activity. 5 by default

  Returns:
    Json (ThreadsData): Collection of threads of a given user.
  '''

  if mode == "post":
    doc_id = '23980155134932173'
  elif mode == "reply":
    doc_id = '24067823902863248'
  elif mode == "repost":
    doc_id = '5903296406439337'
  else:
    raise Exception("Invalid mode")

  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  profile = get_user_info(username, dtsg, session_id)

  profile = User.model_validate(profile)
  user_id = profile.pk

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"userID": "{user_id}", "__relay_internal__pv__BarcelonaIsPollsConsumptionEnabledrelayprovider":{str(mode == "reply").lower()},"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaIsFeedbackHubEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaIsViewCountEnabledrelayprovider":false}}',
    'doc_id': doc_id,
  }

  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  response = json.loads(response.text)
  res = response
  
  cursor = None
  try: 
    cursor = response["data"]["mediaData"]["page_info"]["end_cursor"]
  except:
    print("Cursor not found")

  if n > 0:
    n -= len(response["data"]["mediaData"]["edges"])
  while (n > 0 or n == -1) and cursor != None:
    data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{user_id}", "first": "50", "after": "{response["data"]["mediaData"]["page_info"]["end_cursor"]}"}}',
      'doc_id': '23980155134932173',
    }
    response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
    response = json.loads(response.text)
    cursor = response["data"]["mediaData"]["page_info"]["end_cursor"]
    
    if len(response["data"]["mediaData"]["edges"]) > 0:
      res["data"]["mediaData"]["edges"].extend(response["data"]["mediaData"]["edges"])
    else:
      break

    if n > 0:
      n -= len(response["data"]["mediaData"]["edges"])
    sleep(delay)
  
  res["data"]["mediaData"]["page_info"] = response["data"]["mediaData"]["page_info"]
  
  print(len(res["data"]["mediaData"]["edges"]))
  res = ThreadsData.model_validate_json(json.dumps(res["data"]["mediaData"], ensure_ascii=False))
  return res.model_dump(mode='json', exclude_unset=True)