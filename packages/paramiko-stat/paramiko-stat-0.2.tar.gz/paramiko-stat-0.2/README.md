
---
# paramiko-stat
This is just a wrapper for paramiko with changes included from https://github.com/paramiko/paramiko/pull/1259/files.


## Install it from PyPI

```bash
pip install paramiko-stat
```

## Usage

```py
from paramiko_stat import SSHClient

ssh = SSHClient()
ssh.connect("127.0.0.1", username="user", ...)
sftp = ssh.open_sftp()
sftp.mkdir("path", mode=700)

```
Alternatively, a much better practice:

```py
from paramiko import SSHClient
from paramiko_stat import Transport

ssh = SSHClient()
ssh.connect("127.0.0.1", username="user", ..., transport_factory=Transport)

```
