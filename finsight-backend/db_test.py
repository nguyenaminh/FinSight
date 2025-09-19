from datetime import datetime
from database import SessionLocal, Article

# Tạo session
session = SessionLocal()

# Tạo 1 Article mới
new_article = Article(
    title="Hello FinSight",
    url="https://example.com/hello",
    source="Demo Source",
    published_at=datetime.now(),
    category="crypto",
    sentiment=0.0,
    summary="This is a demo article."
)

# Lưu vào DB
session.add(new_article)
session.commit()
session.refresh(new_article)  # cập nhật ID sau khi commit

print("✅ Inserted:", new_article.id, new_article.title)

session.close()
