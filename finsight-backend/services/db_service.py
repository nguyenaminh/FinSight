# services/db_service.py
import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import Article, SessionLocal
from utils.helpers import canonicalize_url, make_fingerprint, parse_date_to_utc, to_json_str

def insert_article_from_dict(data: dict):
    """
    Nhận 1 dict (raw payload từ collector), chuẩn hoá và insert (skip duplicate).
    Trả về Article object (tồn tại hoặc mới insert).
    """
    # extract fields (tùy nguồn mà có key khác nhau)
    title = data.get("title") or data.get("headline") or "No title"
    url = data.get("url") or data.get("link")
    source = data.get("source") or data.get("news_site") or "unknown"
    published_at_raw = data.get("published_at") or data.get("publishedAt") or data.get("date")
    published_at = parse_date_to_utc(published_at_raw)
    category = data.get("category") or "general"
    sentiment = data.get("sentiment") if data.get("sentiment") is not None else None
    summary = data.get("summary") or data.get("description") or None
    content = data.get("content") or None
    language = data.get("language") or "en"
    raw_json_str = to_json_str(data)

    canonical = canonicalize_url(url)
    fingerprint = make_fingerprint(canonical or url, title, summary)

    db: Session = SessionLocal()
    try:
        # check by canonical_url then fingerprint then url
        if canonical:
            existing = db.query(Article).filter(Article.canonical_url == canonical).first()
            if existing:
                print(f"⚠️ Duplicate by canonical_url skipped: {canonical}")
                return existing

        existing_f = db.query(Article).filter(Article.fingerprint == fingerprint).first()
        if existing_f:
            print(f"⚠️ Duplicate by fingerprint skipped: {fingerprint}")
            return existing_f

        if url:
            existing_u = db.query(Article).filter(Article.url == url).first()
            if existing_u:
                print(f"⚠️ Duplicate by url skipped: {url}")
                return existing_u

        new_article = Article(
            title=title,
            url=url,
            canonical_url=canonical,
            fingerprint=fingerprint,
            source=source,
            published_at=published_at,
            fetched_at=datetime.utcnow(),
            language=language,
            content=content,
            summary=summary,
            category=category,
            sentiment=sentiment,
            raw_json=raw_json_str
        )
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        print(f"✅ Inserted: {new_article.title} (id={new_article.id})")
        return new_article
    finally:
        db.close()

def get_all_articles(limit=100):
    db = SessionLocal()
    try:
        return db.query(Article).order_by(Article.published_at.desc()).limit(limit).all()
    finally:
        db.close()

def get_article_by_id(article_id: int):
    db: Session = SessionLocal()
    try:
        return db.query(Article).filter(Article.id == article_id).first()
    finally:
        db.close()

def delete_article(article_id: int):
    db: Session = SessionLocal()
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if article:
            db.delete(article)
            db.commit()
            print(f"✅ Deleted article ID {article_id}")
        else:
            print(f"⚠️ Article ID {article_id} not found")
    finally:
        db.close()