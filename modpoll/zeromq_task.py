import logging
import argparse
from typing import Optional

import zmq

args: Optional[argparse.Namespace] = None
log: Optional[logging.Logger] = None
context: Optional[zmq.Context] = None
socket: Optional[zmq.Socket] = None


def zeromq_setup(config: argparse.Namespace) -> bool:
    global args, log, context, socket
    args = config
    log = logging.getLogger(__name__)

    try:
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://127.0.0.1:{args.zeromq_port}")

        log.info(f"ZeroMQ server started on port {args.zeromq_port}")
        return True

    except zmq.error.ZMQError as ex:
        log.error(f"ZeroMQ connection error: {ex}")
        return False


def zeromq_publish(topic: str, data: str) -> None:
    global socket
    if socket:
        socket.send_string(f"{topic} {data}")
        log.info(f"Published data to ZeroMQ topic: {topic}")
    else:
        log.error("ZeroMQ socket is not available for publishing")


def zeromq_close() -> None:
    global socket, context, log
    if socket:
        socket.close()
    if context:
        context.term()
    log.info("ZeroMQ connection closed.")