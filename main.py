from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from routers import categories, incomes, periods
from service.service_exception import ServiceException

app = FastAPI()

@app.exception_handler(ServiceException)
def service_exception_handler(request: Request, exc:ServiceException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(periods.router, prefix="/periods", tags=["periods"])
api_router.include_router(incomes.router, prefix="/incomes", tags=["incomes"])
api_router.include_router(
    categories.router, prefix="/categories", tags=["categories"]
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
