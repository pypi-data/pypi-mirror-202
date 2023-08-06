
import os
import json
import sys

from websockets.client import connect as ws_connect
from websockets.server import serve as ws_serve
from websockets.datastructures import Headers,HeadersLike
from http import HTTPStatus
import numpy as np
import io
from typing import Optional,Dict,Tuple,Union,List
import logging
import asyncio
import traceback
from asyncio import Future
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
import uuid
import requests
import aiohttp
import uproot
from time import time_ns
import asyncstdlib as asynclib
import lz4.frame
from sanic.log import logger

from websockets.legacy.client import Connect

from sanic import Request,Websocket,Sanic
from sanic import response


def prepare_logger()->logging.Logger:
    logger = logging.getLogger("server")
    server_logger_handler: logging.StreamHandler = logging.StreamHandler()
    server_logger_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(name)-6s] %(levelname)-8s %(message)s"
                            ))
    logger.addHandler(server_logger_handler)
    logger.setLevel(logging.DEBUG)
    return logger

# forward_connection:Union[Connect,None] = None
# forward_url:Union[str,None] = None

CURR_HOST = "0.0.0.0"
CURR_HOST_PORT = 8765
print("UPROOT SERIALIZATION")

def get_next_url()->str:
    forward_service_name = os.environ.get("FORWARD")
    logger.info(f"Loaded forward url: {forward_service_name}")
    return f"ws://{forward_service_name}:8765"

def get_all_slices()->List[str]:
    service_list = os.environ.get("SLICES").split(",")
    logger.info(f"Loaded slice services: {service_list}")
    return service_list

def get_input_dims()->Tuple[int]:
    input_dims_list = (int(s) for s in os.environ.get("INPUTDIMS").split(","))
    return tuple(input_dims_list)
    

app = Sanic("OrchestratorServer")
app.ctx.forward_url:str = get_next_url()
app.ctx.all_slice_services:List[str] = get_all_slices()
app.ctx.forward_connection:Union[Connect,None] = None
app.ctx.rrm_lock = asyncio.Lock()
app.ctx.request_response_map:Dict[str,Future] = {}
app.ctx.input_dims = get_input_dims()
app.config.WEBSOCKET_MAX_SIZE = sys.maxsize
app.config.KEEP_ALIVE_TIMEOUT = sys.maxsize
app.config.RESPONSE_TIMEOUT = sys.maxsize
app.config.RESPONSE_TIMEOUT = sys.maxsize

# request_response_map:Dict[str,Future] = {}
# rrm_lock = asyncio.Lock()
@app.websocket("/predict")
async def record_response(request:Request,ws:Websocket):
    async for data in ws:
        logger.info("RECEIVED PREDICT!")
        requestId:str
        try:
            decompressed_buff = io.BytesIO()
            decompressed_buff.write(lz4.frame.decompress(data))
            decompressed_buff.seek(0)
            requestId = decompressed_buff.read(36).decode("utf-8")
            logger.info("DECOMPRESSED!")
            logger.info(requestId)
            # data = np.load(decompressed_buff)
            # logger.info("LOADED!")
            # logger.info(data.shape)
            async with app.ctx.rrm_lock:
                app.ctx.request_response_map[requestId].set_result(decompressed_buff.read())
        except Exception as e:
            logger.error(traceback.format_exc())
            async with app.ctx.rrm_lock:
                app.ctx.request_response_map[requestId].set_exception(e)

@app.post("/input")
async def make_prediction(request:Request):
    logger.info("INPUT REQUEST!")
    try:
        request_buff = io.BytesIO()
        request_buff.write(request.body)
        request_buff.seek(0)
        array:np.ndarray = np.load(request_buff)
        expected_input_dims = app.ctx.input_dims

        if len(expected_input_dims) + 1 != len(array.shape) or array.shape[1:] != expected_input_dims:
            raise ValueError()
        
        send_buff = io.BytesIO()
        request_id = str(uuid.uuid4())
        send_buff.write(bytes(request_id,"utf-8"))
        send_buff.write(request.body)
        send_buff.seek(0)
        
        
        loop = asyncio.get_running_loop()
        response_future = loop.create_future()
        async with app.ctx.rrm_lock:
            app.ctx.request_response_map[request_id] = response_future
        await app.ctx.forward_connection.send(lz4.frame.compress(send_buff.read()))
        logger.info("WAITING!")
        await response_future
        return response.raw(body=response_future.result(), status = HTTPStatus.OK)
    except ValueError as e:
        logger.error(traceback.format_exc())
        return response.raw(body="Input dimensions does not match the model",status=HTTPStatus.BAD_REQUEST)
    except Exception as e:
        logger.error(traceback.format_exc())
        return response.json(body=e,status=HTTPStatus.INTERNAL_SERVER_ERROR)

    
@app.get("/connect")
async def connect_to_forward(request:Request):
    try:
        app.ctx.forward_connection:Connect = await ws_connect(f"{app.ctx.forward_url}/predict", max_size=sys.maxsize)
        logger.info(f"Successfly connected to forward_url: {app.ctx.forward_url}")
        return response.text("Successfully connected to  forward url",status=HTTPStatus.OK)
    except:
        logger.error(traceback.format_exc())
        return response.text("Unable to connect to forward url")

@app.get("/activate")
async def activate_all_slices(request:Request):
    try:
        result = {}
        service_name:str
        for service_name in app.ctx.all_slice_services:
            slice_forward_connect_url = f"http://{service_name}:8765/connect"
            async with aiohttp.ClientSession() as session:
                async with session.get(slice_forward_connect_url) as resp:
                    result[service_name] = {
                        "status" : resp.status,
                        "response": await resp.text()
                    }
        return response.json(result,status=HTTPStatus.OK) 
    except Exception:
        logger.error(traceback.format_exc())
        return response.text(body="Failed to activate one or all slice nodes",status=HTTPStatus.BAD_REQUEST)


@app.get("/healthcheck")
async def perform_healthcheck(request:Request):
    logger.info(f"Generating healthcheck")
    return response.json({"forward_url":app.ctx.forward_url, "connected": app.ctx.forward_connection is not None and app.ctx.forward_connection.open},status=HTTPStatus.OK)


@app.get("/workerhealthcheck")
async def queryworker_healthcheck(request:Request):
    try:
        logger.info(f"Generating worker healthcheck")
        result = {}
        service_name:str
        for service_name in app.ctx.all_slice_services:
            healthcheck_url = f"http://{service_name}:8765/healthcheck"
            async with aiohttp.ClientSession() as session:
                async with session.get(healthcheck_url) as resp:
                    result[service_name] = {
                        "status":resp.status,
                        "response": await resp.text()
                    }
                    
            
        return response.json(result,status=HTTPStatus.OK)
    except Exception:
        logger.error(traceback.format_exc())
        return response.text(body="Failed to fetch health check for one or more workers. Perhaps connections have not been established yet. Run http://\{orchestrator_ip\}:8765/activateworkers",status=HTTPStatus.BAD_REQUEST)


if __name__ == "__main__":
    app.run(host=CURR_HOST,port=8765,access_log=True,debug=True)