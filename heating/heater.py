from functools import wraps
from fastapi import BackgroundTasks, FastAPI
from pathlib import Path
from pydantic_loader import load_json, save_json
from pydantic import BaseSettings
import time
from plugcontroller import PlugController
import logging
import os
import asyncio

logging.basicConfig(level=logging.INFO)


class HeaterConfig(BaseSettings):
    state: bool = False
    boost: int = None


app = FastAPI()
plug_controller = PlugController()
config = None
config_file = "state.json"


def load(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global config, config_file
        logging.info("load config")
        if config is None:
            if os.path.isfile(config_file):
                config = load_json(HeaterConfig, Path(config_file))
            else:
                config = HeaterConfig()
        return await func(*args, **kwargs)
    return wrapper


def save():
    global config, config_file
    logging.info("save config")
    save_json(config, Path(config_file))


""" @app.on_event('startup')
@load
async def app_startup(background_tasks: BackgroundTasks):
   background_tasks.add_task(plug_controller.plug_turn_all_off) """


@app.get("/")
@load
async def hello():
    logging.info("hello")
    return {"message": "Hello World"}


@app.get("/status")
@load
async def status():
    logging.info("status")
    return "{'state':" + str(config.state) + ", 'boost':" + str(config.boost) + "}"


@app.get("/on")
@load
async def on(background_tasks: BackgroundTasks):
    global config
    logging.info("turn on")
    config.state = True
    save()
    background_tasks.add_task(plug_controller.plug_turn_all_on)
    return {"result": "on"}


@app.get("/off")
@load
async def off(background_tasks: BackgroundTasks):
    global config
    logging.info("off")

    config.state = False

    if config.boost is None:
        logging.info("boost not active")
        save()
        background_tasks.add_task(plug_controller.plug_turn_all_off)
        return {"result": "off"}
    
    if int(config.boost) + 900 < int(time.time()):
        logging.info("boost time over")
        config.boost = None
        save()
        background_tasks.add_task(plug_controller.plug_turn_all_off)
        return {"result": "off"}

    config.state = True
    save()
    return {"result": "boost active"}


@app.get("/boost")
@load
async def boost(background_tasks: BackgroundTasks):
    global config
    logging.info("boost")    
    config.boost = int(time.time())
    config.state = True
    save()
    background_tasks.add_task(plug_controller.plug_turn_all_on)
    return {"result": "boost"}


@app.get("/reset")
@load
async def reset(background_tasks: BackgroundTasks):
    global config
    logging.info("reset")
    config.boost = None
    config.state = False
    save()
    background_tasks.add_task(plug_controller.plug_turn_all_off)
    return {"result": "reset"}