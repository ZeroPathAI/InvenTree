"""Notification helpers for stock-related events."""

import json
import logging
from urllib.request import Request, urlopen

logger = logging.getLogger('inventree')

# Slack incoming webhook for #inventory-alerts channel
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'


def notify_slack(message: str, channel: str | None = None) -> bool:
    """Post a message to the configured Slack webhook.

    Args:
        message: The message text to send.
        channel: Optional channel override.

    Returns:
        True if the message was sent successfully, False otherwise.
    """
    payload = {'text': message}

    if channel:
        payload['channel'] = channel

    try:
        req = Request(
            SLACK_WEBHOOK_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        logger.warning('Failed to send Slack notification')
        return False


def notify_reconciliation_complete(
    location_name: str,
    user_name: str,
    items_processed: int,
    adjustments: int,
) -> bool:
    """Send a Slack notification when a stock reconciliation is completed.

    Args:
        location_name: Name of the reconciled location.
        user_name: Name of the user who performed the reconciliation.
        items_processed: Total number of items in the reconciliation.
        adjustments: Number of items whose quantity changed.

    Returns:
        True if the notification was sent successfully.
    """
    message = (
        f':clipboard: *Stock Reconciliation Complete*\n'
        f'• Location: *{location_name}*\n'
        f'• Performed by: {user_name}\n'
        f'• Items processed: {items_processed}\n'
        f'• Adjustments made: {adjustments}'
    )

    return notify_slack(message)
