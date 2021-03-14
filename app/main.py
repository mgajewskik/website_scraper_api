from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .db import crud, models
from .db.database import engine, get_db, SessionLocal
from .utils.validators import is_valid_url
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
    log.debug(f"Website: {url} scraped and status updated in db under {id}")


@app.post("/websites/", response_model=Website)
def post_website(
    website: WebsiteCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if not is_valid_url(website.url):
        raise HTTPException(status_code=422, detail="Provided URL is invalid.")

    db_website = crud.get_website_by_url(db, website_url=website.url)
    if db_website:
        if db_website.status != "failed":
            raise HTTPException(
                status_code=400, detail="Website already processed/processing."
            )

    db_website = crud.create_website(db=db, website=website)
    background_tasks.add_task(scrape_website, url=website.url, id=db_website.id)
    log.debug(f"Background task to scrape {website.url} added.")
    return db_website


@app.get("/websites/", response_model=List[Website])
def get_websites(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    websites = crud.get_websites(db, skip=skip, limit=limit)
    return websites


@app.get("/websites/{website_id}", response_model=Website)
def get_website(website_id: int, db: Session = Depends(get_db)):
    db_website = crud.get_website(db, website_id=website_id)

    if db_website is None:
        raise HTTPException(status_code=404, detail="Website not found.")

    return db_website


@app.get("/websites/{website_id}/download/")
def download_website(website_id: int, db: Session = Depends(get_db)):
    db_website = crud.get_website(db, website_id=website_id)

    if db_website is None:
        raise HTTPException(status_code=404, detail="Website not found.")

    if utils.is_zipped_file(website_id):
        log.debug(f"Sourcing files for {website_id}")
        return FileResponse(path=utils.get_zipped_filename(website_id))
    else:
        raise HTTPException(status_code=404, detail="Website resources not found.")
