from fastapi import APIRouter

router = APIRouter()


@router.get("", summary="Health check")
def health():
    return {"status": "ok"}
