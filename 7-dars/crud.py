from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile
import os


from schems import (
    CategoryCreate, CategoryResponse, NewCreate, NewResponse
)
from models import Category, New


MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)




async def create_category(
    category: CategoryCreate,
    db: AsyncSession
) -> CategoryResponse:
    db_category = Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


async def get_categories(db: AsyncSession) -> list[CategoryResponse]:
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return [CategoryResponse.model_validate(c) for c in categories]


async def get_category(category_id: int, db: AsyncSession) -> CategoryResponse:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category NOT FOUND")
    return CategoryResponse.model_validate(category)


async def update_category(
    category_id: int,
    category: CategoryCreate,
    db: AsyncSession
) -> CategoryResponse:

    db_category = await db.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category NOT FOUND")

    for attr, value in category.model_dump().items():
        setattr(db_category, attr, value)

    await db.commit()
    await db.refresh(db_category)

    return CategoryResponse.model_validate(db_category)


async def delete_category(category_id: int, db: AsyncSession) -> dict:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category NOT FOUND")

    await db.delete(category)
    await db.commit()

    return {"message": "Category deleted successfully"}




async def create_new(
    new: NewCreate,
    db: AsyncSession,
    image: UploadFile = None,
    video: UploadFile = None
) -> NewResponse:

    image_path = None
    video_path = None

    if image:
        image_extension = image.filename.split('.')[-1]
        if image_extension.lower() not in ['jpg', 'jpeg', 'png', 'bmp']:
            raise HTTPException(
                status_code=400,
                detail="Only jpg, jpeg, png, bmp images are allowed"
            )

        image_name = f"{uuid.uuid4()}.{image_extension}"
        image_path = os.path.join(MEDIA_DIR, image_name)

        with open(image_path, "wb") as f:
            f.write(await image.read())

    # VIDEO CHECK
    if video:
        video_extension = video.filename.split('.')[-1]
        if video_extension.lower() not in ['mp4', 'avi', 'mov']:
            raise HTTPException(
                status_code=400,
                detail="Only mp4, avi, mov videos are allowed"
            )

        video_name = f"{uuid.uuid4()}.{video_extension}"
        video_path = os.path.join(MEDIA_DIR, video_name)

        with open(video_path, "wb") as f:
            f.write(await video.read())

    db_new = New(
        **new.model_dump(),
        image=image_path,
        video=video_path
    )

    db.add(db_new)
    await db.commit()
    await db.refresh(db_new)

    return NewResponse.model_validate(db_new)


async def get_news(db: AsyncSession) -> list[NewResponse]:
    result = await db.execute(select(New))
    news = result.scalars().all()
    return [NewResponse.model_validate(c) for c in news]


async def get_new(
    new_id: int,
    db: AsyncSession
) -> NewResponse:
    new = await db.get(New, new_id)
    if not new:
        raise HTTPException(status_code=404, detail="New NOT FOUND")
    return NewResponse.model_validate(new)


async def update_new(
    new_id: int,
    new: NewCreate,
    db: AsyncSession
) -> NewResponse:

    db_new = await db.get(New, new_id)
    if not db_new:
        raise HTTPException(status_code=404, detail="New NOT FOUND")

    for attr, value in new.model_dump().items():
        setattr(db_new, attr, value)

    await db.commit()
    await db.refresh(db_new)

    return NewResponse.model_validate(db_new)



async def delete_new(
    new_id: int,
    db: AsyncSession
) -> dict:

    new = await db.get(New, new_id)
    if not new:
        raise HTTPException(status_code=404, detail="New NOT FOUND")

    await db.delete(new)
    await db.commit()

    return {"message": "New deleted successfully"}