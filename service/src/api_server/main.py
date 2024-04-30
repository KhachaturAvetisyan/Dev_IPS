from os import path
from time import sleep
from typing import Optional
from fastapi import FastAPI, Response, UploadFile, File, Depends
from src.packet_creators.scapy_get import scapy_send_http_get
from src.packet_creators.scapy_post import scapy_send_post_get
from pydantic import BaseModel
from src.listeners.http_get_listener import run_http_get_app
from src.listeners.http_post_listener import run_http_post_app
from multiprocessing import Process
from fastapi import applications
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
import fastapi_offline_swagger_ui

app = FastAPI(
    title="Service API",
    version="1.0.0",
    docs_url="/",
    openapi_url="/api/docs/openapi.json",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

listeners_list = \
    {
        "http_get_listener": {"status": "disabled", "pid": Optional[Process]},
        "http_post_listener": {"status": "disabled", "pid": Optional[Process]},
    }


class HttpGetParams(BaseModel):
    ip: str
    deport: int = 8080
    sport: int = 0
    path: str = "/"
    user_agent: str = "Mozilla/5.0"


class HttpPostParams(BaseModel):
    ip: str
    deport: int = 8080
    sport: int = 0
    path: str = "/"
    user_agent: str = "Mozilla/5.0"


class HTTPGetListenerParams(BaseModel):
    ip: str = "0.0.0.0"
    port: int = 8080


class HTTPPostListenerParams(BaseModel):
    ip: str = "0.0.0.0"
    port: int = 8080


@app.post("/send_http_post")
def send_http_post(response: Response,
                   http_post_params: HttpPostParams = Depends(),
                   file: UploadFile = File(...)):
    print(file.filename)

    # Run the send_http_post function
    try:
        scapy_send_post_get(http_post_params.ip, http_post_params.deport,
                            http_post_params.sport, http_post_params.path,
                            http_post_params.user_agent,
                            file.filename, file.file.read())
    except Exception as e:
        response.status_code = 500
        return str(e)

    # Send OK response
    return "OK"


@app.post("/send_http_get")
def send_http_get(http_get_params: HttpGetParams,
                  response: Response):
    # Run the send_http_get function
    try:
        scapy_send_http_get(http_get_params.ip, http_get_params.deport,
                            http_get_params.sport, http_get_params.path,
                            http_get_params.user_agent)
    except Exception as e:
        response.status_code = 500
        return str(e)

    # Send OK response
    return "OK"


@app.get("/listeners_list")
def get_listeners_list():
    listeners_status = {}
    for listener in listeners_list:
        listeners_status[listener] = listeners_list[listener]["status"]
    return listeners_status


@app.post("/run_http_get_listener")
def run_http_get_listener(http_get_listener_params: HTTPGetListenerParams,
                          response: Response):
    # Check if the listener is already running
    if listeners_list["http_get_listener"]["status"] == "enabled":
        response.status_code = 500
        return "HTTP GET listener is already running"

    # Run the listener
    try:
        # Create a child process
        child = Process(target=run_http_get_app, args=(http_get_listener_params.ip, http_get_listener_params.port))
        # Set the child process as a daemon
        child.daemon = True
        # Start the child process
        child.start()

        # Wait for the child process to start
        sleep(2)

        # Check if the child process is not running
        if not child.is_alive():
            raise Exception("Child process is not running")

        listeners_list["http_get_listener"]["status"] = "enabled"
        listeners_list["http_get_listener"]["pid"] = child
    except Exception as e:
        response.status_code = 500
        return str(e)

    return "OK"


@app.get("/stop_http_get_listener")
def stop_http_get_listener(response: Response):
    # Check if the listener is not running
    if listeners_list["http_get_listener"]["status"] == "disabled":
        response.status_code = 500
        return "HTTP GET listener is not running"

    # Stop the listener
    try:
        listeners_list["http_get_listener"]["pid"].terminate()
    except Exception as e:
        response.status_code = 500
        return str(e)

    # Update the listener status
    listeners_list["http_get_listener"]["status"] = "disabled"

    return "OK"


@app.post("/run_http_post_listener")
def run_http_post_listener(http_post_listener_params: HTTPPostListenerParams,
                           response: Response):
    # Check if the listener is already running
    if listeners_list["http_post_listener"]["status"] == "enabled":
        response.status_code = 500
        return "HTTP Post listener is already running"

    # Run the listener
    try:
        # Create a child process
        child = Process(target=run_http_post_app, args=(http_post_listener_params.ip, http_post_listener_params.port))
        # Set the child process as a daemon
        child.daemon = True
        # Start the child process
        child.start()

        # Wait for the child process to start
        sleep(2)

        # Check if the child process is not running
        if not child.is_alive():
            raise Exception("Child process is not running")

        listeners_list["http_post_listener"]["status"] = "enabled"
        listeners_list["http_post_listener"]["pid"] = child
    except Exception as e:
        response.status_code = 500
        return str(e)

    return "OK"


@app.get("/stop_http_post_listener")
def stop_http_post_listener(response: Response):
    # Check if the listener is not running
    if listeners_list["http_post_listener"]["status"] == "disabled":
        response.status_code = 500
        return "HTTP Post listener is not running"

    # Stop the listener
    try:
        listeners_list["http_post_listener"]["pid"].terminate()
    except Exception as e:
        response.status_code = 500
        return str(e)

    # Update the listener status
    listeners_list["http_post_listener"]["status"] = "disabled"

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
