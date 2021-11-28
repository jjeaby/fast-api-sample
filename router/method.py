from typing import Optional

from fastapi import APIRouter
from fastapi import Depends, Query, Path
from pydantic.fields import Field
from pydantic.main import BaseModel
from starlette.responses import JSONResponse

router = APIRouter()

"""
    swagger documentation by pydantic example
    POST/GET Method example
"""


# Request
class ItemGetReq(BaseModel):
    """
        Request Spec
        - item_id is a PathString
        - q is a QueryString
    """
    item_id: int = Path(None, title='item id value')
    q: Optional[str] = Query(None, title='query text')


# Response
class ItemGetRes(BaseModel):
    """
        Response Spec
        - Json Type
    """
    item_id: int = Field(None, title='item id value')
    q: Optional[str] = Field(None, title='query text')


@router.get("/item/{item_id}",
            name="Rest Api For GET sample",
            description="Rest Api GET Method Sample End Point",
            response_model=ItemGetRes
            )
def get_item(item_get_req: ItemGetReq = Depends(ItemGetReq)):
    request_json = dict(item_get_req)
    item_post_res = ItemPostRes(**request_json)
    return item_post_res


# Request
class ItemPostReq(BaseModel):
    """
        Request Spec
        - Json Type
    """
    item_id: int = Field(None, title='item id value')
    q: Optional[str] = Field(None, title='query text')


# Response
class ItemPostRes(BaseModel):
    """
        Response Spec
        - Json Type

    """
    item_id: int = Field(None, title='item id value')
    q: Optional[str] = Field(None, title='query text')


@router.post("/item",
             name="Rest Api For Post sample",
             description="Rest Api Post Method Sample End Point",
             response_model=ItemPostRes
             )
def post_item(item_post_req: ItemPostReq):
    request_json = dict(item_post_req)

    items_post_res = ItemPostRes(**request_json)
    return JSONResponse(items_post_res.dict())
