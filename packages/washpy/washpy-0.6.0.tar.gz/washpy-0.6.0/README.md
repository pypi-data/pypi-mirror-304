# washpy

[![PyPI](https://img.shields.io/pypi/v/washpy.svg)](https://pypi.org/project/washpy/)
[![License](https://img.shields.io/pypi/l/washpy)](https://pypi.org/project/washpy/)
[![documentation](https://img.shields.io/badge/washpy-documentation-blue?logo=bookstack)](https://johann-cm.codeberg.page/washpy/washpy.html)


washpy offers a partial implementation of the Miele Professional IP Profile API.

The project focusses on implementing the parts of the API
for washing machines from Miele Professional.

## Getting started

### Documentation

Read the [documentation of washpy](https://johann-cm.codeberg.page/washpy/washpy.html).

### Project with washpy usage

washpy is used in the [dorfwash](https://pypi.org/project/dorfwash/) project. You can have a look there on how to use washpy in practice.

## Installation

[washpy is available on PyPI](https://pypi.org/project/washpy/),
so washpy can be installed via `pip`, [poetry](https://python-poetry.org/),
or any other tool that interfaces with PyPI.

### Hardware setup

I have tested this library on Miele Professional PWM 507 machines,
with the Miele XKM 3200-WL-PLT KOM module.

- slide the KOM module into the slot of your machine
- connect the RJ45 jack of the module to your network
  - at the time of writing (2024), the modules need a network with DHCP,
    they do not support static IP addresses

### Set up your KOM module

You have to somehow find out the IP addresses of your machines.
For that, I can recommend [arp-scan](https://github.com/royhills/arp-scan)
to discover all hosts in your IPv4 network.

Now, give your machine a visit with your web browser,
and if your browser asks you about the SSL certificate being untrustworthy,
tell the browser to trust the certificate:
```
https://{your.device.ip.address}/Devices/
```

From there, you can get your machines' fabrication number.
This is important for all further calls to the API

#### Activate the admin user

On the KOM module, there exists the `Admin` default user,
with the default password `""` (the empty string).

I had to activate the admin user by changing its password:

```python
from washpy import post_new_password

post_new_password(
    "https://192.168.1.251/Devices/000116343328", "Admin", "", "verySecurePassword!"
)
```

#### Add new User

```python
from washpy import DeviceUser
from washpy.user import User

d = DeviceUser(
    "https://192.168.1.251/Devices/000116343328", "Admin", "verySecurePassword!"
)

user = User(
    ID=102,
    LoginName="MyUser",
    Password="evenStrongerPassword!",
    Description="My first User",
    Roles=[1, 2],
)

# user the Admin standard user to add a new user
d.post_new_user(user)
```

#### Interact with a device

The core of washpy is the `DeviceUser` class. Once constructed,
it provides many methods to control the Miele device.

The script
```python
from washpy import DeviceUser

my_device = DeviceUser(
    "https://192.168.1.251/Devices/000116343328", "Admin", "verySecurePassword!"
)

print(my_device.get_state().Status)
```
will yield
```python
<Status.RUNNING: 5>
```

See also the [exapmles](examples) folder for more usage examples.

## Is there documentation of the IP Profile API?

Yes, you have to request access to it from [Miele Professional](https://www.miele.com/en/com/index-pro.htm).

## known issues

Do not upgrade requests, as it will upgrade to urllib3 version `2.x`.

Problem: you will get handshake errors:

```python
SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] ssl/tls alert handshake failure (_ssl.c:1006)'))
```

Also see this [GitHub Issue](https://github.com/urllib3/urllib3/pull/3060#issuecomment-1578815249).

## License

[LGPL-3.0-only](LICENSE)
