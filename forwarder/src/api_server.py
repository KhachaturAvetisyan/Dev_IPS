from os import path

from fastapi import FastAPI, Response, UploadFile, File, Depends
import requests
from pydantic import BaseModel
from fastapi import applications
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
import fastapi_offline_swagger_ui

TIMEOUT = 5

app = FastAPI(
    title="Forwarder API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/api/docs/openapi.json",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)


class HttpGetParams(BaseModel):
    ip: str
    deport: int = 8080
    sport: int = 0
    user_agent: str = "Mozilla/5.0"


class HttpPostParams(BaseModel):
    ip: str
    deport: int = 8080
    sport: int = 0


class HTTPGetListenerParams(BaseModel):
    ip: str
    port: int


class HTTPPostListenerParams(BaseModel):
    ip: str
    port: int


@app.post("/send_http_get")
def send_http_get(
        http_get_params: HttpGetParams,
        response: Response,
        service_ip: str = "localhost",
        service_port: int = 9043
):
    # Create a request to the service API server
    try:
        req_response = requests.post(f"http://{service_ip}:{service_port}/send_http_get",
                                     json={
                                         "ip": http_get_params.ip,
                                         "deport": http_get_params.deport,
                                         "sport": http_get_params.sport,
                                         "user_agent": http_get_params.user_agent
                                     },
                                     timeout=TIMEOUT
                                     )
    except requests.exceptions.ReadTimeout:
        response.status_code = 408
        return "Service API server timeout"

    # Check if the response is not 200
    if req_response.status_code != 200:
        response.status_code = req_response.status_code
        return req_response.text

    return "OK"


# TODO Implement this endpoint
@app.post("/send_http_post")
def send_http_post(
        response: Response,
        file: UploadFile = File(...),
        http_post_params: HttpPostParams = Depends(),
        service_ip: str = "localhost",
        service_port: int = 9043
):
    # Create a request to the service API server
    try:
        req_response = requests.post(f"http://{service_ip}:{service_port}/send_http_post",
                                     params={
                                         "ip": http_post_params.ip,
                                         "deport": http_post_params.deport,
                                         "sport": http_post_params.sport,
                                     },
                                     files={"file": (file.filename, file.file.read())},
                                     timeout=TIMEOUT
                                     )
    except requests.exceptions.ReadTimeout:
        response.status_code = 408
        return "Service API server timeout"

    # Check if the response is not 200
    if req_response.status_code != 200:
        response.status_code = req_response.status_code
        return req_response.text

    return "OK"


@app.post("/send_icmp")
def send_icmp(
        response: Response,
        service_ip: str = "localhost",
        service_port: int = 9043
):
    return "Not implemented"


@app.get("/listeners_list")
def get_listeners_list(
        response: Response,
        service_ip: str = "localhost",
        service_port: int = 9043
):
    # Create a request to the service API server
    try:
        req_response = requests.get(f"http://{service_ip}:{service_port}/listeners_list",
                                    timeout=TIMEOUT
                                    )
    except requests.exceptions.ReadTimeout:
        response.status_code = 408
        return "Service API server timeout"

    # Check if the response is not 200
    if req_response.status_code != 200:
        response.status_code = req_response.status_code
        return req_response.text

    return req_response.json()


@app.post("/run_http_get_listener")
def run_http_get_listener(
        http_get_listener_params: HTTPGetListenerParams,
        response: Response,
        service_ip: str = "localhost",
        service_port: int = 9043
):
    # Create a request to the service API server
    try:
        req_response = requests.post(f"http://{service_ip}:{service_port}/run_http_get_listener",
                                     json={
                                         "ip": http_get_listener_params.ip,
                                         "port": http_get_listener_params.port
                                     },
                                     timeout=TIMEOUT
                                     )
    except requests.exceptions.ReadTimeout:
        response.status_code = 408
        return "Service API server timeout"

    # Check if the response is not 200
    if req_response.status_code != 200:
        response.status_code = req_response.status_code
        return req_response.text

    return "OK"


@app.post("/stop_http_get_listener")
def stop_http_get_listener(
        response: Response,
        service_ip: str = "localhost",
        service_port: int = 9043
):
    # Create a request to the service API server
    try:
        req_response = requests.get(f"http://{service_ip}:{service_port}/stop_http_get_listener",
                                    timeout=TIMEOUT
                                    )
    except requests.exceptions.ReadTimeout:
        response.status_code = 408
        return "Service API server timeout"

    # Check if the response is not 200
    if req_response.status_code != 200:
        response.status_code = req_response.status_code
        return req_response.text

    return "OK"


@app.post("/run_http_post_listener")
def run_http_post_listener(
        http_post_listener_params: HTTPPostListenerParams,
        response: Response,
        service_ip: str = "localhost",
        service_port: int = 9043
):
    # Create a request to the service API server
    try:
        req_response = requests.post(f"http://{service_ip}:{service_port}/run_http_post_listener",
                                     json={
                                         "ip": http_post_listener_params.ip,
                                         "port": http_post_listener_params.port
                                     },
                                     timeout=TIMEOUT
                                     )
    except requests.exceptions.ReadTimeout:
        response.status_code = 408
        return "Service API server timeout"

    # Check if the response is not 200
    if req_response.status_code != 200:
        response.status_code = req_response.status_code
        return req_response.text

    return "OK"


@app.post("/stop_http_post_listener")
def stop_http_post_listener(
        response: Response,
        service_ip: str = "localhost",
        service_port: int = 9043
):
    # Create a request to the service API server
    try:
        req_response = requests.get(f"http://{service_ip}:{service_port}/stop_http_post_listener",
                                    timeout=TIMEOUT
                                    )
    except requests.exceptions.ReadTimeout:
        response.status_code = 408
        return "Service API server timeout"

    # Check if the response is not 200
    if req_response.status_code != 200:
        response.status_code = req_response.status_code
        return req_response.text

    return "OK"


assets_path = fastapi_offline_swagger_ui.__path__[0]
if path.exists(assets_path + "/swagger-ui.css") and path.exists(assets_path + "/swagger-ui-bundle.js"):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")


    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )

    applications.get_swagger_ui_html = swagger_monkey_patch
