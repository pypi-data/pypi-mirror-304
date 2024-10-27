from dataclasses import dataclass
from typing import Final, List

import requests


@dataclass
class Device:
    host: Final[str]
    """hostname or IP address, e.g. `192.168.1.251`"""

    device_id: Final[str]
    """Device ID, e.g. `000116343328`"""

    url: Final[str]
    """
    A device url follows this scheme:

    `https://<host>/Devices/<device_id>`

    e.g. `'https://192.168.1.251/Devices/000116343328'`
    """

    def __init__(self, host: str, device_id: str) -> None:
        """
        host: hostname or IP address
        device_id: Device ID

        The device url is derived from that parameters.
        000.177.597.163
        """

        self.host = host
        self.device_id = device_id

        self.url = f"https://{self.host}/Devices/{self.device_id}"


def get_devices_from_host(
    host: str, verify_https: bool | str = False, https_timeout: float = 3.0
) -> List[Device]:
    """
    host: hostname or IP address

    verify_https: is passed to the `requests.request` `verify` argument

    https_timeout: timeout for the request, in seconds


    Gets the list of all devices that live on the specified host.

    **raises**: `ValueError`, if the request does not return HTTP 200 status code.
    """
    url = f"https://{host}/Devices"

    payload = {}
    headers = {}

    response = requests.request(
        "GET",
        url,
        headers=headers,
        data=payload,
        verify=verify_https,
        timeout=https_timeout,
    )

    if response.status_code != 200:
        raise ValueError(f"Unable to GET: got HTTP response {response}")

    return [Device(host, id_str) for id_str in response.json().keys()]
