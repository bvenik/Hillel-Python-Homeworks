from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

try:
    from database import get_session
    from models import ItemCreate, ItemRead, ItemUpdate
    import crud
except ImportError:
    from ..database import get_session
    from ..models import ItemCreate, ItemRead, ItemUpdate
    from .. import crud

router = APIRouter()


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_item(session, item)


@router.get("/", response_model=List[ItemRead])
async def list_items(
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = Query(
        None, description="Search by title or description"),
    owner_id: Optional[int] = Query(None, description="Filter by owner ID"),
    sort_by: Optional[str] = Query(
        None, description="Sort field (e.g. price, title)"),
    sort_order: Optional[str] = Query(
        "asc", description="Sort order: asc or desc"),
    session: AsyncSession = Depends(get_session)
):
    return await crud.get_items(
        session,
        skip=skip,
        limit=limit,
        title=title,
        owner_id=owner_id,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await crud.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item_endpoint(
    item_id: int,
    item_update: ItemUpdate,
    owner_id: int = Query(...),
    session: AsyncSession = Depends(get_session)
):
    result = await crud.update_item(session, item_id, item_update, owner_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the item owner can update this item"
        )
    return result


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_endpoint(
    item_id: int,
    owner_id: int = Query(...),
    session: AsyncSession = Depends(get_session)
):
    result = await crud.delete_item(session, item_id, owner_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the item owner can delete this item"
        )
    return None
