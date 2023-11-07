from pydantic import BaseModel, Field
from typing import List, Optional

class Image(BaseModel):
    height: Optional[int] = Field(None, description="The height of the profile picture.")
    url: Optional[str] = Field(..., description="The URL of the profile picture.")
    width: Optional[int] = Field(None, description="The width of the profile picture.")

class FriendshipStatus(BaseModel):
    following: Optional[bool] = Field(..., description="Whether the user is following the account.")
    blocking: Optional[bool] = Field(None, description="Whether the user has blocked this account.")
    muting: Optional[bool] = Field(None, description="Whether the user has muted this account.")

class FriendShipStatusComplete(FriendshipStatus):
    outgoing_request: Optional[bool] = Field(description="Whether there's an outgoing follow request.")
    followed_by: Optional[bool] = Field(description="Whether the user is followed by the account.")
    is_restricted: Optional[bool] = Field(None, description="Whether the user has restricted this account.")
    incoming_request: Optional[bool] = Field(None, description="Whether there's an incoming follow request.")

class BiographyWithEntities(BaseModel):
    entities: List[str] = Field([], description="List of entities mentioned in the biography.")
    raw_text: str = Field(..., description="The raw text of the biography.")

class BioLink(BaseModel):
    url: str = Field(description="Url contained in user's biography")

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
    friendship_status: FriendshipStatus = Field(..., description="Defines the friendship status among the logged account and the profile queried.")
    profile_pic_url: str = Field(..., description="The URL of the profile picture.")
    is_verified: bool = Field(..., description="Whether the user is verified.")
    text_post_app_is_private: bool = Field(..., description="Whether the profile is private (its posts can only be seen by accepted folowers) or not")
    transparency_label: Optional[dict] = Field(None, description="Transparency label.")
    transparency_product: Optional[bool] = None
    transparency_product_enabled: Optional[bool] = None
    text_post_app_has_max_posts_pinned_to_profile: Optional[bool] = None

class UserComplete(User):
    '''
    Complete user information collected when querying a user profile. This includes more data s.a. biography, followers count, etc.
    '''
    hd_profile_pic_versions: List[Image] = Field(..., description="List of HD profile pictures with dimensions.")
    biography: str = Field(..., description="A short description of the user or its acccount.")
    biography_with_entities: BiographyWithEntities = Field(..., description="Biography with entities.")
    follower_count: int = Field(..., description="The number of followers.")
    profile_context_facepile_users: List[str] = Field([], description="...")
    full_name: str = Field(..., description="The full name of the user. Limited to 30 characters, must only contain"
                           "letters, numbers, periods, underscores and spaces.")
    account_badges: Optional[List[str]] = Field([], description="List of account badges.")
    bio_links: Optional[List[dict]] = Field([], description="List of links in the user biography.")
    text_post_app_remove_mention_entrypoint: Optional[bool] = Field(None, description="Whether to remove the mention entry point.")


class UserData(BaseModel):
    """Wrapper Object"""
    user: User

class Data(BaseModel):
    userData: UserData

class Extensions(BaseModel):
    is_final: bool = Field(..., description="...")

class Json1(BaseModel):
    data: Data
    extensions: Extensions

class Data2(BaseModel):
    xdt_user_by_username: UserComplete

class Json2(BaseModel):
    data: Data2
    extensions: Extensions


class UserFollowsData(BaseModel):
    username: str
    pk: str
    id: str

class FollowsCounts(BaseModel):
    total_followers_count: int
    total_following_count: int
    total_pending_follow_count: Optional[int]

class FollowsData(BaseModel):
    user: UserFollowsData
    counts: FollowsCounts

class FollowsInfo(BaseModel):
    data: FollowsData
    extensions: Extensions
