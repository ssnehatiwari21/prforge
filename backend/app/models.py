from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    pr_number = Column(Integer)
    title = Column(String)
    repo = Column(String)
    author = Column(String)

    status = Column(String)

    review_comment = Column(Text)


class PRComment(Base):
    __tablename__ = "pr_comments"

    id = Column(Integer, primary_key=True, index=True)

    pr_number = Column(Integer)
    repo = Column(String)
    role = Column(String)        # "user" or "assistant"
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String)
    repo_name = Column(String)
    full_name = Column(String)
    description = Column(Text)
    status = Column(String, default="connected")
    created_at = Column(DateTime, default=datetime.utcnow)