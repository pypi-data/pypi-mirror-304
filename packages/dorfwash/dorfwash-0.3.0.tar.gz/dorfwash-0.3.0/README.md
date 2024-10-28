# dorfwash

[![PyPI](https://img.shields.io/pypi/v/dorfwash.svg)](https://pypi.org/project/dorfwash/)
[![License](https://img.shields.io/pypi/l/dorfwash)](https://pypi.org/project/dorfwash/)

`dorfwash` lets you monitor your Miele washing machines
via the Miele Professional IP Profile API.

`dorfwash` uses [washpy](https://pypi.org/project/washpy/)
to communicate with the Miele washing machines.

## Usage

There are multiple options on how to run `dorfwash`.

### poetry

run
```bash
poetry run python dorfwash config.json
```
See [config.json](config.json) for an example configuration.

#### Device Setup

If you have a new washing machine and want to set it up for use with `dorfwash`,
you can use the [setup_new_device.py](setup_new_device.py):
```bash
poetry run python setup_new_device.py
```
The script will discover a device URL four you,
given that you provide it with an IP address or a hostname of the washing machine / XKM module.
Use that device URL in the [config.json](config.json).
> Note: You will need to discover the IP address or hostname of the machine on your own.
> I found [arp-scan](https://github.com/royhills/arp-scan) to be a helpful tool for that.

Then, the script will initialize the admin user. You have to choose an admin password.
Then, it will set up a non-admin user with a name and password of you liking.

Be aware, that the Miele IP Profile API may require you to choose a strong enough password
(e.g. at least 8 characters, use of upper case, lower case, digits, special characters).

### docker

`dorfwash` provides a small [Dockerfile](Dockerfile),
so you can build your own `dorfwash` docker container.

```bash
docker build -t dorfwash .
```

You need to mount a valid `config.json` file at
`/config/config.json` in the container to run it.

Also, in [docker-compose](docker-compose) is an example `docker-compose.yml`.
This way, you can just run
```bash
docker compose up
```
to build, mount the config, and run the server.


## Miele IP Profie API

For further information see [washpy](https://pypi.org/project/washpy/)
