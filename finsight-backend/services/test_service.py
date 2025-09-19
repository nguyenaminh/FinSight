from services.db_service import insert_article, get_all_articles

# Insert thử 2 lần cùng URL
article1 = insert_article(
    title="Bitcoin surges today",
    url="https://example.com/bitcoin",
    source="UnitTest",
    category="crypto",
    sentiment=0.8,
    summary="Bitcoin price went up significantly."
)

article2 = insert_article(
    title="Duplicate Bitcoin news",
    url="https://example.com/bitcoin",  # trùng URL
    source="UnitTest",
    category="crypto",
    sentiment=0.5,
    summary="This should not be inserted again."
)

# Đọc lại từ DB
articles = get_all_articles()
print("📊 Total articles:", len(articles))
for a in articles:
    print("-", a.id, a.title, "|", a.url)
