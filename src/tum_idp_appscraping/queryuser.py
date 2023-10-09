from functools import singledispatch
import requests

@singledispatch
def queryuser(arg):
  """
  Returns a user profile by its user internal id (number) or it's username (string) if matched
  """
  return arg

@queryuser.register
def _(arg: int):
  headers = {
    'authority': 'www.threads.net',
    'accept': '*/*',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8,de;q=0.7,it;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.threads.net',
    'pragma': 'no-cache',
    'referer': 'https://www.threads.net/',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-full-version-list': '"Google Chrome";v="117.0.5938.92", "Not;A=Brand";v="8.0.0.0", "Chromium";v="117.0.5938.92"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
  }
  data = {
      'variables': f'{{"userID": "{arg}"}}',
      'doc_id': '6298858840243790',
  }

  print(data)

  response = requests.post('https://www.threads.net/api/graphql', headers=headers, data=data)
  return response.text
  

@queryuser.register
def _(arg: str):
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
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}
  data = {
    'variables': f'{{"username":"{arg}"}}',
    'doc_id': '6422182904495995',
  }

  response = requests.post('https://www.threads.net/api/graphql', headers=headers, data=data)
  print(response)
  return response.text

@singledispatch
def queryuser(arg, dtsg, session_id):
  """
  Returns a user profile by its user internal id (number) or it's username (string) if matched
  """
  return arg