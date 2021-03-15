from typing import List

from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .db import crud, models
from .db.database import engine, get_db, SessionLocal
from .utils.validators import is_valid_url, is_valid_url_format
from .utils.exceptions import (
    raise_not_found,
    raise_unprocessable_entity,
    raise_bad_request,
)
from .utils import log, utils
from .scraper import Scraper
from .schemas import Website, WebsiteCreate


models.Base.metadata.create_all(bind=engine)
log.debug("All tables created. Database ready.")


app = FastAPI()


def scrape_website(url: str, id: int):
    """ Download website resources and update the database entry. """

    try:
        Scraper(url, id).scrape()
    except:
        log.debug("Unknown error:", exc_info=True)

    status = "completed" if utils.is_zipped_file(id) else "failed"
    crud.update_website_status(SessionLocal(), website_id=id, website_status=status)
    log.debug(f"Website: {url} scraped and status updated in db under {id}.")


@app.post("/websites/", response_model=Website)
def post_website(
    website: WebsiteCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if not is_valid_url_format(website.url):
        raise_unprocessable_entity(msg="Provided URL format is invalid.")

    if not is_valid_url(website.url):
        raise_unprocessable_entity(msg="Provided URL is not online.")

    db_website = crud.get_website_by_url(db, website_url=website.url)
    if db_website and db_website.status != "failed":
        raise_unprocessable_entity(msg="Website already processed/processing.")

    db_website = crud.create_website(db=db, website=website)
    background_tasks.add_task(scrape_website, url=website.url, id=db_website.id)
    log.debug(f"Background task to scrape {website.url} added.")
    return db_website


@app.get("/websites/", response_model=List[Website])
def get_websites(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):

    if skip or limit < 0:
        raise_bad_request(msg="Bad request - use values > 0.")

    if limit > 20:
        raise_bad_request(msg="Bad request - limit cannot exceed 20.")

    websites = crud.get_websites(db, skip=skip, limit=limit)
    if websites == []:
        raise_not_found()

    return websites


@app.get("/websites/{website_id}/", response_model=Website)
def get_website(website_id: int, db: Session = Depends(get_db)):
    db_website = crud.get_website(db, website_id=website_id)

    if db_website is None:
        raise_not_found()

    return db_website


@app.get("/websites/{website_id}/download/")
def download_website(website_id: int, db: Session = Depends(get_db)):
    db_website = crud.get_website(db, website_id=website_id)

    if db_website is None:
        raise_not_found()

    if utils.is_zipped_file(website_id):
        log.debug(f"Sourcing files for {website_id}.")
        return FileResponse(path=utils.get_zipped_filename(website_id))
    else:
        raise_not_found(msg="Website resources not found.")
