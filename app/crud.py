import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_website(db: Session, website_id: int):
    return db.query(models.Website).filter(models.Website.id == website_id).first()


def get_website_by_url(db: Session, website_url: str):
    return db.query(models.Website).filter(models.Website.url == website_url).first()


def get_websites(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Website).offset(skip).limit(limit).all()


def create_website(db: Session, website: schemas.WebsiteCreate):
    db_website = models.Website(started_at=datetime.datetime.now(), url=website.url)
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website


# def delete_website(db: Session, website_id: int):
    # db.query(models.Website).filter(models.Website.id == website_id).delete()
    # db.commit()
