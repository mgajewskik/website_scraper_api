from fastapi import HTTPException


def raise_not_found(msg: str = "Website not found."):
    raise HTTPException(status_code=404, detail=msg)


def raise_unprocessable_entity(msg: str = "Unprocessable entity."):
    raise HTTPException(status_code=422, detail=msg)


def raise_bad_request(msg: str = "Bad request."):
    raise HTTPException(status_code=400, detail=msg)
