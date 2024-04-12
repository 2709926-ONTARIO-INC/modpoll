import argparse
import logging
from typing import Optional
import zmq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log: logging.Logger = logging.getLogger(__name__)

args: Optional[argparse.Namespace] = None 
ZMQ_PORT: int = 0
TOPIC: bytes = b""


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='ZeroMQ receiver')
    parser.add_argument(
        "--zeromq-port",
        default=5555,
        help="Specify ZeroMQ subscriber port. Defaults to 5555.",
    )
    parser.add_argument(
        "--zeromq-topic",
        required=True,
        help="Specify ZeroMQ subscriber topic. Required!",
    )
    return parser


def zeromq_connect() -> Optional[zmq.Socket]:
    try:
        # Create ZeroMQ context
        context: zmq.Context = zmq.Context()

        # Create ZeroMQ socket
        socket: zmq.Socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://127.0.0.1:{ZMQ_PORT}")

        # Subscribe to all messages
        socket.subscribe(TOPIC)

        log.info(f"Connected to ZeroMQ publisher at 127.0.0.1:{ZMQ_PORT} for topic '{TOPIC.decode()}'")
        return socket

    except zmq.error.ZMQError as ex:
        log.error(f"ZeroMQ connection error: {ex}")
        return None


def zeromq_receive() -> None:
    socket: Optional[zmq.Socket] = zeromq_connect()
    if socket:
        try:
            while True:
                message = socket.recv()
                log.info(f"Received message from topic: {message}")
        except (zmq.error.ZMQError, KeyboardInterrupt) as ex:
            log.error(f"ZeroMQ receive error: {ex}")
        finally:
            zeromq_close(socket)
    else:
        log.error("Failed to connect to ZeroMQ publisher")


def zeromq_close(socket: zmq.Socket) -> None:
    try:
        socket.close()
        log.info("ZeroMQ connection closed.")
    except zmq.error.ZMQError as ex:
        log.error(f"ZeroMQ close error: {ex}")


def main() -> None:
    global args, ZMQ_PORT, TOPIC
    args = get_parser().parse_args() 
    ZMQ_PORT = args.zeromq_port
    TOPIC = args.zeromq_topic.encode()
    zeromq_receive()

if __name__ == "__main__":
    main()