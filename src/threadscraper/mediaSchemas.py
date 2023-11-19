from pydantic import BaseModel, Field
from typing import List, Optional

class Image(BaseModel):
    height: Optional[int] = Field(None, description="The height of the profile picture.")
    url: Optional[str] = Field(..., description="The URL of the profile picture.")
    width: Optional[int] = Field(None, description="The width of the profile picture.")

class ImageVersions2(BaseModel):
    candidates: List[Image] = Field(description="List of candidates as media previews/thumbnails")

class VideoVersions(BaseModel):
    """
    Data structure containing the information of the video (if any) in the post.
    """
    type: int =  Field(None, description="Numeric value stating the type of video. 101,102 and 103 seem equivalent.")
    url: str = Field(None, description="URL to the video file")

class Audio(BaseModel):
    audio_src: str = Field(description="URL to the audio file")
    waveform_data: List[float] = Field(description="List of decimal numbers representing the waveform of the audio")

class CarouselMedia(BaseModel):
    image_versions2: ImageVersions2
    video_versions: Optional[List[VideoVersions]] = None
    accessibility_caption: Optional[str] = Field(description="Textual description of the media in post")
    has_audio: Optional[bool] = Field(None, description="Wether the post contains a voice note or not (It's null even when there is an audio).")
    original_height: int
    original_width: int
    pk: str
    id: str
    code: Optional[str] = None