from typing import Optional

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Category(Base):
    __tablename__ ='categories'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(150), unique=True)


class New(Base):
    __tablename__ = 'news'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    title:Mapped[str]=mapped_column(String(255))
    image:Mapped[Optional[str]]=mapped_column(nullable=True)
    video:Mapped[Optional[str]]=mapped_column(nullable=True)
    content:Mapped[str]=mapped_column(Text)
    author:Mapped[str]=mapped_column(String(150))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship("Category", back_populates="news")


