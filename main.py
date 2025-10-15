from fastapi import APIRouter, FastAPI

from routers import periods, incomes

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(periods.router, prefix="/periods", tags=["periods"])
api_router.include_router(incomes.router, prefix="/incomes", tags=["incomes"])

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
