from services.db_service import insert_article, get_all_articles, get_article_by_id, delete_article
from database import SessionLocal

def test_insert():
    print("=== Test Insert ===")
    article = insert_article(
        title="Ethereum update",
        url="https://example.com/eth",
        source="UnitTest",
        category="crypto",
        summary="ETH test insert"
    )
    print("Inserted:", article.title, "| ID:", article.id)

def test_read():
    print("\n=== Test Read ===")
    articles = get_all_articles()
    for a in articles:
        print(f"{a.id} | {a.title} | {a.url}")

def test_get_by_id():
    print("\n=== Test Get By ID ===")
    article = get_article_by_id(1)
    if article:
        print("Found:", article.title)
    else:
        print("No article with ID=1")

def test_delete():
    print("\n=== Test Delete ===")
    # Lấy record cuối cùng để xoá thử
    db = SessionLocal()
    last = db.query(get_all_articles()[0].__class__).order_by(-get_all_articles()[0].id).first()
    if last:
        print("Deleting:", last.title)
        delete_article(last.id)
    else:
        print("No article to delete")
    db.close()

if __name__ == "__main__":
    test_insert()
    test_read()
    test_get_by_id()
    test_delete()
    test_read()
