"""Example program using the client -- this example controls a SVSi decoder"""
import logging
import time

from muse_basic_tcp_client.tcp_client import TCPClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Create a function to receive responses
def from_decoder(data):
    # logger.debug(f"Data from server: {data}")
    if 'STREAM' in data[:6]:
        stream = data.replace('STREAM:', '')
        logger.debug(f"Decoder is on stream: {stream}")


# Optional -- A function to be notified of status changes
def on_line(status):
    logger.debug(f"Online is now: {status}")


# Configure the client
svsi_decoder = TCPClient(host="172.17.0.26", port=50002, connection_status=on_line, delimiter="\r", receive=from_decoder)

svsi_decoder.create_poll(rate=1, messages=['getStatus;'])
# connect to the decoder
svsi_decoder.connect()


# simulate the program running
for i in range(10):
    time.sleep(1)
