from fastapi import APIRouter

from src.api.v1.document.delete import router as delete_router
from src.api.v1.document.list import router as list_router
from src.api.v1.document.upload import router as upload_router

router = APIRouter()
router.include_router(upload_router)
router.include_router(list_router)
router.include_router(delete_router)
