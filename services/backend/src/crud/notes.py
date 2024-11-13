from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Notes
from src.schemas.notes import NoteOutSchema
from src.schemas.token import Status  # NEW


async def get_notes():
    """
    获取所有笔记。

    返回:
        一个包含所有笔记的列表。

    异常:
        HTTPException: 如果没有找到笔记，抛出 404 错误。
    """
    return await NoteOutSchema.from_queryset(Notes.all())


async def get_note(note_id) -> NoteOutSchema:
    """
    根据 ID 获取单个笔记。

    参数:
        note_id (int): 要获取的笔记 ID。

    返回:
        NoteOutSchema: 获取到的笔记信息。

    异常:
        HTTPException: 如果没有找到指定 ID 的笔记，抛出 404 错误。
    """
    return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))


async def create_note(note, current_user) -> NoteOutSchema:
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
    note_dict = note.dict(exclude_unset=True)
    note_dict["author_id"] = current_user.id
    note_obj = await Notes.create(**note_dict)
    return await NoteOutSchema.from_tortoise_orm(note_obj)


async def update_note(note_id, note, current_user) -> NoteOutSchema:
    """
    更新指定 ID 的笔记。

    参数:
        note_id (int): 要更新的笔记 ID。
        note (NoteInSchema): 包含更新信息的 Pydantic 模型。
        current_user (UserOutSchema): 当前登录的用户信息。

    返回:
        NoteOutSchema: 更新后的笔记信息。

    异常:
        HTTPException: 如果没有找到指定 ID 的笔记，抛出 404 错误。
        HTTPException: 如果当前用户没有权限更新笔记，抛出 403 错误。
    """
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    if db_note.author.id == current_user.id:
        await Notes.filter(id=note_id).update(**note.dict(exclude_unset=True))
        return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_note(note_id, current_user) -> Status:  # UPDATED
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
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    if db_note.author.id == current_user.id:
        deleted_count = await Notes.filter(id=note_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
        return Status(message=f"Deleted note {note_id}")  # UPDATED

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
