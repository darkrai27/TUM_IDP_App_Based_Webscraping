from functools import singledispatch
import requests
from pydantic import Json
from time import sleep
import json
import os
from dotenv import load_dotenv

from userSchemas import (
  Json1,
  Json2,
  FollowsInfo
)

from postSchemas import (
  JsonPosts
)

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
def queryuser(arg, dtsg: str, session_id: str) -> Json:
  """
  Returns a user profile by its user internal id (number) or it's username (string) is matched.

  Args:
    arg (int): unique user internal id.
    arg (str): unique username of the user.
    dtsg (str): Value generated by Facebook to validated the session.
    session_id (str): Cookie identifier for the user session.

  """
  return arg

@queryuser.register
def _(arg: int, dtsg: str = None, session_id: str = None) -> json:

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
  
  # res = Json1.model_validate_json(response.text)
  res = json.loads(response.text)
  res = res

  return res
  
@queryuser.register
def _(arg: str, dtsg: str = None, session_id: str = None) -> json:
  
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
  # res = Json2.model_validate_json(response.text)
  res = json.loads(response.text)
  return res

def get_posts(username, dtsg: str = None, session_id: str = None) -> json:
  '''
  Returns the most recent posts of a user by its internal user id.

  Args:
    username (str): unique username of the user.
    dtsg (str): Value generated by Facebook to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    Json: Most recent posts of the user inside the list "edges"
  '''


  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  profile = queryuser(username, dtsg, session_id)
  profile = json.dumps(profile, ensure_ascii=False) #Convert the json to string to verify it as Json2
  profile = Json2.model_validate_json(profile)
  user_id = profile.data.xdt_user_by_username.pk

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{user_id}"}}',
      'doc_id': '23980155134932173',
  }
  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  res = json.loads(response.text)
  return res

def get_replys(username, dtsg: str = None, session_id: str = None) -> json:
  '''
  Returns the most recent replys of a user to other user's posts
  and the posts it was originally replying.
  Similar to get_posts but por posts replying other users content.

  Args:
    username (str): unique username of the user
    dtsg (str): Value generated by Facebook to validated the session
    session_id (str): Cookie identifier for the user session

  Returns:
    List[Edge]: List of "Edges" objects containing in each node at least 2 "thread items" being the first
    a post by other user and the seconf the reply from the specified user
  '''
  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  profile = queryuser(username, dtsg, session_id)
  profile = json.dumps(profile, ensure_ascii=False) #Convert the json to string to verify it as Json2
  profile = Json2.model_validate_json(profile)
  user_id = profile.data.xdt_user_by_username.pk

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"userID":"{user_id}","__relay_internal__pv__BarcelonaIsPollsConsumptionEnabledrelayprovider":true,"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaIsFeedbackHubEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaIsViewCountEnabledrelayprovider":false}}',
    'doc_id': '24067823902863248',
  }

  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  res = json.loads(response.text)
  return res

def get_reposts(username, dtsg: str = None, session_id: str = None):
  '''
  Returns the most recent posts of a user by its internal user id.
  Similar to get_posts but por reposted content from other users.

  Args:
    username (str): unique username of the user
    dtsg (str): Value generated by Facebook to validated the session
    session_id (str): Cookie identifier for the user session

  Returns:
    Json: Most recent posts of the user inside the list "edges"
  '''
  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  profile = queryuser(username, dtsg, session_id)  
  profile = json.dumps(profile, ensure_ascii=False) #Convert the json to string to verify it as Json2
  profile = Json2.model_validate_json(profile)
  user_id = profile.data.xdt_user_by_username.pk

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"userID":"{user_id}","__relay_internal__pv__BarcelonaIsPollsConsumptionEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaIsFeedbackHubEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaIsViewCountEnabledrelayprovider":false}}',
    'doc_id': '5903296406439337',
  }

  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)

  return json.loads(response.text)

def get_follows_info(username: str, dtsg: str = None, session_id: str = None) -> str:
  '''
  Returns an overview information of the number of followers and following of an account
  Using the internal userID to perform the query.

  Args:
    username (str): unique username of the user
    dtsg (str): Value generated by Facebook to validated the session
    session_id (str): Cookie identifier for the user session

  Returns:
    Json: total_followers_count, total_follow_count and total_pending_follow_count
  '''

  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")
  
  profile = queryuser(username, dtsg, session_id)
  profile = json.dumps(profile, ensure_ascii=False) #Convert the json to string to verify it as Json2
  profile = Json2.model_validate_json(profile)

  user_id = profile.data.xdt_user_by_username.pk

  cookies = {
    'sessionid': session_id
  }

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID":"{user_id}"}}',
      'doc_id': '6732076973551340',
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)

  return json.loads(response.text)

def get_followers(username: int, dtsg: str = None, session_id: str = None):

  '''
  Collects the latest users who followed an account likers of a post

  Args:
    postID (int): Unique numerical identifier of a post.
    dtsg (str): Value generated by Facebook to validated the session.
    session_id (str): Cookie identifier for the user session.
    limit (int): Limit size of threads to crawl.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.

  Returns:
    List (User): List of users object containing information about the users who followed certain acount
  '''
  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")
  
  profile = queryuser(username, dtsg, session_id)
  profile = json.dumps(profile, ensure_ascii=False) #Convert the json to string to verify it as Json2
  profile = Json2.model_validate_json(profile)

  user_id = profile.data.xdt_user_by_username.pk

  cookies = {
    'sessionid': session_id
  }

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID":"{user_id}"}}',
      'doc_id': '7438202066196885',
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)

  return json.loads(response.text)

def get_following(username: int, dtsg: str = None, session_id: str = None):

  '''
  Collects the most recent follows an account followed.

  Args:
    postID (int): Unique numerical identifier of a post.
    dtsg (str): Value generated by Facebook to validated the session.
    session_id (str): Cookie identifier for the user session.
    limit (int): Limit size of threads to crawl.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.

  Returns:
    List (User): List of users who followed the specified user most recently.
  '''
  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")
  
  profile = queryuser(username, dtsg, session_id)
  profile = json.dumps(profile, ensure_ascii=False) #Convert the json to string to verify it as Json2
  profile = Json2.model_validate_json(profile)

  user_id = profile.data.xdt_user_by_username.pk

  cookies = {
    'sessionid': session_id
  }

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID":"{user_id}"}}',
      'doc_id': '6835301726531323',
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)

  return json.loads(response.text)

def crawl_all(username: str, mode: str, dtsg: str = None, session_id: str = None, limit:int = None, delay: int = 5):
  '''
  Returns all posts/replies or reposts or the most recent ones up to a specified limit of
  certain.
  Strategy: use the unique user internal id to perform recursive queries.
  Performs each query with certain delay to avoid banning the account for bot activity.

  Args:
    username (str): unique username of the user
    mode (str): "post" for posts, "reply" for replies and "repost" for reposts
    dtsg (str): Value generated by Facebook to validated the session
    session_id (str): Cookie identifier for the user session
    limit (int): Limit of posts to query. From most recent to older. None by default
    delay (int): Delay in seconds between each recursive query to avoid accounts suspensions for bot activity. 5 by default

  Returns:
    Json: All posts of the user contained in the "edges" list.
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

  profile = queryuser(username, dtsg, session_id)

  profile = Json2.model_validate_json(profile)
  user_id = profile.data.xdt_user_by_username.pk

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"userID": "{user_id}", "__relay_internal__pv__BarcelonaIsPollsConsumptionEnabledrelayprovider":{str(mode == "reply").lower()},"__relay_internal__pv__BarcelonaIsLoggedInrelayprovider":true,"__relay_internal__pv__BarcelonaIsFeedbackHubEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaIsViewCountEnabledrelayprovider":false}}',
    'doc_id': doc_id,
  }

  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  print(response.text)
  response = json.loads(response.text)
  res = response
  
  cursor = None
  try: 
    cursor = response["data"]["mediaData"]["page_info"]["end_cursor"]
  except:
    print("Cursor not found")  

  while True and (limit == None or limit > 0) and cursor != None:
    data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{user_id}", "first": "10", "after": "{response["data"]["mediaData"]["page_info"]["end_cursor"]}"}}',
      'doc_id': '23980155134932173',
    }
    response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
    response = json.loads(response.text)
    cursor = response["data"]["mediaData"]["page_info"]["end_cursor"]
    
    if len(response["data"]["mediaData"]["edges"]) > 0:
      res["data"]["mediaData"]["edges"].extend(response["data"]["mediaData"]["edges"])
    else:
      break

    if limit != None:
      limit -= len(response["data"]["mediaData"]["edges"])
    sleep(5)
  
  res["data"]["mediaData"]["page_info"] = response["data"]["mediaData"]["page_info"]

  print(len(res["data"]["mediaData"]["edges"]))
  return res