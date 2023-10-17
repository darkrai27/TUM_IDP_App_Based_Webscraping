from functools import singledispatch
import requests
from pydantic import Json
from time import sleep
import json
from schemas import (
  HdProfilePicVersion,
  FriendshipStatus,
  BiographyWithEntities,
  User,
  Data,
  Extensions,
  Json1,
  UserData,
  Json2,
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

# -----------------------------------
# DISCARDED CODE, DOESN'T WORK ANYMORE WITHOUT A FB_LSD HEADER
# @singledispatch
# def queryuser(arg):
#   """
#   Returns a user profile by its user internal id (number) or it's username (string) if matched
#   """
#   return arg

# @queryuser.register
# def _(arg: int):
#   data = {
#       'variables': f'{{"userID": "{arg}"}}',
#       'doc_id': '6298858840243790',
#   }

#   response = requests.post('https://www.threads.net/api/graphql', headers=headers, data=data)
#   res = json.loads(response.text)
#   return res
  

# @queryuser.register
# def _(arg: str):
  
#   data = {
#     'variables': f'{{"username":"{arg}"}}',
#     'doc_id': '6422182904495995',
#   }

#   response = requests.post('https://www.threads.net/api/graphql', headers=headers, data=data)
#   res = json.loads(response.text)
#   return res
# --------------------------------------------------------------------

@singledispatch
def queryuser(arg, dtsg: str, session_id: str) -> Json:
  """
  Returns a user profile by its user internal id (number) or it's username (string) is matched
  """
  return arg

@queryuser.register
def _(arg: int, dtsg: str, session_id: str) -> Json:

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{arg}"}}',
      'doc_id': '6298858840243790',
  }
  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  print(response.text)
  res = Json1.model_validate_json(response.text)
  return res.data.userData.user
  

@queryuser.register
def _(arg: str, dtsg: str, session_id: str) -> Json:
  
  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"username":"{arg}"}}',
    'doc_id': '6422182904495995',
  }
  cookies = {
    'sessionid': session_id,
  } 

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  print(response.text)
  res = Json2.model_validate_json(response.text)
  return res


def get_posts(user_id):
  """
  Returns the most recent posts of a user by its internal user id
  """

  headers = {
    'Accept': '*/*',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.threads.net',
    'Referer': 'https://www.threads.net',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'X-FB-LSD': 'CckP51ktiQJqnm9K9NKc9Z',
    'dpr': '1',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="117.0.5938.150", "Not;A=Brand";v="8.0.0.0", "Chromium";v="117.0.5938.150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'viewport-width': '1704',
    # 'Cookie': 'csrftoken=rs0WHowG_ZMKdhoQqWc0uM; mid=ZSgNpgALAAHGMd_duJ8JKbjmqDJy',
  }
  data = {
    'lsd': 'CckP51ktiQJqnm9K9NKc9Z',
    'variables': f'{{"userID": "{user_id}"}}',
    'doc_id': '23980155134932173',
  }

  response = requests.post('https://www.threads.net/api/graphql', headers=headers, data=data)
  res = json.loads(response.text)
  return res

def get_posts(username, dtsg, session_id):
  """
  Returns most recent posts of a user by its internal user id
  """

  profile = queryuser(username, dtsg, session_id)
  user_id = profile["data"]["xdt_user_by_username"]["pk"]

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

def scrap_all_posts(username: str, dtsg: str, session_id: str, limit:int = None, delay: int = 5):
  """
  Returns all posts of the account with the passed username using its internal user_id or the most recent up post to a limit of posts.
  Each query is performed each delay seconds (5 by default) to avoid banning the account for bot activity.
  """

  profile = queryuser(username, dtsg, session_id)

  user_id = profile["data"]["xdt_user_by_username"]["pk"]

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"userID": "{user_id}"}}',
    'doc_id': '23980155134932173',
  }
  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  print(response.text)
  response = json.loads(response.text)
  cursor = response["data"]["mediaData"]["page_info"]["end_cursor"]
  res = response

  while True and (limit == None or limit > 0) and cursor != None:
    print(cursor)
    print(len(response["data"]["mediaData"]["edges"]))
    data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{user_id}", "first": "10", "after": "{response["data"]["mediaData"]["page_info"]["end_cursor"]}"}}',
      'doc_id': '23980155134932173',
    }
    response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
    print(response.text)
    response = json.loads(response.text)
    cursor = response["data"]["mediaData"]["page_info"]["end_cursor"]
    
    if len(response["data"]["mediaData"]["edges"]) > 0:
      res["data"]["mediaData"]["edges"].extend(response["data"]["mediaData"]["edges"])
    else:
      break

      
    # for edge in response["data"]["mediaData"]["edges"]:
    #   res["data"]["mediaData"]["edges"].append(edge)

    if limit != None:
      limit -= len(response["data"]["mediaData"]["edges"])
    sleep(5)

  print(len(res["data"]["mediaData"]["edges"]))
  return res

def get_follows_info(username: str, dtsg: str, session_id: str):
  "Returns an overview information of the number of followers and following of an account"
  profile = queryuser(username, dtsg, session_id)

  user_id = profile["data"]["xdt_user_by_username"]["pk"]

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