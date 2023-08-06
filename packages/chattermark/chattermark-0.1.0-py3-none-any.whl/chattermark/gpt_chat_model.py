from typing import Any, Dict, List, NewType, Optional

from pydantic import BaseModel


MetaData = NewType("MetaData", Dict[str, Any])


class Author(BaseModel):
    role: str
    metadata: MetaData


class Content(BaseModel):
    content_type: str
    parts: List[str]


class Message(BaseModel):
    id: str
    author: Author
    create_time: float
    content: Content
    weight: float
    metadata: MetaData
    recipient: str


class Node(BaseModel):
    id: str
    message: Optional[Message] = None
    parent: Optional[str] = None
    children: List[str]


class GPTChatSession(BaseModel):
    title: str
    create_time: float
    update_time: float
    mapping: Dict[str, Node]
