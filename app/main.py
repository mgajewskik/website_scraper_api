from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db, engine
from .validators import is_valid_url


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def scrape_website():
    pass


@app.post("/websites/", response_model=schemas.Website)
def post_website(website: schemas.WebsiteCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    # validate website.url if right
    if not is_valid_url(website.url):
        raise HTTPException(status_code=422, detail="Provided URL is invalid.")

    # validate if status pending - cannot add again
    # if status failed - can add again

    # if status failed add again
    db_website = crud.get_website_by_url(db, website_url=website.url)
    if db_website:
        raise HTTPException(status_code=400, detail="Website already processed.")

    # start background task
    # background_tasks.add_task(function, parameters)
    return crud.create_website(db=db, website=website)


@app.get("/websites/", response_model=List[schemas.Website])
def get_websites(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    websites = crud.get_websites(db, skip=skip, limit=limit)
    return websites


@app.get("/websites/{website_id}", response_model=schemas.Website)
def get_website(website_id: int, db: Session = Depends(get_db)):
    db_website = crud.get_website(db, website_id=website_id)

    if db_website is None:
        raise HTTPException(status_code=404, detail="Website not found")

    return db_website


@app.get("/websites/{website_id}/download/")
def download_website(website_id: int, db: Session = Depends(get_db)):
    db_website = crud.get_website(db, website_id=website_id)

    if db_website is None:
        raise HTTPException(status_code=404, detail="Website not found")

    # check for file on disk with id = website.id
    # check on S3 for file
    # if no file return response no resource available

    return FileResponse(file, media_type="application/zip")


# @app.delete("/websites/{website_id}/")
# def delete_website(website_id: int, db: Session = Depends(get_db)):
    # db_website = crud.get_website(db, website_id=website_id)

    # if db_website is None:
        # raise HTTPException(status_code=404, detail="Website not found")

    # crud.delete_website(db, website_id=website_id)

    # return JSONResponse(status_code=200, content={"detail": "Website deleted"})

