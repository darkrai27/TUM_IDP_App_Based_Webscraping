from pydantic import BaseModel, Field
from typing import List, Optional, ForwardRef

from threadscraper.mediaSchemas import Image

class FriendshipStatus(BaseModel):
    is_restricted: Optional[bool] = Field(None, description="Whether the session_user has restricted this account.")
    blocking: Optional[bool] = Field(None, description="Whether the session_user has blocked this account.")
    muting: Optional[bool] = Field(None, description="Whether the session_user has muted this account.")
    followed_by: Optional[bool] = Field(None, description="Whether the session_user is followed by the account.")
    following: bool = Field(..., description="Whether the session_user is following the account.")
    incoming_request: Optional[bool] = Field(None, description="Whether there's an incoming follow request.")
    outgoing_request: Optional[bool] = Field(None,description="Whether there's an outgoing follow request.")

UserBaserForwardRef = ForwardRef("UserBase")

class BiographyWithEntities(BaseModel):
    """
    Data structure containing all the information about the biography and a reference to the users mentioned in it.
    """
    entities: List[UserBaserForwardRef] = Field([], description="List of entities (users) mentioned in the biography.")
    raw_text: str = Field(..., description="The raw text of the biography.")

class BioLink(BaseModel):
    url: str = Field(description="Url contained in user's biography")

# class ProfilePicFacepileUser(BaseModel):
#     """
#     Profile pic of facepile users. Thumbnail of profile pics of accounts following that also follow this account
#     """
#     profile_pic_url: str
#     id: Optional[str] = None

class UserBase(BaseModel):
    '''
    User basic identifiers present in different queries results.
    '''
    id: Optional[int] = Field(..., description="Same values as pk, optioanl -> Not always present.")
    username: str = Field(..., description="The username of the account. Is unique and inherited from the instagram account."
                          "Limited to 30 characters, must only contain letters in lowercase, numbers, periods, and underscores.")

class User(UserBase):
    '''
    Basic users information present in different queries.
    '''
    pk: int = Field(..., description="The primary key - unique internal numeric identifier - of the user.")
    hd_profile_pic_versions: Optional[List[Image]] = Field(None, description="List of HD profile pictures with dimensions.")
    profile_pic_url: str = Field(None, description="The URL of the profile picture.")
    biography: Optional[str] = Field(None, description="Customizable text. Used to describe the user or its account.")
    friendship_status: FriendshipStatus | None = Field(None, description="Defines the friendship status among the logged account and the profile queried.")
    biography_with_entities: Optional[BiographyWithEntities] = Field(None, description="Biography with entities.")
    follower_count: Optional[int] = Field(None, description="The number of followers.")
    # profile_context_facepile_users: Optional[List[ProfilePicFacepileUser]] = []
    account_badges: Optional[List[str]] = Field([], description="List of account badges.")
    bio_links: Optional[List[dict]] = Field([], description="List of links in the user biography.")
    text_post_app_is_private: bool = Field(None, description="Whether the profile is private (its posts can only be seen by accepted folowers) or not")
    transparency_label: Optional[dict] = Field(None, description="Transparency label.")
    full_name: Optional[str] = Field(None, description="The full name of the user. Limited to 30 characters, must only contain"
                           "letters, numbers, periods, underscores and spaces.")
    # text_post_app_remove_mention_entrypoint: Optional[bool] = Field(None, description="Whether to remove the mention entry point.")
    transparency_product: Optional[bool] = None
    transparency_product_enabled: Optional[bool] = None
    text_post_app_has_max_posts_pinned_to_profile: Optional[bool] = Field(None, description="Wether the account has reached the maximum of pinned posts in its profile.")
    is_verified: bool = Field(..., description="Whether the account is verified.")

class FollowsCounts(BaseModel):
    """
    Data structure containing the amount of followers, following and pending follow requests of a user.
    """
    total_followers_count: int
    total_following_count: int
    total_pending_follow_count: Optional[int]
