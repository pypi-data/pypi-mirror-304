import requests
import json


def post_new_password(
    device_url: str,
    user: str,
    password_old: str,
    password_new: str,
    verify_https: bool | str = False,
    https_timeout: float = 3.05,
) -> None:
    """
    `device_url`: e.g. `'https://192.168.1.251/Devices/000116343328'`

    `user`: e.g. `'MYUSER'`

    `password_old`: old password

    `password_new`: the new password to be set

    `verify_https`: is passed to the `requests.request` `verify` argument

    `https_timeout`: timeout for HTTPS connections, in seconds

    **raises**: `ValueError`, if the password change was unsuccessfull
    """
    payload = json.dumps(
        {"LoginName": user, "Password": password_old, "PasswordNew": password_new}
    )
    headers = {"Content-Type": "application/json"}

    url = device_url + "/profSession"
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload,
        verify=verify_https,
        timeout=https_timeout,
    )
    if response.status_code != 204:
        raise ValueError(f"something went wrong: got HTTP response {response}")
