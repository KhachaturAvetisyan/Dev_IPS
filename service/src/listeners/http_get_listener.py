from fastapi import FastAPI
import uvicorn

http_get_app = FastAPI()


def run_http_get_app(host, port):
    uvicorn.run(http_get_app, host=host, port=port)


@http_get_app.get("/")
def root():
    return "OK"
