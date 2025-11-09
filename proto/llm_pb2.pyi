from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TextChunk(_message.Message):
    __slots__ = ("content", "order", "is_last")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    content: str
    order: int
    is_last: bool
    def __init__(self, content: _Optional[str] = ..., order: _Optional[int] = ..., is_last: bool = ...) -> None: ...

class ChunkMetadata(_message.Message):
    __slots__ = ("order", "title", "description", "keywords", "topic")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    order: int
    title: str
    description: str
    keywords: _containers.RepeatedScalarFieldContainer[str]
    topic: str
    def __init__(self, order: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., keywords: _Optional[_Iterable[str]] = ..., topic: _Optional[str] = ...) -> None: ...

class GenerateChunkRequest(_message.Message):
    __slots__ = ("model", "chunk", "max_tokens")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    model: str
    chunk: TextChunk
    max_tokens: int
    def __init__(self, model: _Optional[str] = ..., chunk: _Optional[_Union[TextChunk, _Mapping]] = ..., max_tokens: _Optional[int] = ...) -> None: ...

class GenerateChunkResponse(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: ChunkMetadata
    def __init__(self, metadata: _Optional[_Union[ChunkMetadata, _Mapping]] = ...) -> None: ...

class AggregateRequest(_message.Message):
    __slots__ = ("model", "chunk_metadata", "max_tokens")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    CHUNK_METADATA_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    model: str
    chunk_metadata: _containers.RepeatedCompositeFieldContainer[ChunkMetadata]
    max_tokens: int
    def __init__(self, model: _Optional[str] = ..., chunk_metadata: _Optional[_Iterable[_Union[ChunkMetadata, _Mapping]]] = ..., max_tokens: _Optional[int] = ...) -> None: ...

class AggregateResponse(_message.Message):
    __slots__ = ("title", "description", "keywords", "topic")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    keywords: _containers.RepeatedScalarFieldContainer[str]
    topic: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., keywords: _Optional[_Iterable[str]] = ..., topic: _Optional[str] = ...) -> None: ...
