from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr

 # can be a lot of number of schema in a single application
class Post(BaseModel):#that's the base model means user input must be like this can be more then that but must be atleast these field fill up.
    
      content:str
      title:str
      published:bool= False
      
   

      class Config:
        orm_mode=True

class CreatePost(BaseModel):
    content:str
    title:str
    published:bool=False
    
    created_by:str

    class Config:
        orm_mode=True
class userinfo(BaseModel):
        id:int
        username:EmailStr
        created_at:datetime


class responsepost(BaseModel):
    content:str
    title:str
    published:bool=False
    created_by:str
    
   

    class Config:
        orm_mode=True


class createusers(BaseModel):
        username:EmailStr
        password:str


class responseuser(BaseModel):
      username:str

      class Config:
        orm_mode=True




class UserLogin(BaseModel):
        username:EmailStr
        password:str

        
#class PostCreate(Post):# extends post class
    
class Token(BaseModel):
        access_token :str
        token_type:str

    

class TokenData(BaseModel):
        id:Optional[str] = None
