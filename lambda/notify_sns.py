"""
    Forward SNS
    ------------
    Receives event payloads from SNS that are parsed and sent to Slack
"""

import json
import logging
import os
from typing import Any, Dict

import boto3

client = boto3.client("sns")

REGION = os.environ.get("AWS_REGION", "us-east-1")


def send_sns(payload: Dict[str, Any]) -> str:
    """
    Send notification payload to SNS

    :params payload: message payload
    :returns: response details from sending notification
    """

    forward_to_sns = os.environ["FORWARD_TO_SNS_ARN"]
    response = client.publish(TopicArn=forward_to_sns, Message=payload)

    return response


def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Lambda function to parse notification events and forward to Slack

    :param event: lambda expected event object
    :param context: lambda expected context object
    :returns: none
    """
    if os.environ.get("LOG_EVENTS", "False") == "True":
        logging.info(f"Event logging enabled: `{json.dumps(event)}`")

    for record in event["Records"]:
        sns = record["Sns"]
        subject = sns["Subject"]
        message = sns["Message"]
        region = sns["TopicArn"].split(":")[3]

        response = send_sns(payload=message)

    if json.loads(response)["code"] != 200:
        response_info = json.loads(response)["info"]
        logging.error(
            f"Error: received status `{response_info}` using event `{event}` and context `{context}`"
        )

    return response


t
