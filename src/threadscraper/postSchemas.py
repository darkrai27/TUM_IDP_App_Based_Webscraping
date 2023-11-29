from pydantic import BaseModel, Field, root_validator
from typing import List, Optional
from typing import ForwardRef

from threadscraper.userSchemas import User, UserIdentifiers, UserBasicInfo
from threadscraper.mediaSchemas import Image, ImageVersions2, VideoVersions, Audio, CarouselMedia, GiphyMediaInfo

class PinnedPostInfo(BaseModel):
    """
    """
    can_viewer_pin_to_profile : Optional[bool] = False
    can_viewer_unpin_from_profile : Optional[bool] = False
    can_viewer_pin_to_parent_post : Optional[bool] = False
    can_viewer_unpin_from_parent_post : Optional[bool] = False
    is_pinned_to_profile : Optional[bool] = False
    is_pinned_to_parent_pos : Optional[bool] = False

# Allows us to use Post in ShareInfo before it's defined
# So we can have a Post object inside a Post object (repost)
PostForwardRef = ForwardRef("Post")

class ShareInfo(BaseModel):
    """
    Object specifying if session_user can quote or repost the post, if has already done so,
    the reason why it may be restricted to do so or if the post is a reply to another post.
    """
    can_quote_post: Optional[bool] = Field(None, description="Wether session_user can quote the post or not.")
    can_repost: Optional[bool] = Field(None, description="Wether session_user can repost the post or not.")
    is_reposted_by_viewer: Optional[bool] = Field(None, description="Wether session_user has already reposted the post or not.")
    repost_restricted_reason: Optional[bool] = Field(None, description="Reason why session_user can't repost the post.")
    # __typename: str
    reposted_post: Optional[PostForwardRef] = Field(None, description="Post object referencing the reposted post.")
    quoted_post: Optional[PostForwardRef] = Field(None, description="Post object referencing the quoted post.") 

class LinkPreviewAttachment(BaseModel):
    """
    Object containing the metadata such as the url preview of the attached media to a post.
    """
    display_url: str
    favicon_url: Optional[str] = None
    image_url: Optional[str] = Field(description="Url to the image preview / thumbnal")
    title: str = Field(description="Title of the link")
    url: str  

class TextPostAppInfo(BaseModel):
    """
    Object containig all information regarding who can view, share and reply the post, if the post is a reply,
    the restrictions to share or view and the reasons.
    """
    share_info: ShareInfo
    can_reply: Optional[bool] = Field(None, description="Wether session_user can reply to the post or not.")
    is_reply: Optional[bool] = Field(None, description="Wether the post is a reply to another post or not.")
    # hush_info: Optional[bool] = None
    reply_control: Optional[str] = Field(None, description="Who can reply to the post. Can be everyone, accounts_you_follow or mentioned_only.")
    pinned_post_info: Optional[PinnedPostInfo] = None
    link_preview_attachment: Optional[LinkPreviewAttachment] = None
    reply_to_author: Optional[UserIdentifiers] = None
    is_post_unavailable: Optional[bool] = Field(None, description="Wether the post is unavailable or not.")
    post_unavailable_reason: Optional[bool] = Field(None, description="Reason why the post is unavailable. Can be region locked due to copyright in specific regions, etc")
    impression_count: Optional[bool] = Field(None, description="Number of impressions of the post.")

class Caption(BaseModel):
    text: str

class Post(BaseModel):
    user: User  | UserIdentifiers = Field(description="User who posted the thread.")
    accessibility_caption: Optional[str] = Field(None, description="Caption describing the media present in the post if any.")
    image_versions2: Optional[ImageVersions2] = Field(None, description="Image/s previews of the media (if any) in the post. No matter wether is a video or a picture.")
    original_width: Optional[int] = Field(612)
    original_height: Optional[int] = Field(612) 
    code: str = Field(description="Internal code for the post URL. Can be watched in the browser by accessing http://threads.net/t/{code}")
    video_versions: Optional[List[VideoVersions]] = Field(None, description="List of videos in the post if any.")
    carousel_media: Optional[List[CarouselMedia]] = Field(...,description="List of all media present in the post when multiples are present.")
    giphy_media_info: Optional[GiphyMediaInfo] = Field(None, description="Wether the post contains a gif or not.")
    pk: str
    text_post_app_info: TextPostAppInfo
    is_fb_only: Optional[bool] = None
    is_internal_only: Optional[bool] = None
    id: str = Field(description="Internal post ID")
    media_type: int = Field(description="Numeric value stating the type of post. 19 indicates text only")
    has_audio: Optional[bool] = Field(None, description="Wether the post contains a voice note or not (It's null even when there is an audio).")
    audio: Optional[Audio] = Field(None, description="Audio file if present in the post.")
    text_with_entities: Optional[str] = None
    transcription_data: Optional[bool] = None
    caption_is_edited: Optional[bool] = Field(None, description="""Indicates if the text in post has been edited. Seems to be always false even when the post has been edited.
                                              There are no indicators in the webclient of the post being edited neither.""")
    has_liked: Optional[bool] = Field(None, description="States if session_user has already liked the post.")
    is_paid_partnership: Optional[bool] = Field(None, description="States wether the post is an ad or not.")
    like_and_view_counts_disabled: Optional[bool] = Field(None, description="Wether the likes and reach of the post are publicly visible")
    taken_at: int = Field(description="UNIX Timestamp when the post was published.")
    caption: Optional[str] = Field("", description="Text in the post, if any")
    @root_validator(pre=True)
    def unpack_caption(cls, values):
        if values.get("caption", {}) != None:
            if type(values.get('caption', {})) != str:
                text = values.get('caption', {}).get('text')
                values['caption'] = text
            return values
        else:
            values['caption'] = None
            return values
    like_count: int = Field(description="Amount of likes in the post.")
    media_overlay_info: Optional[str] = None

class ThreadItem(BaseModel):
    post: Post
    line_type: str = Field(description="""Type of line drawn next to the post. line indicates that there is a line drawn (when the post has replies). none
                           indicates no line, no replies.""")
    view_replies_cta_string: Optional[str] = Field(description="Text showing the number of replies to the post.")
    # reply_facepile_users: List[ProfilePicFacepileUser] = Field([], description="Preview of profile pic of users who replied to the post.")
    should_show_replies_cta: bool = Field(description="Wether if showing the number of replies on the client.")

# class Header(BaseModel):
#     pass

class Node(BaseModel):
    thread_items: List[ThreadItem]
    thread_type: Optional[str] = None
    # header: Optional[Header] = None
    id: str
    # __typename: str

class PageInfo(BaseModel):
    """
    Data structure that indicates wether there is a next page or not, and the cursors to query the next page.
    Used when querying multiple threads from a user or more responses to a thread.
    """
    has_next_page: bool
    has_previous_page: bool
    end_cursor: Optional[str] = Field(description="Cursor pointing the the last post in the page, useful to query the next batch of posts.")
    start_cursor: Optional[bool] = Field(description="Cursor pointing the the first post in the current batch.")

class Edge(BaseModel):
    node: Node
    cursor: str
    # __typename: str

# class HideLikesSettingData(BaseModel):
#     """
#     Wether the author of the thread decide to hide the likes and views of the post.
#     """
#     hide_like_and_view_counts: bool

class ThreadsData(BaseModel):
    edges: List[Edge]
    page_info: PageInfo
    # hideLikesSettingData: Optional[HideLikesSettingData] = None
    
class Likers(BaseModel):
    likers: List[UserBasicInfo]