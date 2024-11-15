from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.notes as crud
from src.auth.jwthandler import get_current_user
from src.schemas.notes import NoteOutSchema, NoteInSchema, UpdateNote
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


# 创建一个 FastAPI 路由对象
router = APIRouter()


# 定义一个 GET 请求处理函数，用于获取所有笔记
@router.get(
    "/notes",
    response_model=List[NoteOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_notes():
    """
    获取所有笔记。

    返回:
        一个包含所有笔记的列表。

    异常:
        HTTPException: 如果没有找到笔记，抛出 404 错误。
    """
    return await crud.get_notes()


# 定义一个 GET 请求处理函数，用于获取指定 ID 的笔记
@router.get(
    "/note/{note_id}",
    response_model=NoteOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_note(note_id: int) -> NoteOutSchema:
    """
    根据 ID 获取单个笔记。

    参数:
        note_id (int): 要获取的笔记 ID。

    返回:
        NoteOutSchema: 获取到的笔记信息。

    异常:
        HTTPException: 如果没有找到指定 ID 的笔记，抛出 404 错误。
    """
    try:
        return await crud.get_note(note_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Note does not exist",
        )


# 定义一个 POST 请求处理函数，用于创建新笔记
@router.post(
    "/notes", response_model=NoteOutSchema, dependencies=[Depends(get_current_user)]
)
async def create_note(
    note: NoteInSchema, current_user: UserOutSchema = Depends(get_current_user)
) -> NoteOutSchema:
    """
    创建一个新笔记。

    参数:
        note (NoteInSchema): 包含笔记信息的 Pydantic 模型。
        current_user (UserOutSchema): 当前登录的用户信息。

    返回:
        NoteOutSchema: 创建成功的笔记信息。

    异常:
        HTTPException: 如果创建笔记失败，抛出 400 错误。
    """
    return await crud.create_note(note, current_user)


# 定义一个 PATCH 请求处理函数，用于更新指定 ID 的笔记
@router.patch(
    "/note/{note_id}",
    dependencies=[Depends(get_current_user)],
    response_model=NoteOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_note(
    note_id: int,
    note: UpdateNote,
    current_user: UserOutSchema = Depends(get_current_user),
) -> NoteOutSchema:
    """
    更新指定 ID 的笔记。

    参数:
        note_id (int): 要更新的笔记 ID。
        note (UpdateNote): 包含更新信息的 Pydantic 模型。
        current_user (UserOutSchema): 当前登录的用户信息。

    返回:
        NoteOutSchema: 更新后的笔记信息。

    异常:
        HTTPException: 如果没有找到指定 ID 的笔记，抛出 404 错误。
        HTTPException: 如果当前用户没有权限更新笔记，抛出 403 错误。
    """
    return await crud.update_note(note_id, note, current_user)


# 定义一个 DELETE 请求处理函数，用于删除指定 ID 的笔记
@router.delete(
    "/note/{note_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_note(
    note_id: int, current_user: UserOutSchema = Depends(get_current_user)
):
    """
    删除指定 ID 的笔记。

    参数:
        note_id (int): 要删除的笔记 ID。
        current_user (UserOutSchema): 当前登录的用户信息。

    返回:
        Status: 删除操作的状态信息。

    异常:
        HTTPException: 如果没有找到指定 ID 的笔记，抛出 404 错误。
        HTTPException: 如果当前用户没有权限删除笔记，抛出 403 错误。
    """
    return await crud.delete_note(note_id, current_user)
