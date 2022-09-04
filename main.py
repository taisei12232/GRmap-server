import uvicorn
from fastapi import FastAPI

from firebase import db_operate
from my_types import HelloWorldModel

app = FastAPI()


@app.get("/", response_model=HelloWorldModel)
def root():
    return {"Hello": "World"}


@app.get("/reviews")
def get_review():
    return 200


@app.post("/review")
def post_review(data):
    res = db_operate.add_review(data)
    return res


@app.get("/location")
def get_fest():
    return 200


@app.get("/reviewimage")
def get_url():
    return 200


@app.post("/shop")
def add_shop(data):
    return db_operate.add_shop(data)


@app.post("/test")
def post_test(data):
    print(data)
    print(data.text)
    print(data["text"])


def main() -> None:
    print("===== main() =====")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=2)


if __name__ == "__main__":
    main()
