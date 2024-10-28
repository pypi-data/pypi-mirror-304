import threading
from concurrent.futures import ThreadPoolExecutor

from shared_kernel.messaging import AWSDataBus


class EventExecutor():
    def __init__(self):
        self.databus:AWSDataBus = AWSDataBus()
        self.event_connector = {}

    def _callback_wrapper(self, event_name, callback, message):
        try:
            callback(message)
        except Exception as e:
            # logger.error(f"Error while invoking callback for event: {queue.event_name}")
            self.databus.sent_to_dead_letter_queue(event_name, message, e)
        finally:
            self.databus.delete_message(message, event_name)

    def _listen_events(self,event_name, executor:ThreadPoolExecutor, callback):
        while True:
            # Block until you get a job
            message = self.databus.get_async_event(event_name)
            # Block if concurreny has hit the limit
            executor.submit(self._callback_wrapper,args=[callback, event_name, message])


    def register_event(self, event_name, callback, max_concurrency):
        self.databus.subscribe_async_event(event_name)
        executor = ThreadPoolExecutor(max_concurrency)
        thread = threading.Thread(target=self._listen_events, args=[event_name, executor, callback])
        thread.start()




