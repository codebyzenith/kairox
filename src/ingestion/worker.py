from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models import Source, Article, IngestionRun
from src.ingestion.rss_fetcher import fetch_feed


def run_ingestion(db: Session) -> None:
    sources = db.query(Source).filter(Source.active == True).all()

    for source in sources:
        _ingest_source(db, source)


def _ingest_source(db: Session, source: Source) -> None:
    run = IngestionRun(
        source_id=source.id,
        started_at=datetime.now(timezone.utc),
        status="running",
    )
    db.add(run)
    db.commit()

    try:
        articles = fetch_feed(source.url)

        articles_found = len(articles)
        articles_new = 0

        for article_data in articles:
            exists = db.query(Article).filter(
                Article.url == article_data["url"]
            ).first()

            if exists:
                continue

            article = Article(
                source_id=source.id,
                headline=article_data["title"],
                url=article_data["url"],
                body=article_data["summary"],
                published_at=article_data["published_at"],
            )
            db.add(article)
            articles_new += 1

        db.commit()

        run.status = "completed"
        run.completed_at = datetime.now(timezone.utc)
        run.articles_found = articles_found
        run.articles_new = articles_new
        db.commit()

    except Exception as e:
        db.rollback()
        run.status = "failed"
        run.error_message = str(e)
        run.completed_at = datetime.now(timezone.utc)
        db.commit()