from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .congress_members import router as congress_members_router
from .bills import router as bills_router
from .votes import router as votes_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(congress_members_router, prefix="/congress-members", tags=["congress_members"])
api_router.include_router(bills_router, prefix="/bills", tags=["bills"])
api_router.include_router(votes_router, prefix="/votes", tags=["votes"])