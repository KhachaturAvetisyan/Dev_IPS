from fastapi import FastAPI, File
import uvicorn

http_post_app = FastAPI()


def run(host, port):
    uvicorn.run(http_post_app, host=host, port=port)


@http_post_app.post("/")
def root(file_bytes: bytes = File()):
    return {'file_bytes': str(file_bytes)}

