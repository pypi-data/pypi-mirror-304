import json
import threading
import time
from typing import Callable, Dict, Any
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from botocore.exceptions import ClientError

from shared_kernel.config import Config
from shared_kernel.interfaces.databus import DataBus
from shared_kernel.logger import Logger
from shared_kernel.messaging.utils.aws_utility import AWSMessagingUtility, AWSQueue

app_config = Config()
logger = Logger(app_config.get("APP_NAME"))


class AWSDataBus(DataBus):
    """
    An EventBridge and SQS interface class to handle event-driven communication.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AWSDataBus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the AWSDataBus and start listening to multiple SQS queues.

        Args:
            config (Dict): A dictionary containing the EventBridge and SQS configuration.
        """
        if not hasattr(self, "initialized"):  # Prevent reinitialization
            super().__init__()
            self.aws_utility = AWSMessagingUtility()
            self.event_bus_name = app_config.get("EVENT_BUS_NAME")
            self.service_name = app_config.get("APP_NAME")
            self.event_concurrent_executors: Dict[str, ThreadPoolExecutor] = {}
            self.initialized = True

    def _add_event_concurrency(self, event_name: str):
        """
        Configure concurrency settings for processing events associated with a specific event name.

        This method creates a ThreadPoolExecutor that allows concurrent processing of messages
        for the specified event type. The maximum number of worker threads is determined
        by a configuration setting specific to the event.

        Args:
            event_name (str): The name of the event for which concurrency is being configured.
        """
        max_workers = int(app_config.get(f"{event_name.upper()}_CONCURRENCY"))
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.event_concurrent_executors[event_name] = executor

    def make_connection(self):
        pass

    def close_connection(self):
        pass

    def request_event(self, event_name: str, event_payload: dict) -> Any:
        pass

    def publish_event(self, event_name: str, event_payload: dict) -> bool:
        """
        Publish an event to the EventBridge and check if it was successful.

        Args:
            event_name (str): The name of the event to publish.
            event_payload (dict): The payload of the event.

        Returns:
            bool: True if the event was published successfully, False otherwise.
        """
        return self.aws_utility.publish_event(event_name, event_payload)

    def subscribe_sync_event(self, event_name: str, callback: Callable[[Any], None]):
        """
        Not applicable
        """
        pass

    def sent_to_dead_letter_queue(self, event_name, message, failure_reason):
        pass

    def _queue_executor(self, queue: AWSQueue, callback):
        while True:
            message = self.aws_utility.get_message_from_queue(queue)
            if message:
                try:
                    callback(message)
                except Exception as e:
                    logger.error(f"Error while invoking callback for event: {queue.event_name}")
                    self.sent_to_dead_letter_queue(queue.event_name, message, e)
                finally:
                    self.delete_message(message, queue)

    def _event_executor(self, queue: AWSQueue, callback):
        thread = threading.Thread(target=self._queue_executor, args=[queue, callback])
        thread.start()

    def subscribe_async_event(self, event_name: str, callback: Callable[[Any], None]):
        """
        Subscribe to an event by creating an EventBridge rule and store the callback for the event.

        Args:
            event_name (str): The name of the event to subscribe to.
            callback (Callable[[Any], None]): The callback function to be invoked when the event is received.
        """
        aws_queue = None
        if not self.aws_utility.check_if_queue_exist(event_name):
            aws_queue: AWSQueue = self.aws_utility.create_queue(event_name)
            self.aws_utility.add_event_bridge_rule(aws_queue)
        else:
            aws_queue = self.aws_utility.get_queue(event_name)
            logger.info(f"Queue already exists: {aws_queue.url}")
        self.event_queue_mapper.put(event_name, aws_queue)
        # self._event_executor(aws_queue, callback)

    def get_async_message(self, event_name):
        queue = self.event_queue_mapper[event_name]
        # get_message_from_queue should be blocking
        message = self.aws_utility.get_message_from_queue(queue)
        return message

    def delete_message(self, message, queue: AWSQueue):
        """
        Delete a message from the SQS queue.

        Args:
            receipt_handle (str): The receipt handle associated with the message to delete.
        """
        try:
            self.aws_utility.delete_message_from_queue(queue, message)
        except ClientError as e:
            logger.error(f"Failed to delete message from SQS: {e}")
