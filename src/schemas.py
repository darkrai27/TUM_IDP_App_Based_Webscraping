from pydantic import BaseModel, Field
from typing import List, Optional

class HdProfilePicVersion(BaseModel):
    height: int = Field(..., description="The height of the profile picture.")
    url: str = Field(..., description="The URL of the profile picture.")
    width: int = Field(..., description="The width of the profile picture.")

class FriendshipStatus(BaseModel):
    following: bool = Field(..., description="Whether the user is following the account.")
    outgoing_request: bool = Field(..., description="Whether there's an outgoing follow request.")
    followed_by: bool = Field(..., description="Whether the user is followed by the account.")
    is_restricted: Optional[bool] = Field(None, description="Whether the user has restricted this account.")
    blocking: Optional[bool] = Field(None, description="Whether the user has blocked this account.")
    muting: Optional[bool] = Field(None, description="Whether the user has muted this account.")
    incoming_request: Optional[bool] = Field(None, description="Whether there's an incoming follow request.")

class BiographyWithEntities(BaseModel):
    entities: List[str] = Field([], description="List of entities mentioned in the biography.")
    raw_text: str = Field(..., description="The raw text of the biography.")

class User(BaseModel):
    pk: int = Field(..., description="The primary key - unique internal numeric identifier - of the user.")
    username: str = Field(..., description="The username of the account. Is unique and inherited from the instagram account."
                          "Limited to 30 characters, must only contain letters in lowercase, numbers, periods, and underscores.")
    hd_profile_pic_versions: List[HdProfilePicVersion] = Field(..., description="List of HD profile pictures with dimensions.")
    profile_pic_url: str = Field(..., description="The URL of the profile picture.")
    biography: str = Field(..., description="A short description of the user or its acccount.")
    biography_with_entities: BiographyWithEntities = Field(..., description="Biography with entities.")
    follower_count: int = Field(..., description="The number of followers.")
    profile_context_facepile_users: List[str] = Field([], description="...")
    text_post_app_is_private: bool = Field(..., description="Whether the profile is private (its posts can only be seen by accepted folowers) or not")
    friendship_status: FriendshipStatus = Field(..., description="Defines the friendship status among the logged account and the profile queried.")
    full_name: str = Field(..., description="The full name of the user. Limited to 30 characters, must only contain"
                           "letters, numbers, periods, underscores and spaces.")
    is_verified: bool = Field(..., description="Whether the user is verified.")
    account_badges: Optional[List[str]] = Field([], description="List of account badges.")
    bio_links: Optional[List[dict]] = Field([], description="List of links in the user biography.")
    transparency_label: Optional[dict] = Field(None, description="Transparency label.")
    text_post_app_remove_mention_entrypoint: Optional[bool] = Field(None, description="Whether to remove the mention entry point.")

class UserData(BaseModel):
    user: User

class Data(BaseModel):
    userData: UserData

class Extensions(BaseModel):
    is_final: bool = Field(..., description="...")

class Json1(BaseModel):
    data: Data
    extensions: Extensions

class Data2(BaseModel):
    xdt_user_by_username: User

class Json2(BaseModel):
    data: Data2
    extensions: Extensions
