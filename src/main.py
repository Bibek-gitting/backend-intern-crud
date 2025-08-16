from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List
import src.models as models, src.schemas as schemas
from src.database import engine, Base, SessionLocal
from src.auth import router as auth_router
from src.auth import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog Post CRUD with Likes & Comments")
app.include_router(auth_router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[schemas.UserOut, Depends(get_current_user)]

# Create blog post
@app.post("/api/posts", response_model=schemas.BlogPostOut, status_code=201)
def create_post(post: schemas.BlogPostCreate, db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    new_post = models.BlogPost(
        title=post.title,
        content=post.content,
        user_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"id": new_post.id, "created by": current_user.username ,"title": new_post.title, "content": new_post.content, "likes_count": 0, "comments": []}

# Read all blog posts
@app.get("/api/posts", response_model=List[schemas.BlogPostOut])
def get_posts(db: db_dependency):
    posts = db.query(models.BlogPost).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    result = []
    for p in posts:
        user = db.query(models.User).filter(models.User.id == p.user_id).first()
        result.append({
            "id": p.id,
            "created by": user.username,
            "title": p.title,
            "content": p.content,
            "likes_count": len(p.likes),
            "comments": [schemas.CommentOut.model_config(c) for c in p.comments],
        })
    return result

# Read single blog post
@app.get("/api/posts/{id}", response_model=schemas.BlogPostOut)
def get_post(id: int, db: db_dependency):
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "likes_count": len(post.likes),
        "comments": [schemas.CommentOut.model_config(p) for p in post.comments]
    }

# Update post
@app.put("/api/posts/{id}", response_model=schemas.BlogPostOut)
def update_post(id: int, updated: schemas.BlogPostUpdate, db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if updated.title is not None:
        post.title = updated.title
    if updated.content is not None:
        post.content = updated.content

    db.commit()
    db.refresh(post)
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "likes_count": len(post.likes),
        "comments": [schemas.CommentOut.model_config(p) for p in post.comments]
    }

# Delete post
@app.delete("/api/posts/{id}", status_code=204)
def delete_post(id: int, db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

# Like a post
@app.post("/api/posts/{id}/like", status_code=201)
def like_post(id: int, db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing_like = db.query(models.Like).filter_by(post_id=id, user_id=current_user.id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this post")
    like = models.Like(post_id=id, user_id=current_user.id)
    db.add(like)
    db.commit()
    return {"message": "Post liked successfully"}

# Add comment
@app.post("/api/posts/{id}/comment", response_model=schemas.CommentOut, status_code=201)
def add_comment(id: int, comment: schemas.CommentCreate, db: db_dependency, current_user: user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = models.Comment(post_id=id, user_id=current_user.id, content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Get comments
@app.get("/api/posts/{id}/comments", response_model=List[schemas.CommentOut])
def get_comments(id: int, db: db_dependency):
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db.query(models.Comment).filter(models.Comment.post_id == id).all()
