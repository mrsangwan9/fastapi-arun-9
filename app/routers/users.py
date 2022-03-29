from ..import module,schemas,utile
from fastapi import FastAPI, Response,status,Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    tags=['users']
)


@router.post("/users",response_model=schemas.responseuser)
def create_users(newuser:schemas.createusers,db:Session= Depends(get_db)):
    #cur.execute("""Insert into NewUsers(username,password) Values(%s,%s) Returning *""",(newuser.username,newuser.password))
   # created = cur.fetchone()
   # conn.commit()
   #hash the password  - user.pasword

    hashed_password= utile.hash(newuser.password)
    newuser.password = hashed_password
    
    created = module.Users(
        **newuser.dict())
    if db.query(module.Users).filter(module.Users.username==created.username):
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="username already used..")
    db.add(created)
    db.commit()
    db.refresh(created)
    return created


@router.get('/users/{id}',response_model= schemas.responseuser)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(module.Users).filter(module.Users.id==id).first()
   

    if user == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND)
    return user