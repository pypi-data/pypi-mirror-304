import uuid
import base64
from datetime import datetime, timezone, timedelta
import re
import rfc3987
import validators


def valid_datetime_string(datetime_string):
    try:
        datetime.fromisoformat(datetime_string)
        return True
    except ValueError:
        return False


def valid_did(value):
    DID_REGEX = re.compile("did:([a-z0-9]+):((?:[a-zA-Z0-9._%-]*:)*[a-zA-Z0-9._%-]+)")
    if DID_REGEX.match(value):
        return True
    return False


def valid_url(value):
    return validators.url(value)


def valid_uri(value):
    if valid_did(value) or rfc3987.parse(value, rule="URI"):
        return True
    return False


def id_from_string(string):
    return f"urn:uuid:{str(uuid.uuid5(uuid.NAMESPACE_DNS, string))}"


def b64_encode(message):
    return base64.urlsafe_b64encode(message).decode().rstrip("=")


def datetime_range(days=None, minutes=None):
    start = datetime.now(timezone.utc).isoformat("T", "seconds")
    if days:
        end = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat(
            "T", "seconds"
        )
    elif minutes:
        end = (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat(
            "T", "seconds"
        )
    return start, end
