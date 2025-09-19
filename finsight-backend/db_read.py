from database import SessionLocal, Article

session = SessionLocal()

articles = session.query(Article).all()

print("📖 Articles in DB:")
for a in articles:
    print(a.id, a.title, a.source, a.published_at)

session.close()
