from fastapi import APIRouter
from .empa import empa 
from .empb import empb
from .empc import empc
from .empd import empd

router = APIRouter()

router.include_router(empa)
router.include_router(empb)
router.include_router(empc)
router.include_router(empd)