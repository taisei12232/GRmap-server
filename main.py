import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from firebase import db_operate
from my_types import Fest, HelloWorldModel, Review, ReviewImage, Shop

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # 追記により追加
    allow_methods=["*"],  # 追記により追加
    allow_headers=["*"],  # 追記により追加
)


@app.get("/", response_model=HelloWorldModel)
def root():
    return {"Hello": "World"}


@app.get("/reviews")
def get_review(fid: str):
    res = db_operate.get_reviews(fid)
    return res


@app.post("/review")
def post_review(data: Review):
    res = db_operate.add_review(data)
    return res


@app.get("/location")
def get_fest(lat: float = 35.6554348, lng: float = 139.7607593):
    res = db_operate.search_fest(lat, lng)
    return res


@app.post("/reviewimage")
def get_url(data: ReviewImage):
    db_operate.add_review_image(data)
    return 200


@app.post("/shop")
def add_shop(data: Shop):
    print("ERROR")
    return db_operate.add_shop(data)


@app.post("/test")
def post_test(data):
    print(data)
    print(data.text)
    print(data["text"])


@app.post("/fest")
def post_fes(data: Fest):
    return db_operate.create_festival(data)


def main() -> None:
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        reload=True,
        workers=2,
    )


if __name__ == "__main__":
    main()
