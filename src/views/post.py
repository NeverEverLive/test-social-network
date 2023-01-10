import logging
from fastapi import APIRouter, Query, Depends, Request

from src.components.post.schemas import PostSchema, PostResponse, PostsResponse
from src.components.post.methods import create_post
from src.components.post.methods import get_posts
from src.components.post.methods import get_posts_by_user
from src.components.post.methods import get_post
from src.components.post.methods import update_post
from src.components.post.methods import delete_post
from src.components.post.methods import rate_post
from src.components.base_response.schema import BaseResponse
from src.models.redis.base import get_session

from src.components.auth.jwt import JWTBearer

router = APIRouter(prefix="/posts")


@router.post("/", response_model=PostResponse, status_code=201, dependencies=[Depends(JWTBearer())])
async def create_post_endpoint(user: PostSchema, request: Request):
    return await create_post(user, request.state.user_id)


@router.get("/", response_model=PostsResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_posts_endpoint():
    return await get_posts()


@router.get("/by/user_id/{user_id}", response_model=PostsResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_posts_by_user_endpoint(user_id: str):
    return await get_posts_by_user(user_id)


@router.get("/by/post_id/{post_id}", response_model=PostResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def get_post_endpoint(post_id: str):
    return await get_post(post_id)


@router.put("/", response_model=PostResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def update_post_endpoint(post: PostSchema, request: Request):
    return await update_post(post, request.state.user_id)


@router.delete("/", response_model=PostResponse, status_code=202, dependencies=[Depends(JWTBearer())])
async def delete_post_endpoint(request: Request, post_id: str = Query(alias="id")):
    return await delete_post(post_id, request.state.user_id)


@router.patch("/", response_model=PostResponse, status_code=200, dependencies=[Depends(JWTBearer())])
async def update_post_endpoint(
        request: Request,
        _id: str = Query(alias="id"), 
        like: bool = Query(default=False), 
        dislike: bool = Query(default=False)
    ):
    return await rate_post(_id, like, dislike, request.state.user_id)
