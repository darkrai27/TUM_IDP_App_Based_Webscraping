from pydantic import BaseModel, Field
from typing import List, Optional
from userSchemas import FriendshipStatus, User, UserBase, Image

class ImageVersions2(BaseModel):
    candidates: List[Image]

class VideoVersions(BaseModel):
    pass

class Audio(BaseModel):
    audio_src: str = Field(description="URL to the audio file")
    waveform_data: List[float] = Field(description="List of decimal numbers representing the waveform of the audio")

class CarouselMedia(BaseModel):
    image_versions2: ImageVersions2
    video_versions: Optional[VideoVersions]
    accessibility_caption: Optional[str] = Field(description="Textual description of the media in post")
    has_audio: Optional[bool] = Field(None, description="Wether the post contains a voice note or not (It's null even when there is an audio).")
    original_height: int
    original_width: int
    pk: str
    id: str
    code: Optional[str] = None

class ShareInfo(BaseModel):
    can_quote_post: Optional[bool] = None
    can_repost: bool
    is_reposted_by_viewer: bool
    repost_restricted_reason: Optional[bool] = None
    # __typename: str
    reposted_post: Optional[bool] = None
    quoted_post: Optional[bool] = None

class TextPostAppInfo(BaseModel):
    share_info: ShareInfo
    can_reply: bool
    is_reply: bool
    hush_info: Optional[bool] = None
    reply_control: str
    pinned_post_info: Optional[bool] = None
    link_preview_attachment: Optional[bool] = None
    reply_to_author: Optional[UserBase] = None
    is_post_unavailable: bool
    post_unavailable_reason: Optional[bool] = None
    impression_count: Optional[bool] = None

class Caption(BaseModel):
    text: str

class Post(BaseModel):
    user: User
    accessibility_caption: Optional[str] = Field(None, description="Caption describing the media present in the post if any.")
    original_height: Optional[int] = Field(612) 
    original_width: Optional[int] = Field(612)
    image_versions2: ImageVersions2
    code: str = Field(description="Internal code for the post URL. Can be watched in the browser by accessing http://threads.net/t/{code}")
    video_versions: Optional[VideoVersions] = None
    carousel_media: Optional[List[CarouselMedia]] = Field(...,description="List of all media present in the post.")
    giphy_media_info: Optional[bool] = None
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
    caption_is_edited: Optional[bool] = Field(None, description="Indicates if the text in posat has been edited.")
    has_liked: bool = Field(description="States if the user has already liked the post.")
    is_paid_partnership: Optional[bool] = Field(None, description="States wether the post is an ad or not.")
    like_and_view_counts_disabled: bool = Field(description="Wether the likes and reach of the post are publicly visible")
    taken_at: int = Field(description="Timestamp when the thread was posted.")
    caption: Optional[Caption] = Field(None, description="Text in the post, if any")
    like_count: int = Field(description="Amount of likes in the post.")
    media_overlay_info: Optional[bool]

class ReplyFacepileUsers(BaseModel):
    pass

class ThreadItems(BaseModel):
    post: Post
    line_type: str
    view_replies_cta_string: Optional[str] = None
    reply_facepile_users: List[ReplyFacepileUsers]
    should_show_replies_cta: bool

class Header(BaseModel):
    pass

class Node(BaseModel):
    thread_items: List[ThreadItems]
    thread_type: Optional[str] = None
    header: Optional[Header] = None
    id: str
    # __typename: str

class PageInfo(BaseModel):
    has_next_page: bool
    has_previous_page: bool
    end_cursor: Optional[bool] = None
    start_cursor: Optional[bool] = None

class Edge(BaseModel):
    node: Node
    cursor: str

class ThreadsData(BaseModel):
    edges: List[Edge]
    page_info: PageInfo

class HideLikesSettingData(BaseModel):
    hide_like_and_view_counts: bool

class WrapperData(BaseModel):
    data: ThreadsData
    hideLikesSettingData: HideLikesSettingData

class Extensions(BaseModel):
    is_final: bool

class JsonPosts(BaseModel):
    data: WrapperData
    extensions: Extensions
