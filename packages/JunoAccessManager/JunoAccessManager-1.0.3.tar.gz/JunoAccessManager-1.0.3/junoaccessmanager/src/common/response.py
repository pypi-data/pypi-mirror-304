from typing import Dict, List, Union, Any

import orjson
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_200_OK
from junoaccessmanager.src.apps.controllers.write_log import write_log


class ResponseModel(BaseModel):
    code: int = 200
    msg: str = "success"
    data: Union[List, Dict, None] = None


class CORJSONResponse(ORJSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
        )


class BaseResponse:

    @classmethod
    def ok(cls, user_id: int, code: int = HTTP_200_OK, msg: str = "success", data: Union[List, Dict, None,] = None):
        if user_id != -1:
            write_log(user_id=user_id, content=msg)
        from fastapi.encoders import jsonable_encoder
        try:
            jsonable_encoder(data)
            return {
                "code": code,
                "msg": msg,
                "data": data
            }
        except ValueError as e:
            print(f"解析原始数据失败，{str(e)}")
        return CORJSONResponse(
            content={
                "code": code,
                "msg": msg,
                "data": data
            }
        )

    @classmethod
    def err(cls, user_id: int, code: int = 400, msg: str = "fail", data: Union[List, Dict, None] = None):
        if user_id != -1:
            write_log(user_id=user_id, content=msg)
        return CORJSONResponse(
            content={
                "code": code,
                "msg": msg,
                "data": data
            }
        )


R = BaseResponse
