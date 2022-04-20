from typing import List, Optional
from fastapi import status,Depends,APIRouter,HTTPException,Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models,schemas,oauth2


router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
) 


@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),
                current_user:int=Depends(oauth2.get_current_user),
                limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    print(limit)
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts=db.query(models.Post,func.count(models.Vote.user_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(
        models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),
                current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    # (post.title,post.content,post.published))

    # new_post=cursor.fetchone()

    # conn.commit()
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db),
            current_user:int=Depends(oauth2.get_current_user)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """,(id,))
    # post=cursor.fetchone()

    post=db.query(models.Post,func.count(models.Vote.user_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.id==id).first()

    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id {id} was not found"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),
                current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    # post=cursor.fetchone()
    # conn.commit()

    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    if post.first().owner_id == current_user.id:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),
                current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    # (post.title,post.content,post.published,id))
    # post=cursor.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id==id)
    post_=post_query.first()

    if post_==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    if post_.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update post")

    post_query.update(post.dict(),synchronize_session=False)
    
    db.commit()

    return post_query.first()