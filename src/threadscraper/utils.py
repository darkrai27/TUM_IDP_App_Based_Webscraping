import json
from typing import List
from threadscraper.postSchemas import Edge, Post
import logging

logging.basicConfig(level=logging.INFO)


def extract_captions(edges: List[Edge]):
  """
  Extracts all captions from the posts of a given list of edges.

  Args:
    edges (List[Edge]): List of edges to extract the captions from.
  """
  captions = []
  for edge in edges:
    for item in edge.node.thread_items:
      repost = item.post.text_post_app_info.share_info.reposted_post
      if repost is not None:
        if repost.caption is not None:
          if repost.caption.text is not None:
            captions.append(repost.caption.text)
      if item.post.caption is not None:
        if item.post.caption.text is not None:
          captions.append(item.post.caption.text)
    
  return captions

def extract_medias(post):
  """
  Extracts all medias from all posts of a given list of edges.

  Args:
    edges (List[Edge]): List of edges to extract the medias from.
  """
  medias = {}
  for edge in post["edges"]:
    for item in edge["node"]["thread_items"]:
      if item["post"]["carousel_media"] is not None:
        for media in item["post"]["carousel_media"]:
          if media["video_versions"] is not None:
            for video in media["video_versions"]:
              urlKey = video["url"].split("?")[0]
              if urlKey not in medias:
                medias[urlKey] = [video["url"]]
              else:
                medias[urlKey].append(video["url"])
          if media["image_versions2"] is not None:
            for candidate in media["image_versions2"]["candidates"]:
              urlKey = candidate["url"].split("?")[0]
              if urlKey not in medias:
                medias[urlKey] = [candidate["url"]]
              else:
                medias[urlKey].append(candidate["url"])
      if item["post"]["image_versions2"] is not None:
        for candidate in item["post"]["image_versions2"]["candidates"]:
            urlKey = candidate["url"].split("?")[0]
            if urlKey not in medias:
              medias[urlKey] = [candidate["url"]]
            else:
              medias[urlKey].append(candidate["url"])     
      if item["post"]["video_versions"] is not None:
        for video in item["post"]["video_versions"]:
          logging.info("video %s", video["url"])
          urlKey = video["url"].split("?")[0]
          if urlKey not in medias:
            medias[urlKey] = [video["url"]]
          else:
            medias[urlKey].append(video["url"])
          logging.info("%s", medias[urlKey])
  return medias
