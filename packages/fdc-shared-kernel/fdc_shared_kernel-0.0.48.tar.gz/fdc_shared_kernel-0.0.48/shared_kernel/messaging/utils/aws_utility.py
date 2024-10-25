import json
from typing import Dict

import boto3
from botocore.exceptions import ClientError

from shared_kernel.config import Config
from shared_kernel.logger import Logger

config = Config()
logger = Logger(config.get("APP_NAME"))


class AWSUtility:
    """
    Manages AWS operations such as EventBridge rules, SQS queue creation, and message handling.
    """

    def __init__(self, config: Dict = None):
        self.event_bridge = boto3.client("events")
        self.sqs = boto3.client("sqs")
        self.event_bus_name = config.get("event_bus_name")
        self.service_name = config.get("service_name")

    def create_queue(self, event_name: str):
        """
        Create a new SQS queue for the event.
        Args:
            event_name (str): The name of the event for which the queue is created.
        """
        queue_url = self.check_if_queue_exist(event_name)
        if queue_url:
            queue_arn = self.get_queue_arn(queue_url)
            return queue_url, queue_arn

        queue_name = f"{self.service_name}-{event_name}"
        response = self.sqs.create_queue(QueueName=queue_name)
        queue_url = response["QueueUrl"]
        queue_arn = self.get_queue_arn(queue_url)
        logger.info(f"Queue '{queue_name}' created with URL: {queue_url}")
        return queue_url, queue_arn

    def get_queue_arn(self, queue_url: str) -> str:
        """
        Retrieve the ARN of an SQS queue given its URL.

        Args:
            queue_url (str): The URL of the queue.

        Returns:
            str: The ARN of the queue.
        """
        response = self.sqs.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["QueueArn"]
        )
        return response["Attributes"]["QueueArn"]

    def check_if_queue_exist(self, event_name: str) -> bool:
        """
        Check if an SQS queue for a specific event exists by querying AWS SQS.
        Args:
            event_name (str): The name of the event.
        Returns:
            bool: True if the queue exists, otherwise False.
        """
        queue_name_prefix = f"{self.service_name}-{event_name}"

        response = self.sqs.list_queues(QueueNamePrefix=queue_name_prefix)
        queue_urls = response.get("QueueUrls", [])

        return True if queue_urls else False

    def add_event_bridge_rule(self, event_name: str):
        """
        Add an EventBridge rule to forward the event to the SQS queue.
        Args:
            event_name (str): The name of the event to subscribe to.
        """
        rule_name = f"{event_name}_rule"
        event_pattern = json.dumps({"detail-type": [event_name]})
        self.event_bridge.put_rule(
            Name=rule_name,
            EventPattern=event_pattern,
            State="ENABLED",
            EventBusName=self.event_bus_name,
        )
        self.event_bridge.put_targets(
            Rule=rule_name,
            EventBusName=self.event_bus_name,
            Targets=[
                {
                    "Id": f"{event_name}_sqs_target",
                    "Arn": self.queue_arn,
                }
            ],
        )
        logger.info(f"EventBridge rule '{rule_name}' added.")

    def get_messages_from_queue(self, queue_url):
        """
        Poll the SQS queue for messages.
        Returns:
            List[Dict]: A list of messages received from the SQS queue.
        """
        response = self.sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
        )
        return response.get("Messages", [])

    def delete_message_from_queue(self, queue_url, message: Dict):
        """
        Delete a message from the SQS queue.
        Args:
            message (Dict): The message to be deleted.
        """
        self.sqs.delete_message(
            QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
        )
        logger.info(
            f"Message deleted from queue with receipt handle '{message['ReceiptHandle']}'."
        )

    def publish_event(self, event_name: str, event_payload: dict):
        """
        Publish an event to EventBridge.
        Args:
            event_name (str): The name of the event.
            event_payload (dict): The payload of the event.
        Returns:
            bool: True if the event was successfully published.
        """
        try:
            response: dict = self.event_bridge.put_events(
                Entries=[
                    {
                        "Source": self.service_name,
                        "DetailType": event_name,
                        "Detail": json.dumps(event_payload),
                        "EventBusName": self.event_bus_name,
                    }
                ]
            )
            logger.info(f"Published event '{event_name}' with payload: {event_payload}")

            if response["FailedEntryCount"] > 0:
                logger.error(
                    f"Failed to publish event '{event_name}': {response['Entries'][0].get('ErrorMessage', 'Unknown error while publishing event')}"
                )
                return False
            else:
                event_id = response["Entries"][0].get("EventId")
                logger.info(
                    f"Successfully published event '{event_name}' with EventId: {event_id}"
                )
                return True
        except ClientError as e:
            logger.error(f"Failed to publish event: {e}")
            return False
