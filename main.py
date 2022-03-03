import schema
from fastapi import FastAPI, Query, Depends, Request, Form
from enum import Enum
from pydantic import BaseModel
from database import SessionLocal, engine
import model
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
# from starlette.responses import `JSONResponse

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/movie", response_class=HTMLResponse)
# @app.get("/movie")
async def read_movies(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(Movie).all()
    return 2
#     return templates.TemplateResponse("index.html", {"request": request, "data": records})

# @app.post("/movie/")
# async def create_movie(db: Session = Depends(get_database_session), name: schema.Movie.name = Form(...), url: schema.Movie.url = Form(...), rate: schema.Movie.rating = Form(...), type: schema.Movie.type = Form(...), desc: schema.Movie.desc = Form(...)):
#     movie = Movie(name=name, url=url, rating=rate, type=type, desc=desc)
#     db.add(movie)
#     db.commit()
#     response = RedirectResponse('/', status_code=303)
#     return response

# @app.get("/movie/{name}", response_class=HTMLResponse)
# def read_movie(request: Request, name: schema.Movie.name, db: Session = Depends(get_database_session)):
#     item = db.query(Movie).filter(Movie.id==name).first()
#     print(item)
#     return templates.TemplateResponse("overview.html", {"request": request, "movie": item})

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items2/")
async def read_items(
    q: str
    | None = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.post("/create_item")
# async def create_item(item2: Item):
#     item2.name.cap
#     return item2

async def create_item2(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item



