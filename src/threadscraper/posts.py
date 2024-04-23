from functools import singledispatch
import requests
from pydantic import Json
from time import sleep
import json
import os
from dotenv import load_dotenv

from threadscraper.postSchemas import ThreadsData, Likers

import logging

load_dotenv()

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
  
def get_post_info(url:str, dtsg: str = None, session_id: str = None) -> Json:
  """
  Gets basic information about a post using its URL.
  Useful to obtain the postID to use in other queries.

  Args:
    url (str): URL of the post. Formats accepted: /username/post/postCode or /t/postCode or only the post code.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    Json: Json object containing the basic information of the post.
  """


  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  assert dtsg != None and session_id != None, "dtsg and session_id are required"

  cookies = {
      'sessionid': session_id,
  }

  try:
    url = url.split("/")
    if len(url) > 3:
      url = url[-3:]
      url = "/".join(url)
    else:
      url = f"t/{url[-1]}"

    url = "/" + url
    data = {
        'route_urls[0]': url,
        'routing_namespace': 'barcelona_web',
        '__user' : '0',
        '__a': '1',
        '__comet_req': '29',
        'fb_dtsg': dtsg,
    }
    print(data)

    response = requests.post('https://www.threads.net/ajax/bulk-route-definitions/', cookies=cookies, headers=headers, data=data)

    res = "{" + response.text.split("for (;;);{")[1]

    res = json.loads(res)["payload"]["payloads"][url]
    print(res)
    if "error" in res and res["error"] == True:
      return res
    elif "redirect_result" in res["result"]:
      return res["result"]["redirect_result"]["exports"]
    else:
      return  res["result"]["exports"]
  except Exception as e:
    logging.error("Error while getting post info", e)
    logging.error("Ensure the provided url is in format /username/post/postCode")
    return {"error": "Error while getting post info"}

def get_thread(postID: int, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:

  '''
  Gets a thread, consisting of the original posts and all replies to
  this post and the replies to the replies of the author

  Args:
    postID (int): Unique numerical identifier of a post.
    n (int): Maximum amount of replies to query.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    Json (ThreadsData): List of objects containing all information about a thread, its different posts and replies
  '''


  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"postID":"{postID}","__relay_internal__pv__BarcelonaIsFirstPostContextLineEnabledrelayprovider":false,"__relay_internal__pv__BarcelonaIsViewCountEnabledrelayprovider":false}}',
      'doc_id': '6888303811288218',
  }
  cookies = {
    'sessionid': session_id,
  } 

  try:
    response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
    res = json.loads(response.text)['data']['data']
    res = ThreadsData.model_validate_json(json.dumps(res, ensure_ascii=False))
    return res.model_dump(mode='json', exclude_unset=True)
  except Exception as e:
    logging.error("Error while getting thread", e)
    return {"error": "Error while getting thread"}

def get_thread_by_url(url: str, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:

  '''
  Gets a thread, consisting of the original posts and all replies to this post and the replies by the author.

  Args:
    url (str): URL of the post. Formats accepted: /username/post/postCode or /t/postCode or only the post code.
    n (int): Maximum amount of replies to query.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    Json (ThreadsData): List of objects containing all information about a thread, its different posts and replies
  '''


  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  postID = get_post_info(url, dtsg, session_id)
  print(postID)
  postID = postID["rootView"]["props"]["post_id"]

  return get_thread(postID, n, delay, dtsg, session_id)

def get_likers(postID: int, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:

  '''
  Collects all (or up to n) likers of a post, sorted by most recent.

  Args:
    postID (int): Unique numerical identifier of a post.
    n (int): Maximum amount of likers to return.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.
    limit (int): Limit size of threads to crawl.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.

  Returns:
     Json (List (User)): List of users object containing information about users who liked the post
  '''


  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")

  cookies = {
    'sessionid': session_id,
  }

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"first":10,"post_id":"{postID}","request_data":{{"sort_type":"most_recent","tab_type":"like"}}}}',
    'doc_id': '6929221547142095',
  }

  response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
  response = json.loads(response.text)
  res = response
  
  cursor = None
  try: 
    cursor = response["data"]["feedback_hub_tab_items"]["page_info"]["end_cursor"]
  except Exception as e:
    logging.error("Cursor not found", e)

  try:
    if n > 0:
      n -= len(response["data"]["feedback_hub_tab_items"]["edges"])
    while (n > 0 or n == -1) and cursor != None:
      data = {
        'fb_dtsg': dtsg,
        'variables': f'{{"after":"{response["data"]["feedback_hub_tab_items"]["page_info"]["end_cursor"]}","first":10,"post_id":"{postID}","request_data":{{"sort_type":"most_recent","tab_type":"like"}}}}',
        'doc_id': '6929221547142095',
      }

      response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
      response = json.loads(response.text)
      cursor = response["data"]["feedback_hub_tab_items"]["page_info"]["end_cursor"]
      
      if len(response["data"]["feedback_hub_tab_items"]["edges"]) > 0:
        res["data"]["feedback_hub_tab_items"]["edges"].extend(response["data"]["feedback_hub_tab_items"]["edges"])
      else:
        break

      if n > 0:
        n -= len(response["data"]["feedback_hub_tab_items"]["edges"])
      sleep(delay)

    res["data"]["feedback_hub_tab_items"]["page_info"] = response["data"]["feedback_hub_tab_items"]["page_info"]
    # res = ThreadsData.model_validate_json(json.dumps(res["data"]["feedback_hub_tab_items"], ensure_ascii=False))
    res = res["data"]["feedback_hub_tab_items"]["edges"]

    for node in res:
      user = node["node"]["actor"]
      res[res.index(node)] = user
    res = {"likers": res}
    logging.debug(res)

    return Likers.model_validate_json(json.dumps(res, ensure_ascii=False)).model_dump(mode='json', exclude_unset=True)
  except Exception as e:
    logging.error("Error while getting likers", e)
    return {"error": "Error while getting likers"}

def get_reposters(postID: int, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:

  '''
  Collects all (or up to n) users who reposted a post, sorted by most recent.

  Args:
    postID (int): Unique numerical identifier of a post.
    n (int): Maximum amount of reposters to return.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.
    limit (int): Limit size of threads to crawl.
    delay (int): Delay among requests to avoid the account of getting suspended by bot activity.

  Returns:
     Json (List (User)): List of users object containing information about users who reposted the post
  '''


  if dtsg == None:
    dtsg = os.getenv("DTSG")
  
  if session_id == None:
    session_id = os.getenv("SESSION")
  
  
  cookies = {
    'sessionid': session_id,
  }

  data = {
    'fb_dtsg': dtsg,
    'variables': f'{{"first":10,"post_id":"{postID}","request_data":{{"sort_type":"most_recent","tab_type":"repost"}}}}',
    'doc_id': '6929221547142095',
  }

  try:
    response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
    response = json.loads(response.text)
    res = response
    cursor = None
    try: 
      cursor = response["data"]["feedback_hub_tab_items"]["page_info"]["end_cursor"]
    except Exception as e:
      logging.error("Cursor not found", e)

    if n > 0:
      n -= len(response["data"]["feedback_hub_tab_items"]["edges"])
    while (n > 0 or n == -1) and cursor != None:
      data = {
        'fb_dtsg': dtsg,
        'variables': f'{{"after":"{cursor}","first":10,"post_id":"{postID}","request_data":{{"sort_type":"most_recent","tab_type":"repost"}}}}',
        'doc_id': '6929221547142095',
      }

      response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
      response = json.loads(response.text)
      cursor = response["data"]["feedback_hub_tab_items"]["page_info"]["end_cursor"]
      
      if len(response["data"]["feedback_hub_tab_items"]["edges"]) > 0:
        res["data"]["feedback_hub_tab_items"]["edges"].extend(response["data"]["feedback_hub_tab_items"]["edges"])
      else:
        break

      if n > 0:
        n -= len(response["data"]["feedback_hub_tab_items"]["edges"])
      sleep(delay)

    res["data"]["feedback_hub_tab_items"]["page_info"] = response["data"]["feedback_hub_tab_items"]["page_info"]
      # res = ThreadsData.model_validate_json(json.dumps(res["data"]["feedback_hub_tab_items"], ensure_ascii=False))

    res = res["data"]["feedback_hub_tab_items"]["edges"]

    for node in res:
      user = node["node"]["actor"]
      res[res.index(node)] = user
    res = {"likers": res}
    logging.debug(res)

    return Likers.model_validate_json(json.dumps(res, ensure_ascii=False)).model_dump(mode='json', exclude_unset=True)
  except Exception as e:
    logging.error("Error while getting reposters", e)
    return {"error": "Error fetching reposters"}

def get_quotes(postID: int, n: int = 100, delay: float = 1, dtsg: str = None, session_id: str = None) -> Json:
  
    '''
    Collects all (or up to n) quotes and the users who quoted a post, sorted by most recent.
  
    Args:
      postID (int): Unique numerical identifier of a post.
      n (int): Maximum amount of quoters to return.
      dtsg (str): Value generated by Meta to validated the session.
      session_id (str): Cookie identifier for the user session.
      limit (int): Limit size of threads to crawl.
      delay (int): Delay among requests to avoid the account of getting suspended by bot activity.
  
    Returns:
      Json (List (User)): List of users object containing information about users who quoted the post
    '''
  
  
    if dtsg == None:
      dtsg = os.getenv("DTSG")
    
    if session_id == None:
      session_id = os.getenv("SESSION")
    
    cookies = {
      'sessionid': session_id,
    }

    data = {
      'fb_dtsg': dtsg,
      'variables': f'{{"after":null,"first":null,"post_id":"{postID}","request_data":{{"sort_type":"most_recent","tab_type":"quote"}}}}',
      'doc_id': '6929221547142095',
    }

    try:
      response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
      response = json.loads(response.text)
      edges = response["data"]["feedback_hub_tab_items"]["edges"]

      cursor = None
      try: 
        cursor = response["data"]["feedback_hub_tab_items"]["page_info"]["end_cursor"]
      except Exception as e:
        logging.error("Cursor not found", e)

      if n > 0:
        n -= len(response["data"]["feedback_hub_tab_items"]["edges"])

      while (n > 0 or n == -1) and cursor != None:
        data = {
          'fb_dtsg': dtsg,
          'variables': f'{{"after":"{cursor}","first":null,"post_id":"{postID}","request_data":{{"sort_type":"most_recent","tab_type":"quote"}}}}',
          'doc_id': '6929221547142095',
        }
        response = requests.post('https://www.threads.net/api/graphql', cookies=cookies, headers=headers, data=data)
        response = json.loads(response.text)
        cursor = response["data"]["feedback_hub_tab_items"]["page_info"]["end_cursor"]
        
        if len(response["data"]["feedback_hub_tab_items"]["edges"]) > 0:
          edges.extend(response["data"]["feedback_hub_tab_items"]["edges"])
        else:
          break

        if n > 0:
          n -= len(response["data"]["feedback_hub_tab_items"]["edges"])
        sleep(delay)
          # res = ThreadsData.model_validate_json(json.dumps(res["data"]["feedback_hub_tab_items"], ensure_ascii=False))
      return edges
    except Exception as e:
      logging.error("Error while getting quotes", e)
      return {"error": f"Error fetching quotes {e}"}

def download_media(mediaURL:str,  path: str = None) -> bool:
  '''
  Downloads the media from the specified url.

  Args:
    mediaURL (int): URL of the media.

  Returns:
    bool: True if the media was downloaded successfully, False otherwise.
  '''
  try:
    response = requests.get(mediaURL, stream=True)

    if response.status_code != 200:
      return False

    if path is None:
      path = mediaURL.split("/")[-1]

    if ".jpg" not in path and ".mp4" not in path:
      if ".jpg" in mediaURL:
        extension = ".jpg"
      elif ".mp4" in mediaURL:
        extension = ".mp4"
      elif ".webp" in mediaURL:
        extension = ".webp"
      
      logging.info("Saving %s file", extension)
      path = path + extension

    if not os.path.exists(os.path.dirname(path)):
      os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

    return True
  except Exception as e:
    logging.error("Error while downloading media", e)
    return False

def download_all_media(post: str | int,  path: str = None, dtsg: str = None, session_id: int = None) -> bool:
  '''
  Downloads the media of a given post.

  Args:
    post (int): postID of the post.
    post (str): URL of the post.
    path (str): Path to save the media.
    dtsg (str): Value generated by Meta to validated the session.
    session_id (str): Cookie identifier for the user session.

  Returns:
    bool: True if the media was downloaded successfully, False otherwise.
  '''
  if isinstance(post, str):
    post = get_post_info(post, dtsg, session_id)["rootView"]["props"]["post_id"]
  
  if path is None:
    path = post

  thread = get_thread(post, dtsg, session_id)
  post = thread["edges"][0]["node"]["thread_items"][0]["post"]

  i = 0
  if "carousel_media" in post and post["carousel_media"] != None:
    for node in post["carousel_media"]:
      candidate = node["image_versions2"]["candidates"][0]
      if download_media(candidate["url"], f"{path}_{i}.jpg") == False:
        return False
      i += 1
  
  else:
    if len(post["image_versions2"]["candidates"]) > 0:
      candidate = post["image_versions2"]["candidates"][0]
      if download_media(candidate["url"], f"{path}_{i}.jpg") == False:
        return False
      i += 1

  if "video_versions" in post and post["video_versions"] != None:
    for node in post["video_versions"]:
      if download_media(node["url"], f"{path}_{i}.mp4") == False:
        return False
      i += 1


  return True