from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

# --- SQL DATABASE SETUP ---
DATABASE_URL = "sqlite:///./social_app.db" # This creates a file in your folder
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DATABASE MODELS ---
class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    bio = Column(String, default="New Student!")

class PostTable(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True)
    owner = Column(String)
    content = Column(Text)
    image_url = Column(String)

# Create the database files
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Middleware (CORS)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check if user exists using SQL
    exists = db.query(UserTable).filter(UserTable.username == username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username taken")
    
    new_user = UserTable(username=username, password=password)
    db.add(new_user)
    db.commit()
    return {"message": "User Created"}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Find user in SQL
    user = db.query(UserTable).filter(UserTable.username == username, UserTable.password == password).first()
    if not user:
        raise HTTPException(status_code=400, detail="Wrong username or password")
    return {"username": user.username, "bio": user.bio}

@app.post("/upload")
def create_post(username: str = Form(...), content: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    with open(f"static/{filename}", "wb") as buffer:
        import shutil
        shutil.copyfileobj(file.file, buffer)
    
    new_post = PostTable(
        id=str(uuid.uuid4()),
        owner=username,
        content=content,
        image_url=f"http://127.0.0.1:8000/static/{filename}"
    )
    db.add(new_post)
    db.commit()
    return {"message": "Post saved to SQL"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(PostTable).all()

@app.delete("/delete/{post_id}")
def delete_post(post_id: str, username: str, db: Session = Depends(get_db)):
    post = db.query(PostTable).filter(PostTable.id == post_id, PostTable.owner == username).first()
    if post:
        db.delete(post)
        db.commit()
        return {"message": "Deleted from SQL"}
    raise HTTPException(status_code=404, detail="Not found or unauthorized")

# Don't forget to mount your static folder like in previous steps!
