from pydantic import BaseModel
from typing import Literal, Union


# Telegram Response

class getMe(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    can_join_groups: bool
    can_read_all_group_messages: bool
    supports_inline_queries: bool

class TelegramgetMeResponse(BaseModel):
    ok: bool
    result: getMe

# Telegram Payload

class TelegramMessage(BaseModel):
    chat_id: int
    text: str
    parse_mode: Literal['HTML', 'MarkdownV2'] = "HTML"

class TelegramPhoto(BaseModel):
    chat_id: int
    photo: str
    caption: Union[str, None]

class TelegramDocument(BaseModel):
    chat_id: int
    document: str
    caption: Union[str, None]

class TelegramAudio(BaseModel):
    chat_id: int
    audio: str
    caption: Union[str, None]

class TelegramVideo(BaseModel):
    chat_id: int
    video: str
    caption: Union[str, None]

class TelegramPoll(BaseModel):
    chat_id: int
    question: str
    options: object