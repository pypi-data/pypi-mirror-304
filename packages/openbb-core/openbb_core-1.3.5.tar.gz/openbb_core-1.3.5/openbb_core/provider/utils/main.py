import asyncio
import json
import logging
import sys

import websockets

# Configure logging for the WebSocket
logger = logging.getLogger("WebSocket")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


async def login(websocket, api_key):
    login_event = {
        "event": "login",
        "data": {
            "apiKey": api_key,
        },
    }
    try:
        await websocket.send(json.dumps(login_event))
        logger.info("Login event sent")
        response = await websocket.recv()
        logger.info(f"Login response: {response}")
        if json.loads(response).get("message") == "Unauthorized":
            logger.error(
                "Account not anauthorized. Please check that the API key is entered correctly and is entitled to access."
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
        logger.info("Subscribe event sent")
        response = await websocket.recv()
        logger.info(f"Subscribe response: {response}")
    except Exception as e:
        logger.error(f"Error during subscribe: {e}")


async def connect_and_stream(uri, ticker, api_key):
    async with websockets.connect(uri) as websocket:
        await login(websocket, api_key)
        await subscribe(websocket, ticker)
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                if "event" in data and data["event"] != "heartbeat":
                    logger.info(data)
                elif data.get("event") != "heartbeat":
                    sys.stdout.write(json.dumps(data) + "\n")
            except KeyboardInterrupt:
                logger.info("Connection closed")
                break
            except json.JSONDecodeError:
                logger.error("Received non-JSON message")


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

    uri = "wss://crypto.financialmodelingprep.com"
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run_coroutine_threadsafe(
            connect_and_stream(uri, kwargs["symbol"], kwargs["api_key"]), loop
        )
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Connection closed")
    finally:
        sys.exit(0)
