import uvicorn
from fastapi import FastAPI

from my_types import HelloWorldModel

app = FastAPI()


@app.get("/", response_model=HelloWorldModel)
def root():
    return {"Hello": "World"}

@app.get("/reviews")
def getreview():
    return 200

@app.post("/review")
def postreview():
    return 200

@app.get("/location")
def getfest():
    return 200

@app.get("/reviewimage")
def geturl():
    return 200

def main() -> None:
    print("===== main() =====")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=2)


if __name__ == "__main__":
    main() 