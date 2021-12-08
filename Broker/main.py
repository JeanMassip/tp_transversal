import concurrent.futures

import concurrent.futures, queue
import logging
import threading
from handler import CAMHandler
from receiver import Receiver

def main():
    event = threading.Event()
    try:
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        cam_receiver = Receiver("localhost", 1883)
        denm_receiver = Receiver("localhost", 1883)

        cam_queue = queue.Queue()
        denm_queue = queue.Queue()

        cam_handler = CAMHandler("localhost", 1883, cam_queue)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            logging.info("Starting receiver threads...")
            executor.submit(cam_receiver.start(cam_queue, "/sensors/cam"))
            executor.submit(denm_receiver.start(denm_queue, "/sensors/denm"))
            executor.submit(cam_handler.handle_message(event))
    finally:
        event.set()
        cam_receiver.stop("/sensors/cam")
        denm_receiver.stop("/snesors/denm")
        del cam_receiver
        del denm_receiver
        del cam_handler
