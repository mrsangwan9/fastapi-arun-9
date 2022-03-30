from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,module
from .database import get_db
from fastapi import Depends,HTTPException ,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#secret key
#algorithm
#expression time( like time to loged in. after this time user have to login again..)



def create_acces_token(data: dict):
    to_encode =  data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encode_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return encode_jwt


def verify_access_token(token:str, credentials_exception):
     try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        id:str= payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

     except JWTError:
       raise credentials_exception

     return token_data
 


def get_current_user(token:str=Depends(oauth2_scheme),db:Session = Depends(get_db)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="login to access",
        headers={"WWW-Authenticate":"Bearer"})
      
        token = verify_access_token(token,credentials_exception)

        user:int = db.query(module.Users).filter(module.Users.id == token.id).first()
      
       
        
        return user