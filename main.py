from fastapi import FastAPI

from database import Base, engine

from routers.genre_router import router as genres_router
from routers.book_router import router as books_router

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(genres_router)
app.include_router(books_router)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

