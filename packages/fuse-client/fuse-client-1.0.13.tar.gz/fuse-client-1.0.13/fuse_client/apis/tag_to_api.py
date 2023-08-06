import typing_extensions

from fuse_client.apis.tags import TagValues
from fuse_client.apis.tags.fuse_api import FuseApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.FUSE: FuseApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.FUSE: FuseApi,
    }
)
