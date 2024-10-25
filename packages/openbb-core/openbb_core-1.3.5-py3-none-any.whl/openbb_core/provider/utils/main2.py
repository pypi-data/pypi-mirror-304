import asyncio
import json
import logging
import os
import sys
import threading

import websockets

# Configure logging for the WebSocket
logger = logging.getLogger("Websocket")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Create a lock for thread-safe file writing
file_lock = threading.Lock()


async def login(websocket, api_key):
    login_event = {
        "event": "login",
        "data": {
            "apiKey": api_key,
        },
    }
    try:
        await websocket.send(json.dumps(login_event))
        response = await websocket.recv()
        logger.info(f"Message: {response}")
        if json.loads(response).get("message") == "Unauthorized":
            logger.error(
                "Account not authorized. Please check that the API key is entered correctly and is entitled to access."
            )
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error during login: {e}")
        sys.exit(1)


async def subscribe(websocket, ticker):
    if isinstance(ticker, str):
        ticker = ticker.split(",")
    subscribe_event = {
        "event": "subscribe",
        "data": {
            "ticker": ticker,
        },
    }
    try:
        await websocket.send(json.dumps(subscribe_event))
        response = await websocket.recv()
        logger.info(f"Message: {response}")
    except Exception as e:
        logger.error(f"Error during subscribe: {e}")


async def connect_and_stream(uri, ticker, api_key, temp_file_path, limit):

    n_rows = 0
    records: list = []
    limit = int(limit) if limit else None

    if os.path.exists(temp_file_path):
        with open(temp_file_path, encoding="utf-8") as temp_file:
            old_records = json.load(temp_file)
            if isinstance(old_records, list) and len(old_records) > 0:
                records = old_records
                n_rows = len(old_records)
    elif not os.path.exists(temp_file_path):
        with open(temp_file_path, "w", encoding="utf-8") as temp_file:
            pass  # Just create the file

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                await login(websocket, api_key)
                await subscribe(websocket, ticker)
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if "event" in data and data["event"] != "heartbeat":
                        logger.info(json.dumps(data))
                    elif data.get("event") != "heartbeat":
                        with file_lock, open(
                            temp_file_path, "w", encoding="utf-8"
                        ) as temp_file:
                            n_rows += 1
                            if limit and n_rows > limit:
                                records = records[-(limit - 1) :]
                            records.append(data)
                            json.dump(records, temp_file, indent=4)

        except (KeyboardInterrupt, websockets.ConnectionClosed):
            logger.info("WebSocket connection closed")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":

    args = sys.argv[1:]
    kwargs: dict = {}
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=")
            kwargs[key] = value

    if not kwargs.get("api_key") and not kwargs.get("apiKey"):
        kwargs["api_key"] = "3ac3ab634f0d5f91ceec1ec7367a21ff"
        # logger.error("API key is required to connect to the WebSocket")
        # sys.exit(1)
    elif kwargs.get("apiKey") and not kwargs.get("api_key"):
        kwargs["api_key"] = kwargs.pop("apiKey")

    if not kwargs.get("symbol"):
        kwargs["symbol"] = "btcusd,ethusd"

    if kwargs.get("results_file"):
        temp_file_path = os.path.abspath(kwargs["results_file"])
        if not os.path.exists(kwargs["results_file"]):
            with open(kwargs["results_file"], "w", encoding="utf-8") as temp_file:
                pass
        kwargs["results_file"] = temp_file_path

    limit = kwargs.get("limit")

    uri = "wss://crypto.financialmodelingprep.com"
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run_coroutine_threadsafe(
            connect_and_stream(
                uri, kwargs["symbol"], kwargs["api_key"], temp_file_path, limit
            ),
            loop,
        )
        loop.run_forever()

    except (KeyboardInterrupt, websockets.ConnectionClosed):
        logger.info("WebSocket connection closed")

    finally:
        sys.exit(0)
