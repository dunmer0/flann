from fastapi import FastAPI, APIRouter
from routers import periods

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(periods.router, prefix="/periods", tags=["periods"])

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
