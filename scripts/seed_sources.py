from src.database import SessionLocal
from src.models import Source


def seed_sources():
    db = SessionLocal()

    sources = [
        {
            "name": "Yahoo Finance",
            "url": "https://finance.yahoo.com/rss/topstories",
            "category": "financial_news",
            "tier": 5,
            "source_type": "rss",
        },
        {
            "name": "MarketWatch",
            "url": "https://feeds.marketwatch.com/marketwatch/topstories",
            "category": "financial_news",
            "tier": 4,
            "source_type": "rss",
        },
        {
            "name": "CNBC Finance",
            "url": "https://www.cnbc.com/id/10001147/device/rss/rss.html",
            "category": "financial_news",
            "tier": 5,
            "source_type": "rss",
        },
        {
            "name": "Seeking Alpha",
            "url": "https://seekingalpha.com/feed.xml",
            "category": "financial_news",
            "tier": 3,
            "source_type": "rss",
        },
    ]

    for s in sources:
        exists = db.query(Source).filter(Source.url == s["url"]).first()
        if exists:
            print(f"Already exists: {s['name']}")
            continue

        source = Source(**s)
        db.add(source)
        print(f"Added: {s['name']}")

    db.commit()
    db.close()
    print("\nDone.")


if __name__ == "__main__":
    seed_sources()