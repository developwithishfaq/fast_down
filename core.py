from pydantic import BaseModel


def returnData(success: bool, msg: str,data):
    return {
        "success": success,
        "message": msg,
        "data": data
    }