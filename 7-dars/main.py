from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from schems import (
    CategoryResponse, CategoryCreate,
    NewCreate, NewResponse
)

from database import get_db, engine, Base
import crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)



@app.post('/category', response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_category(category, db)


@app.get('/categories', response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)


@app.put('/categories/{categories_id}', response_model=NewResponse)
async def update_categories(
    categories_id: int,
    categories: NewCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_categories(categories_id, categories, db)


@app.delete('/category/{category_id}')
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_category(category_id, db)



@app.post('/news', response_model=NewResponse)
async def create_news(
    name: str,
    title: str,
    content: str,
    category_id: int,
    image: Optional[UploadFile] = None,
    video: Optional[UploadFile] = None,
    db: AsyncSession = Depends(get_db)
):
    news = NewCreate(
        name=name,
        title=title,
        content=content,
        category_id=category_id
    )
    return await crud.create_news(news, db, image, video)


@app.get('/news', response_model=list[NewResponse])
async def get_news(db: AsyncSession = Depends(get_db)):
    return await crud.get_news(db)


@app.put('/news/{news_id}', response_model=NewResponse)
async def update_news(
    news_id: int,
    news: NewCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_news(news_id, news, db)


@app.delete('/news/{news_id}')
async def delete_news(news_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_news(news_id, db)




if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)