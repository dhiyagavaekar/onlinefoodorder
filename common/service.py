
from fastapi import Response
from typing import Optional
from fastapi import Response, status
from fastapi.responses import JSONResponse
from typing import Optional
from .message import message



def responseSend(res: Response, code: Optional[int] = None, msg: Optional[str] = None, data: Optional[dict] = None, count: Optional[int] = None):
    try:
        result = {}
        n_code = code or 455
        m = message.get(n_code)

        result["success"] = m["status"] if m else n_code
        result["message"] = msg or m.get("message", "Unknown error")
        result["data"] = data
        if count:
            result["count"] = count

        http_code = m["httpCode"] if m else 280
        return JSONResponse(status_code=http_code, content=result)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"success": False, "message": f"Failure while encrypting data: {str(e)}"})

