import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Cho phép override DATABASE_URL qua env var (dễ tạo DB mới để test)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finsight.db")

# engine: nếu là sqlite cần connect_args, khác thì để mặc định
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=True)           # original url (may be null)
    canonical_url = Column(String, unique=True, nullable=True) # canonicalized url
    fingerprint = Column(String, index=True, nullable=True)    # hash for dedupe
    source = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)
    language = Column(String, default="en")
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    category = Column(String, default="general")
    sentiment = Column(Float, nullable=True)
    raw_json = Column(Text, nullable=True)    # store original payload (stringified)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
