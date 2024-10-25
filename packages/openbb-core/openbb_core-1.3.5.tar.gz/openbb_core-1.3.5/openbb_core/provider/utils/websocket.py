import atexit
import json
import logging
import os
import subprocess
import sys
import tempfile
import threading
import uuid
from pathlib import Path
from typing import Optional

import psutil


class ProcessManager:
    """ProcessManager class for starting and stopping a WebSocket connection in a non-blocking pattern."""

    def __init__(
        self,
        symbol: Optional[str] = None,
        limit: Optional[int] = None,
        results_file: Optional[str] = None,
        save_results: bool = False,
    ):
        self._command = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), "main2.py"),
        ]
        self._symbol = ",".join(symbol) if isinstance(symbol, list) else symbol
        self.limit = limit
        self._process = None
        self._psutil_process = None
        self._thread = None
        self.results_file = results_file if results_file else None
        if not results_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(json.dumps([]).encode("utf-8"))
                temp_file_path = temp_file.name
                self.results_path = Path(temp_file_path).absolute()
                self.results_file = temp_file_path
        self.results_path = Path(self.results_file).absolute()
        self.save_results = save_results
        self.uuid = uuid.uuid1()

        # Configure logging for the ProcessManager instance.
        self.logger = logging.getLogger(f"ProcessManager-{self.uuid}")
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        atexit.register(self._atexit)

    def _atexit(self):
        if self._process is not None or self.is_running:
            self.stop()
        if self.save_results:
            self.logger.info(f"\nWebsocket results saved to, {self.results_file}.\n")
        else:
            self.logger.info(
                f"\nWebsocket results file, {self.results_file}, removed.\n"
            )
            os.remove(self.results_file)

    def start(self):
        symbol = self.symbol
        if not symbol:
            self.logger.info("\nNo subscribed symbols.")
            return
        command = self.command
        for c in command:
            if c.startswith("symbol=") or c.startswith("results_file="):
                command.remove(c)
        command.extend([f"symbol={symbol}"])
        command.extend([f"results_file={self.results_file}"])
        if self.limit:
            command.extend([f"limit={self.limit}"])
        self._process = subprocess.Popen(
            command,  # noqa
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            env=os.environ,
            text=True,
            bufsize=1,
        )
        self._psutil_process = psutil.Process(self._process.pid)
        self._thread = threading.Thread(
            target=non_blocking_websocket, args=(self._process, self._psutil_process)
        )
        self._thread.daemon = True
        self._thread.start()
        self.logger.info(f"\nWebSocket connection running on PID: {self._process.pid}")
        self.logger.info(f"\nData being captured to: {self.results_file}")

    def stop(self):
        if self._process is None or self.is_running is False:
            return
        if (
            self._psutil_process is not None
            and hasattr(self._psutil_process, "is_running")
            and self._psutil_process.is_running()
        ):
            self.logger.info(f"\nTerminated PID: {self._process.pid}")
            self._psutil_process.terminate()
        self._process.wait()
        self._thread.join()

    def subscribe(self, symbol):
        ticker = (
            symbol.split(",")
            if isinstance(symbol, str) and "," in symbol
            else symbol if isinstance(symbol, list) else [symbol]
        )
        old_symbols = self.symbol.split(",") if self.symbol else []
        new_symbols = list(set(old_symbols + ticker))
        if new_symbols == old_symbols:
            self.logger.info("\nNo new symbols to subscribe.")
            return
        if self.is_running:
            self.stop()
        self.symbol = new_symbols
        self.logger.info(f"\nSubscribed symbols: {new_symbols}")
        self.start()

    def unsubscribe(self, symbol):
        if not self.symbol:
            self.logger.info("\nNo subscribed symbols.")
            return
        ticker = (
            symbol.split(",")
            if isinstance(symbol, str) and "," in symbol
            else symbol if isinstance(symbol, list) else [symbol]
        )
        old_symbols = self.symbol.split(",")
        if symbol not in old_symbols:
            self.logger.info(f"\n{symbol} was not subscribed.")
            return
        new_symbols: list = []
        for sym in old_symbols:
            if sym not in ticker:
                new_symbols.append(sym)
        self.stop()
        self.symbol = new_symbols
        self.logger.info(
            f"\nSubscribed symbols: {new_symbols}"
            if new_symbols
            else "\nNo subscribed symbols."
        )
        if self.symbol:
            self.start()

    @property
    def is_running(self):
        if hasattr(self._psutil_process, "is_running"):
            return self._psutil_process.is_running()
        return False

    @property
    def results(self):
        file_path = self.results_path
        if file_path.exists():
            with open(file_path, encoding="utf-8") as temp_file:
                return json.load(temp_file)
        return []

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

    @property
    def logs(self):
        """Display messages logged by the current connection."""
        if self._process is None:
            return
        if hasattr(self._process, "_fileobj2output") and self._process._fileobj2output:
            try:
                logs = self._process._fileobj2output[
                    list(self._process._fileobj2output)[0]
                ]
                return [d.decode("utf-8").rstrip("\n") for d in logs if d]
            except Exception as e:
                self.logger.error(
                    f"\nError getting messages from the websocket process: {e}"
                )


def non_blocking_websocket(process, psutil_process):
    while psutil_process.is_running():
        process.communicate()
