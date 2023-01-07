from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.views.health import router as health_router
from src import models

def create_app():
    app = FastAPI(title="Studing ticket", debug=False)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": str(exc)},
        )

    app.include_router(
        health_router,
        prefix="/api",
        tags=["Health check"]
    )

    return app
