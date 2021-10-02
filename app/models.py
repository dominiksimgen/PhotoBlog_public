from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy.orm import relationship
from . import db
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, MONEY, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR
     
login_manager = LoginManager()



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    
    # "author" bezieht sich auf das "author" Attribut der PhotoPost Klasse
    posts = relationship("PhotoPost", back_populates="author")
    comments =  relationship("Comment", back_populates="comment_author")

class PhotoPost(db.Model):
    __tablename__ = "photo_posts"
    id = db.Column(db.Integer, primary_key=True)
    
    #Erzeugt Foreign Key, "users.id" bezieht sich auf die Tabelle "users"
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #Erzeugt eine Referenz zum User Object, und bezieht sich auf das "posts" Attribut der User Klasse.
    author = relationship("User", back_populates="posts")


    img = db.Column(db.LargeBinary)
    subtitle = db.Column(db.String(250))
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    maps_url = db.Column(db.String(250))
    likes = db.Column(db.Integer) # soll sich auf die Tabelle "users" beziehen, ist noch nicht implementiert
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    post_id = db.Column(db.Integer, db.ForeignKey("photo_posts.id"))
    parent_post = relationship("PhotoPost", back_populates="comments")
