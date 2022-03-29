from asyncio.windows_events import NULL
from operator import mod
from ..import module, schemas, oauth2
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    tags=['post']
)


@router.get("/")
def root():
    return "that's the home page of Your social media account "


@router.get("/posts", response_model=List[schemas.CreatePost])
def all_post(db: Session = Depends(get_db)):
    #  cur.execute("""select * from posts""")
    #  posts = cur.fetchall()
    #  return {"data":posts}

    mypost = db.query(module.Post).all()
    return mypost


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.responsepost)
def add_post(post: schemas.Post, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
   # new_post= module.Post(title =post.title,content =post.content,published = post.published)
    #  cur.execute("""INSERT INTO posts (title, content, Published)  VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
   # single_post = cur.fetchone()
    # conn.commit()
  #  return {"your post":single_post}
    # print(get_current_user.password)
  #  print(get_current_user.username)
    new_post = module.Post(created_by = get_current_user.username,
                           **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}")
def get_single_post(id: int, db: Session = Depends(get_db)):
  #  cur.execute("""Select * from posts where id= %s""",(str(id),))
 #   mypost = cur.fetchone()
    mypost = db.query(module.Post).filter(module.Post.id == id).first()
    if not mypost:
        return{"Your post": "Sorry their is not post with your id number..."}
    else:
        return mypost


@router.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    if get_current_user.id == id:

        post_query = db.query(module.Post).filter(module.Post.owner_id == id)
        post = post_query.first()
        post_query.update(updated_post.dict(), synchronize_session=False)
        db.commit()
      #  cur.execute("""update posts set title= %s,content = %s, published = %s where id = %s returning *""",
   # (post.title,post.content,post.published,(str(id))))
   # cur.execute("""update posts set title = %s where id = %s returning *""",
        # (newupdate.title,(str(id))),)
   # update_post = cur.fetchone()
   # conn.commit()
        if post == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
        else:
            return post_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="your can't update this post. You must be owner for this post for that.")


@router.delete("/posts/{id}")
def del_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
   # cur.execute("""DELETE  FROM posts WHERE id = %s RETURNING *""",(str(id),))
   ## Deleted_post =  cur.fetchone()
    # conn.commit()

    if get_current_user.id == id:

        Delete_post = db.query(module.Post).filter(
            module.Post.owner_id == id).first()

        if Delete_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="posts not found..")
        else:
            db.delete(Delete_post)
        db.commit()
        return Delete_post

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="your can't delete this post. You must be owner for this post for that.")
