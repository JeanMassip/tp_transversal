import concurrent.futures, queue
import logging
import threading
from handler import CAMHandler, DENMHandler
from receiver import Receiver

def main():
    event = threading.Event()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    try:
        cam_queue = queue.Queue()
        denm_queue = queue.Queue()

        cam_receiver = Receiver("mosquitto", cam_queue)
        denm_receiver = Receiver("mosquitto", denm_queue)

        cam_handler = CAMHandler("mosquitto", 1883, cam_queue)
        denm_handler = DENMHandler("mosquitto", 1883, denm_queue)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            logging.info("Starting receiver threads...")
            executor.submit(cam_receiver.start(cam_queue, "/sensors/cam"))
            executor.submit(denm_receiver.start(denm_queue, "/sensors/denm"))
            logging.info("Starting handlers...")
            executor.submit(cam_handler.handle_message(event))
            executor.submit(denm_handler.handle_message(event))
            executor.shutdown(True)
        

    finally:
        event.set()
        cam_receiver.stop("/sensors/cam")
        denm_receiver.stop("/snesors/denm")
        del cam_receiver
        del denm_receiver
        del cam_handler

if __name__ == '__main__':
    main()
