from typing import List
from datetime import datetime
from sqlalchemy import String, ForeignKey, Column, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database.database import Base


class User(Base):
    """
    System user model.
    Contains basic information and relationship with user's items.
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)  # Unique username
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True, server_default=None) # Unique email
    github_id: Mapped[int] = mapped_column(Integer, unique=True)
    github_login: Mapped[str] = mapped_column(String)

    bio: Mapped[str] = mapped_column(String,        # User's biography 
                                     nullable=False,
                                     server_default="User didn't add his bio")
    
    location: Mapped[str] = mapped_column(String,
                                          nullable=True,
                                          server_default="")
    
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 nullable=False,
                                                 server_default=func.now())

    project: Mapped[List["Project"]] = relationship(
        "Project",
        back_populates="user",
        lazy="selectin"
    )

    # relationship to the Item model – each user may have multiple items
    # (the original code neglected to declare this, which caused the
    # ``Mapper 'User' has no property 'item'`` error when the Item class used
    # ``back_populates='item'``).
    items: Mapped[List["Item"]] = relationship(
        "Item",
        back_populates="user",
        lazy="selectin"
    )

class Item(Base):
    """
    Item model.
    Belongs to specific user through many-to-one relationship.
    Each user can create an item with the same name as another user
    But user cannot create an item with the same name as another of THEIR items.
    """
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)    # Item name (not unique)
    description: Mapped[str] = mapped_column(String, 
                                             nullable=False, 
                                             server_default="No description") # Item description 
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))    # Foreign key to user

    # Many-to-one relationship with User model
    user: Mapped["User"] = relationship(
        "User",
        back_populates="items",  # Back reference matches User.items
        lazy="selectin" # Load user with item
    )

class Project(Base):
    __tablename__ = 'project'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    repo_name: Mapped[str] = mapped_column(String, unique=True)
    owner_name: Mapped[str] = mapped_column(String, unique=False)

    description: Mapped[str] = mapped_column(String, nullable=True)

    full_readme: Mapped[str] = mapped_column(Text, unique=False)          

    repo_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    repo_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # "Cached" Github data 
    github_data: Mapped[dict] = mapped_column(JSON)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))    # Foreign key to user

    # Many-to-one relationship with User model
    user: Mapped["User"] = relationship(
        "User",
        back_populates="project",  # Back reference
        lazy="selectin" # Load user with item
    )