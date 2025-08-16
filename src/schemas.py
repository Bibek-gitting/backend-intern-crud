from pydantic import BaseModel, Field
from typing import List, Optional

class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = "bearer"

class UserCreate(BaseModel):
    username: str = Field(..., max_length=64, description="Unique username for the user")
    password: str = Field(..., min_length=8, description="Password for the user account")

class UserOut(BaseModel):
    id: int = Field(..., description="Unique identifier of the user")
    username: str = Field(..., max_length=64, description="Username of the user")
    model_config = {"from_attributes": True}

class CommentBase(BaseModel):
    content: str = Field(..., description="Text content of the comment")

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int = Field(..., description="Unique identifier of the comment")

    model_config = {"from_attributes": True}

class BlogPostBase(BaseModel):
    title: str = Field(..., description="Title of the blog post")
    content: str = Field(..., description="Main content/body of the blog post")

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated title of the blog post")
    content: Optional[str] = Field(None, description="Updated main content/body of the blog post")

class BlogPostOut(BlogPostBase):
    id: int = Field(..., description="Unique identifier of the blog post")
    likes_count: int = Field(..., description="Number of likes the post has received")
    comments: List[CommentOut] = Field(default_factory=list, description="List of comments on the post")

    model_config = {"from_attributes": True}

class LikeCreated(BaseModel):
    post_id: int = Field(..., description="ID of the post that was liked")
    user_id: int = Field(..., description="ID of the user who liked the post")

