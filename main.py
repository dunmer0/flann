from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import categories, category_names, expenses, incomes, periods
from service.service_exception import ServiceException

app = FastAPI()

# origins = [
#     "http://localhost:4200"
# ]


app.add_middleware(
    CORSMiddleware,  # type: ignore  # False positive from type checker
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ServiceException)
def service_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(status_code=404, content={"detail": exc.message})


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(periods.router, prefix="/periods", tags=["periods"])
api_router.include_router(incomes.router, prefix="/incomes", tags=["incomes"])
api_router.include_router(
    category_names.router, prefix="/category-names", tags=["category_names"]
)
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])

app.include_router(api_router)
