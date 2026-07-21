from typing import List, Optional
from sqlalchemy import func, or_
from sqlmodel import SQLModel, asc, desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from models import Item, ItemCreate, ItemUpdate


async def create_item(session: AsyncSession, item_data: ItemCreate) -> Item:
    """
    Creates a new item record.
    :param session: AsyncSession instance
    :param item_data: ItemCreate schema
    :return: created Item instance
    """
    item = Item.model_validate(item_data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def get_item(session: AsyncSession, item_id: int) -> Optional[Item]:
    """
    Retrieves an item by ID.
    :param session: AsyncSession instance
    :param item_id: item ID
    :return: Item or None
    """
    return await session.get(Item, item_id)


async def get_items(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    owner_id: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc"
) -> List[Item]:
    """
    Retrieves list of items with filtering, search, sorting (asc/desc), and pagination.
    :param session: AsyncSession instance
    :param skip: offset
    :param limit: maximum records
    :param title: optional search query
    :param owner_id: optional owner filter
    :param sort_by: optional field to sort by (e.g. price, title, or -price)
    :param sort_order: sort direction 'asc' or 'desc'
    :return: list of Item objects
    """
    statement = select(Item)

    if title:
        search_pattern = f"%{title.lower()}%"
        statement = statement.where(
            or_(
                func.lower(Item.title).like(search_pattern),
                func.lower(Item.description).like(search_pattern)
            )
        )

    if owner_id is not None:
        statement = statement.where(Item.owner_id == owner_id)

    if sort_by:
        field_name = sort_by.lstrip("-")
        is_desc = sort_by.startswith("-") or (
            sort_order and sort_order.lower() == "desc"
        )
        if hasattr(Item, field_name):
            column_attr = getattr(Item, field_name)
            statement = statement.order_by(
                desc(column_attr) if is_desc else asc(column_attr)
            )

    statement = statement.offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_item(
    session: AsyncSession,
    item_id: int,
    item_data: ItemUpdate,
    request_owner_id: int
) -> Optional[Item]:
    """
    Updates an item if requester is the owner.
    :param session: AsyncSession instance
    :param item_id: item ID
    :param item_data: ItemUpdate schema
    :param request_owner_id: ID of owner making request
    :return: updated Item, None if not found, or False if forbidden
    """
    item = await session.get(Item, item_id)
    if not item:
        return None
    if item.owner_id != request_owner_id:
        return False
    item_data_dict = item_data.model_dump(exclude_unset=True)
    for key, value in item_data_dict.items():
        setattr(item, key, value)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(
    session: AsyncSession,
    item_id: int,
    request_owner_id: int
) -> Optional[bool]:
    """
    Deletes an item if requester is the owner.
    :param session: AsyncSession instance
    :param item_id: item ID
    :param request_owner_id: ID of owner making request
    :return: True if deleted, None if not found, False if forbidden
    """
    item = await session.get(Item, item_id)
    if not item:
        return None
    if item.owner_id != request_owner_id:
        return False
    await session.delete(item)
    await session.commit()
    return True
