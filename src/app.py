import json
import logging
import psutil
import os

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from src.exceptions.authentication import AuthenticationException
from src.exceptions.user import UserException
from src.exceptions.post import PostException
from src.models.postgres.base import get_session as postgrse_session
from src.models.redis.base import get_session as redis_session
from src.views.health import router as health_router
from src.views.user import router as user_router
from src.views.post import router as posts_router

def create_app():
    app = FastAPI(title="Studing ticket", debug=False)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    @repeat_every(seconds=10)
    async def merge_chache() -> None:
        parent_process = psutil.Process(os.getppid())
        children = parent_process.children(recursive=True)
        logging.warning(children[0].pid)
        logging.warning(os.getpid())
        if children[1].pid == os.getpid():
            logging.warning("MERGE")
            session = await redis_session()
            async for key in session.scan_iter():
                logging.warning(key)
                value = await session.get(key)
                value = json.loads(value.decode("utf-8"))
                with postgrse_session() as postgres_session:
                    logging.warning("UPDATE")
                    postgres_session.execute(f"""
                    UPDATE post
                    SET "like" = "like" + {value["likes"]},
                    "dislike" = "dislike" + {value["dislikes"]}
                    WHERE "id" = '{key.decode("utf-8")}';""")
                    postgres_session.commit()
                logging.warning("DELETE")
                logging.warning(type(key))
                await session.delete(key)
            logging.warning("END")

    @app.exception_handler(AuthenticationException)
    async def authentication_exception_handler(request: Request, exc: AuthenticationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(UserException)
    async def user_exception_handler(request: Request, exc: UserException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(PostException)
    async def post_exception_handler(request: Request, exc: PostException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
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

    app.include_router(
        user_router,
        prefix="/api",
        tags=["User"]
    )

    app.include_router(
        posts_router,
        prefix="/api",
        tags=["Posts"]
    )

    return app
