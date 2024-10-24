"""This is a basic tcp client that communicates with tcp servers (devices)"""

import asyncio
import logging
import threading
from typing import Callable, List

logger = logging.getLogger(__name__)


class TCPClient:
    """The TCP Client"""
    def __init__(self, host: str, port: int, delimiter: str,
                 receive: Callable, connection_status: Callable = None,
                 rate_limit: float = None):
        """A TCP socket client that can send either str or bytes.

            Features:

             * Rate Limiting -- sets the number of messages per second
             * Connection Status -- allows a callback to be assigned for when the connection is made or dropped
        """
        self._host = host
        self._port = port
        self._delimiter = delimiter.encode()
        self._receive = receive
        self._connection_status = connection_status
        self._rate_limit = rate_limit

        self.connected = False

        self._writer = None
        self._queue = asyncio.Queue(maxsize=10)
        self._send_worker = None

        self._poll_worker = None
        self._poll = None

    async def _socket_listener(self, reader):
        """Receive and split messages from the server"""
        incoming_messages = b""
        while True:
            data = await reader.read(1024)
            if not data:
                break
            incoming_messages += data
            # logger.debug(f"Data: {incoming_messages}")
            if self._delimiter:
                # Split on the delimiter
                while self._delimiter in incoming_messages:
                    msg = incoming_messages.split(self._delimiter)[0]
                    incoming_messages = incoming_messages.replace(msg + self._delimiter, b'')
                    self._receive(msg.decode())
            else:
                self._receive(incoming_messages)
                incoming_messages = b""

        await self._queue.join()

    async def _initiate_connection(self):
        """Connect to the Server"""
        # Monitor for poll
        self._poll_worker = asyncio.create_task(self._repeating_poll())
        if self._rate_limit:
            self._send_worker = asyncio.create_task(self._rate_limit_send())
        # await self.queue.join()
        while True:
            try:
                reader, self._writer = await asyncio.open_connection(self._host, self._port)
                self._set_connected(state=True)
                await self._socket_listener(reader)
                self._writer.close()
                logger.debug(f"{self._host} -- Socket was closed")
                await self._writer.wait_closed()
                self._set_connected(state=False)
            except (asyncio.TimeoutError, ConnectionRefusedError, OSError) as e:
                logger.debug(f"{self._host} -- An error occurred opening the socket: {e}")
            logger.warning(f"{self._host} -- Attempting reconnect...")
            await asyncio.sleep(5)

    async def _rate_limit_send(self):
        """Send data to server in a rate limited fashion"""
        while True:
            try:
                data = self._queue.get_nowait()
            except asyncio.QueueEmpty:
                await asyncio.sleep(.001)
                continue
            self._send_to_socket(data)
            self._queue.task_done()
            if self._rate_limit:
                await asyncio.sleep(self._rate_limit)
            else:
                await asyncio.sleep(.001)

    def _send_to_socket(self, data):
        if self._writer:
            # logger.debug(f"{self._host} -- Sending to server: {data}")
            if isinstance(data, bytes):
                self._writer.write(data)
            elif self._delimiter:
                self._writer.write(f"{data}".encode() + self._delimiter)
            else:
                self._writer.write(f"{data}".encode())
        else:
            logger.critical(f"Unable to send when not connected, discarding message {repr(data)}")

    def create_poll(self, rate: int, messages: List[bytes | str]):
        """This creates a thread that polls at the rate and with the message provided"""
        self._poll = (rate, messages)

    async def _repeating_poll(self):
        """Send the same message over and over, used for polling"""
        while True:
            if self._writer and self._poll:
                for item in self._poll[1]:
                    self.send(item)
                    await asyncio.sleep(self._poll[0])
            else:
                # do nothing
                await asyncio.sleep(1)

    def _set_connected(self, state: bool):
        """Sets connection state"""
        self.connected = state
        if self._connection_status:
            self._connection_status(state)

    def _connection(self):
        """Function for the thread"""
        asyncio.run(self._initiate_connection())

    def connect(self):
        """Starts attempting to connect"""
        threading.Thread(target=self._connection, name="Basic TCP Client Thread", daemon=True).start()

    def send(self, data: str | bytes):
        """Send data to the Server"""
        if not self._rate_limit:
            self._send_to_socket(data)
        else:
            try:
                self._queue.put_nowait(data)
            except asyncio.QueueFull:
                # Start removing items from the queue
                self._queue.get_nowait()
                self._queue.task_done()

    def __str__(self):
        return f"BasicTCP -- {self._host}:{self._port} connected: {self.connected}"

    def __repr__(self):
        return f"BasicTCP({self._host}:{self._port} -- Connected: {self.connected})"


def test_receive(data):
    logger.critical(f"Got {data}")


if __name__ == "__main__":
    my_client = TCPClient(host='127.0.0.1', port=12345, delimiter='', receive=test_receive, rate_limit=0.1)
    my_client.connect()
    import time
    for i in range(20):
        my_client.send(f"Test: {i}  ")
    while True:
        time.sleep(.1)
