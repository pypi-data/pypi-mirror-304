import asyncio
import json
import logging
import os
import queue
import subprocess
import sys
from typing import Optional

import psutil

# Configure logging for the WebSocket
logger = logging.getLogger("ProcessManager")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ProcessManager:

    def __init__(self, symbol: Optional[str] = None):
        self._command = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), "main.py"),
        ]
        self._symbol = ",".join(symbol) if isinstance(symbol, list) else symbol
        self.process = None
        self.psutil_process = None
        self.output_queue = queue.Queue()
        self.output_list = []
        self.loop = asyncio.get_event_loop()

    def start(self):
        symbol = self.symbol
        if not symbol:
            logger.info("No subscribed symbols.")
            return
        command = self.command
        for c in command:
            if c.startswith("symbol="):
                command.remove(c)
        command.extend([f"symbol={symbol}"])
        if self.process is not None:
            logger.error("Process is already running")
            return
        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.psutil_process = psutil.Process(self.process.pid)
        self.loop.run_until_complete(self._read_output())

    async def _read_output(self):
        while True:
            line = await self.loop.run_in_executor(None, self.process.stdout.readline)
            if not line:
                if self.process.poll() is not None:
                    break
                continue
            logger.info(f"Read line: {line.strip()}")  # Debugging information
            try:
                json_line = json.loads(line)
                self.output_queue.put(json_line)
                self.output_list.append(json_line)
            except json.JSONDecodeError:
                logger.info("Received non-JSON message")

    def send_message(self, message):
        if self.process is None:
            raise RuntimeError("Process is not running")
        self.process.stdin.write(message + "\n")
        self.process.stdin.flush()

    def receive_message(self):
        try:
            return self.output_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        if self.process is None:
            logger.info("No process is running")
            return
        self.psutil_process.terminate()
        self.process.wait()
        self.process = None

    def subscribe(self, symbol):
        ticker = (
            symbol.split(",")
            if isinstance(symbol, str) and "," in symbol
            else symbol if isinstance(symbol, list) else [symbol]
        )
        old_symbols = self.symbol.split(",") if self.symbol else []
        new_symbols = list(set(old_symbols + ticker))
        if self.is_running:
            self.stop()
        self.symbol = new_symbols
        self.start()

    def unsubscribe(self, symbol):
        if not self.symbol:
            logger.info("No subscribed symbols.")
            return
        ticker = (
            symbol.split(",")
            if isinstance(symbol, str) and "," in symbol
            else symbol if isinstance(symbol, list) else [symbol]
        )
        old_symbols = self.symbol.split(",")
        new_symbols: list = [sym for sym in old_symbols if sym not in ticker]
        if self.is_running:
            self.stop()
        self.symbol = new_symbols if new_symbols else None
        if self.symbol:
            self.start()

    @property
    def is_running(self):
        return self.process is not None

    @property
    def results(self):
        return self.output_list

    def clear_results(self):
        self.output_list = []

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        self._command = command

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = (
            ",".join(symbol) if isinstance(symbol, list) else symbol if symbol else None
        )
