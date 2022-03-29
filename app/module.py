from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__= "myposts"

    id = Column(Integer,nullable = False,primary_key = True)
    title = Column(String,nullable=False)
    content = Column(String, nullable = False)
    published = Column (Boolean, server_default ='True',nullable = False) 
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default =text('now()'))
   # owner_id = Column(Integer, ForeignKey("usertable.id",ondelete="CASCADE"), nullable = False)# that's id work when have use or related user id with post id to know which post is done by which user.
    created_by = Column(String,ForeignKey("usertable.username",ondelete="CASCADE"),nullable = False)

    #postinfo = relationship("Users")
class Users(Base):
    __tablename__ = 'usertable'

    id = Column(Integer,primary_key = True)
    username = Column(String,nullable = False,unique= True)
    password = Column(String,nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default =text('now()'))
