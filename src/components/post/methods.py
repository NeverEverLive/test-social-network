import logging
from typing import List
import itertools as it
import uuid
import json

from sqlalchemy import select, update, delete
from pydantic import parse_obj_as

from src.exceptions.post import PostNotExistException, PostPermissionException, PostException
from src.models.postgres.post import PostModel
from src.models.postgres.base import get_session as postgres_session
from src.models.redis.base import get_session as redis_sesssion
from src.components.post.schemas import PostSchema, PostResponse, PostsResponse


async def create_post(post: PostSchema, user_id: str) -> PostResponse:
    """Create post.
    :type post: PostSchema
    :param post: Post data
    :return: Created post with user
    """
    post.user_id = user_id
    post_query = PostModel().fill(**post.dict())
    
    with postgres_session() as session:
        session.add(post_query)
        session.commit()
    
    return PostResponse(
        post=post,
        user_id=user_id,
        message="Post successfully created",
        success=True
        )


async def get_posts() -> PostsResponse:
    """Get posts.
    :return: PostsResponse with all posts
    """
    post_state = select(
        PostModel
    )

    with postgres_session() as session:
        return PostsResponse(
            posts=parse_obj_as(List[PostSchema], list(it.chain(*session.execute(post_state).fetchall()))),
            message="Posts collected successfully",
            success=True
        )

async def get_posts_by_user(_id: str) -> PostsResponse:
    """Get posts.
    :return: PostsResponse with all posts sorted by user
    """
    post_state = select(
        PostModel
    ).where(
        PostModel.user_id == _id
    )

    with postgres_session() as session:
        return PostsResponse(
            posts=parse_obj_as(List[PostSchema], list(it.chain(*session.execute(post_state).fetchall()))),
            message="Posts collected successfully",
            success=True
        )

async def get_post(_id: str) -> PostsResponse:
    """Get post.
    :return: PostResponse with one post
    """
    post_state = select(
        PostModel
    ).where(
        PostModel.id == _id
    )

    with postgres_session() as session:
        if post := session.execute(post_state).fetchone():
            return PostResponse(
                post=post[0],
                message="Post successfully received",
                success=True
            )
        raise PostNotExistException(
            status_code=404,
            message="This post doesn't exist"
        )

async def update_post(post: PostSchema, user_id: uuid.UUID) -> PostResponse:
    """Update post.
    :type post: PostSchema
    :param post: Updated post data
    :return: PostResponse with updated post instance
    """
    if user_id != post.user_id:
        raise PostPermissionException(
            message="This is not your post",
            status_code=403
        )

    post_state = update(
        PostModel
    ).where(
        PostModel.id == post.id
    ).values(
        **post.dict(exclude={"like", "dislike"})
    )

    with postgres_session() as session:
        session.execute(post_state)
        session.commit()

    return PostResponse(
        post=post,
        message="Post successfully updated",
        success=True
    )


async def delete_post(post_id: str, user_id: str) -> PostResponse:
    """Delete post.
    :type id: str
    :param id: Post id
    :return: PostResponse with message about operation
    """
    permision_state = select(
        PostModel
    ).where(
        PostModel.id == post_id,
        PostModel.user_id == user_id,
    )

    with postgres_session() as session:
        posts = session.execute(permision_state)
        
    if not posts:
        raise PostPermissionException(
            message="This is not your post",
            status_code=403
        )

    post_state = delete(
        PostModel
    ).where(
        PostModel.id == post_id
    )

    with postgres_session() as session:
        session.execute(post_state)
        session.commit()

    session = redis_sesssion()
    await session.delete(post_id.encode("utf-8"))

    return PostResponse(
        message="Post successfully deleted",
        success=True
    )


async def rate_post(_id: str, like: bool, dislike: bool, user_id: str):
    if not (_id and (like or dislike)):
        raise PostException(
                status_code=400,
                message="You must provide post id and like or dislike"
            )

    if like and dislike:
        raise PostException(
                status_code=400,
                message="You must provide only like or dislike"
            )

    post_state = select(
        PostModel
    ).where(
        PostModel.id == _id
    )

    with postgres_session() as session:
        if not (post := session.execute(post_state).fetchone()):
            raise PostNotExistException(
                status_code=404,
                message="This post doesn't exist"
            )
        
    if post[0].user_id == user_id:
        raise PostException(
            message="You can't like your posts"
        )

    session = await redis_sesssion()

    logging.warning(await session.get(_id))
    if stats := await session.get(_id):
        stats = json.loads(stats.decode("utf-8"))
        stats["likes"] += int(like)
        stats["dislikes"] += int(dislike)
    else:
        stats = {
            "likes": int(like),
            "dislikes": int(dislike)
        }
    
    await session.set(_id, json.dumps(stats).encode("utf-8"))
    await session.close()

    return PostResponse(
        message="Post reated",
        success=True
    )
