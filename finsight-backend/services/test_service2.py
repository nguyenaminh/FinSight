from services.db_service import insert_article_from_dict, get_all_articles

sample = {
    "title": "Test article for FinSight v2",
    "url": "https://example.com/test-finsight-v2?utm_source=test",
    "source": "UnitTest",
    "published_at": "2025-09-19T12:00:00Z",
    "category": "crypto",
    "summary": "This is a test insert for new schema.",
    "content": "Full content goes here...",
    "language": "en"
}

if __name__ == "__main__":
    inserted = insert_article_from_dict(sample)
    print("Inserted id:", inserted.id)
    arts = get_all_articles()
    print("Total fetched:", len(arts))
    for a in arts:
        print("-", a.id, a.title, "|", a.canonical_url or a.url)
