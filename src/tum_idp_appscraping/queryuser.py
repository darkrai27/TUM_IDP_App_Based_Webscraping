from functools import singledispatch
import requests
import json
from time import sleep

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

@singledispatch
def queryuser(arg):
  """
  Returns a user profile by its user internal id (number) or it's username (string) if matched
  """
  return arg

@queryuser.register
def _(arg: int):
  data = {
      'variables': f'{{"userID": "{arg}"}}',
      'doc_id': '6298858840243790',
  }

  print(data)

  response = requests.post('https://www.threads.net/api/graphql', headers=headers, data=data)
  res = json.loads(response.text)
  return res
  

@queryuser.register
def _(arg: str):
  
  data = {
    'variables': f'{{"username":"{arg}"}}',
    'doc_id': '6422182904495995',
  }

  response = requests.post('https://www.threads.net/api/graphql', headers=headers, data=data)
  res = json.loads(response.text)
  return res

@singledispatch
def queryuser(arg, dtsg, session_id):
  """
  Returns a user profile by its user internal id (number) or it's username (string) if matched
  """
  return arg

@queryuser.register
def _(arg: int, dtsg, session_id):

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{arg}"}}',
      'doc_id': '6298858840243790',
  }
  cookies = {
    'sessionid': session_id,
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  res = json.loads(response.text)
  return res
  

@queryuser.register
def _(arg: str, dtsg, session_id):
  
  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"username":"{arg}"}}',
    'doc_id': '6422182904495995',
  }
  cookies = {
    'sessionid': session_id,
  } 

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  res = json.loads(response.text)
  return res


def query_posts(user_id):
  """
  Returns all posts of a user by its internal user id
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

def queryuser_posts(user_id, dtsg, session_id):
  """
  Returns most recent posts of a user by its internal user id
  """

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

def scrap_all(user_id, dtsg, session_id, limit=None):
  """
  Returns all posts of a user by its internal user id or the most recent up to a limit of posts
  """

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
  res = response

  while True and (limit == None or limit > 0):
    print(response["data"]["mediaData"]["page_info"]["end_cursor"])
    print(len(response["data"]["mediaData"]["edges"]))
    data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"userID": "{user_id}", "first": "10", "after": "{response["data"]["mediaData"]["page_info"]["end_cursor"]}"}}',
      'doc_id': '23980155134932173',
    }
    response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
    print(response.text)
    response = json.loads(response.text)
    
    if len(response["data"]["mediaData"]["edges"]) > 0:
      res["data"]["mediaData"]["edges"].extend(response["data"]["mediaData"]["edges"])
    else:
      break
    
    # for edge in response["data"]["mediaData"]["edges"]:
    #   res["data"]["mediaData"]["edges"].append(edge)

    if limit != None:
      limit -= 10
    sleep(5)

  print(len(res["data"]["mediaData"]["edges"]))
  return res