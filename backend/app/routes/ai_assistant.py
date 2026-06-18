from fastapi import APIRouter

router = APIRouter(
    tags=["AI Assistant"]
)


@router.get("/assistant")
def assistant():

    return {
        "message":
        "GridLock AI Assistant Active"
    }